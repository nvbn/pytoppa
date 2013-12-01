import os
from .contexts.globals import GlobalContext
from .contexts.release import ReleaseContext
from .helpers.temporary import TemporaryDirectory
from .helpers.package_data import PackageData


def main():
    path = os.getcwdu()
    context = GlobalContext(path)
    with TemporaryDirectory(path, context) as temp:
        for release in context['releases']:
            release_context = ReleaseContext(context, release)
            with PackageData(temp.destination, release_context):
                print 'horray'


if __name__ == '__main__':
    main()
