from datetime import datetime
import subprocess
import os
import setuptools
import sys
from ..helpers.revision import Revision
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

    def _get_commit_datetime(self, commit=None):
        """Get commit date, if None - use current commit"""
        git_args = ['log', '-1', '--format=%ct']
        if commit is not None:
            git_args.append(commit)
        timestamp = self._git(*git_args).readline()
        return datetime.fromtimestamp(float(timestamp[:-1]))

    def _set_current_commit_date(self):
        """Set current commit date"""
        self._current = self._get_commit_datetime()

    def _is_before_current(self, commit):
        """Is commit before current"""
        commit_date = self._get_commit_datetime(commit)
        return commit_date <= self._current

    def _store_args(self, *args, **kwargs):
        """Store arguments to setup"""
        self._data = kwargs

    def _get_revisions_with_changes(self):
        """Get revisions with changes"""
        out = self._git('log', '--pretty=format:%h', 'setup.py')
        return [
            line[:-1] for line in out.readlines()
            if self._is_before_current(line[:-1])
        ][::-1]

    def _get_commits_with_versions(self, commits):
        """Get commits with versions"""
        versions = []
        setup = None
        for commit in commits:
            with Revision(commit, self._path) as revision:
                sys.path.insert(0, revision.destination)
                if setup is None:
                    setup = __import__('setup')
                else:
                    reload(setup)
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
        self._set_current_commit_date()
        self._patch_setuptools()
        changes = self._get_revisions_with_changes()
        version_pairs = self._get_commits_with_versions(changes)
        return list(self._create_change_logs(version_pairs))
