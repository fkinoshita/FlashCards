# SPDX-License-Identifier: GPL-3.0-or-later

import sys
import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from .application import Application


def main(version):
    """The application's entry point."""
    app = Application()
    return app.run(sys.argv)

