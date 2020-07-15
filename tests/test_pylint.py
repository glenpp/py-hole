#!/usr/bin/env python3
"""Wrapper for using pylint in unittests
"""


import unittest
import os
import glob
import io
import sys
import warnings
import pylint.lint
import pylint.reporters.text


# config required
CODEQUALITY = 7.0
EXCLUDE = [
    'tests/'
]
INCLUDE = [
    'py-hole-bind9RPZ',
]


# see https://github.com/PyCQA/pylint/blob/master/pylint/reporters/text.py
class ErrorsOnlyReporter(pylint.reporters.text.TextReporter):
    """Errors-only Reporter

    If we exclude checks in pylint then we also don't get those in code quality ratings.
    This allows all checks to be run and ignore messages which are not vital.
    """
    def handle_message(self, msg):
        if msg.C not in 'EF':
            return
        # do the usual display things this methoud would normally do
        super().handle_message(msg)


class UnitTestPylint(unittest.TestCase):
    """pylint wrapper for unit tests
    """
    def setUp(self):
        self.cwd = os.getcwd()
        # get into top-level of project
        os.chdir(os.path.realpath(os.path.join(os.path.dirname(__file__), '..')))
    def tearDown(self):
        os.chdir(self.cwd)

    def test_pylint(self):
        """Run pylint
        """
        files = glob.glob('**/*.py', recursive=True)
        for exclude in EXCLUDE:
            files = [path for path in files if not path.startswith(exclude)]
        files += INCLUDE
        # runing within unittests causes normally supressed warnings
        warnings.simplefilter('ignore', category=PendingDeprecationWarning)
        warnings.simplefilter('ignore', category=DeprecationWarning)
        # run and check
        output = io.StringIO()
        result = pylint.lint.Run(files, reporter=ErrorsOnlyReporter(output), exit=False)
        # check
        if result.linter.stats['fatal'] > 0 or result.linter.stats['error'] > 0:
            sys.stdout.write(output.getvalue())
            self.assertEqual(result.linter.stats['fatal'], 0, "pylint: fatal found")
            self.assertEqual(result.linter.stats['error'], 0, "pylint: error found")
        self.assertGreaterEqual(
            result.linter.stats['global_note'], CODEQUALITY,
            "pylint: code quality of minimum {} required, got {}".format(
                CODEQUALITY,
                result.linter.stats['global_note']
            )
        )



if __name__ == '__main__':
    unittest.main()

