import os
import argparse
from .contexts.globals import GlobalContext
from .contexts.release import ReleaseContext
from .helpers.temporary import TemporaryDirectory
from .helpers.package_data import PackageData
from .utils import create_tarball, build, push


def _get_arguments():
    """Get arguments"""
    parser = argparse.ArgumentParser(description='py-to-ppa')
    parser.add_argument('key', type=str)
    parser.add_argument('ppa', type=str)
    return parser.parse_args()


def main():
    args = _get_arguments()
    path = os.getcwd()
    context = GlobalContext(path)
    with TemporaryDirectory(path, context) as temp:
        create_tarball(temp.destination, context)
        context.update_changelog(temp.destination)
        for release in context['releases']:
            release_context = ReleaseContext(context, release)
            with PackageData(temp.destination, release_context):
                changes = build(temp.destination, args.key, release_context)
                push(changes, args.ppa)


if __name__ == '__main__':
    main()
