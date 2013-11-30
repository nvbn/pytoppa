import subprocess
import os
import setuptools
from .exceptions import ParsingError


class GitParser(object):
    """Git parser"""

    def _git(self, *args):
        """Get output of call to git"""
        proc = subprocess.Popen(
            ['git'] + list(args), stdout=subprocess.PIPE,
            cwd=self._path,
        )
        proc.wait()
        return proc.stdout

    def _patch_setuptools(self):
        """Patch setuptools"""
        setuptools.setup = self._store_args

    def _store_args(self, *args, **kwargs):
        """Store arguments to setup"""
        self._data = kwargs

    def _get_revisions_with_changes(self):
        """Get revisions with changes"""
        out = self._git('log', '--pretty=format:%h', 'setup.py')
        return [line[:-1] for line in out.readlines()][::-1]

    def _get_setup_py_content(self, commit):
        """get setup.py content in commit"""
        return self._git('show', '{}:setup.py'.format(commit)).read()

    def _get_commits_with_versions(self, commits):
        """Get commits with versions"""
        versions = []
        for commit in commits:
            exec self._get_setup_py_content(commit)
            if not self._data['version'] in versions:
                versions.append(self._data['version'])
                yield commit, self._data['version']

    def _get_commit_range_changes(self, end, start=None):
        """Get changes in commit range"""
        out = self._git(
            'log', '--pretty=format:%s',
            '{}...{}'.format(start, end) if start else end,
        )
        return [
            line.replace('\n', '').replace('\r', '')
            for line in out.readlines()
        ]

    def _get_commit_date(self, commit):
        """Get commit date"""
        return self._git('log', '--pretty=format:%cd', '--date=rfc', commit)\
            .readlines()[0]

    def _create_change_logs(self, pairs):
        """Create change logs"""
        last = None
        for commit, version in pairs:
            yield (
                version, self._get_commit_range_changes(commit, last),
                self._get_commit_date(commit),
            )
            last = commit

    def _set_path(self, path):
        """Set path"""
        git_path = os.path.join(path, '.git')
        if not os.path.exists(git_path):
            raise ParsingError('You should run pytoppa in git root')
        self._path = path

    def parse(self, path):
        """Create changelog from git"""
        self._set_path(path)
        self._patch_setuptools()
        changes = self._get_revisions_with_changes()
        version_pairs = self._get_commits_with_versions(changes)
        return list(self._create_change_logs(version_pairs))
