import subprocess
import os


def _get_root(path):
    """Get root from path"""
    return os.path.join(path, '..')


def create_tarball(path, context):
    """Create tarball"""
    root = _get_root(path)
    destination = '{}_{}.orig.tar.xz'.format(
        context['name'], context['version'],
    )
    subprocess.call(['tar', 'cJvf', destination, context['name']], cwd=root)


def build(path, key, context):
    """Build package data"""
    root = _get_root(path)
    subprocess.call([
        'debuild', '-S', '-sa', '-rfakeroot', '-k{}'.format(key),
    ], cwd=path)
    return os.path.join(root, '{}_{}-0~{}_source.changes'.format(
        context['name'], context['version'], context['release'],
    ))


def push(changes, ppa):
    """Push to ppa"""
    subprocess.call(['dput', ppa, changes])
