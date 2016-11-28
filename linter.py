#
# linter.py
# Linter for SublimeLinter3, a code checking framework for Sublime Text 3
#
# by Daniel (dmilith) Dettlaff
# based on work by Gregory Oschwald in 2014
#
# License: MIT
#
"""This module exports the Rustc plugin class."""

import os
from os.path import dirname, realpath
from SublimeLinter.lint import Linter, util


class Rust(Linter):
    """Provides an interface to Rust +1.13.0 with new error output"""

    cmd = [dirname(realpath(__file__)) + '/cargo-sublimelint-helper']
    syntax = 'rust'

    multiline = True
    regex = (
             r'^(?P<error>error.*):\s+(?P<message>.+)\s+'
             r'^\s+-->\s+(?P<file>.+):(?P<line>\d+):(?P<col>\d+)\s+'
            )

    def run(self, cmd, code):
        current_dir = os.path.dirname(self.filename)
        self.cargo_config = util.find_file(current_dir, 'Cargo.toml')

        try:
            os.chdir(os.path.dirname(self.cargo_config))
            return util.communicate(cmd,
                                    code=code,
                                    output_stream=self.error_stream,
                                    env=self.env)
        finally:
            os.chdir(current_dir)
