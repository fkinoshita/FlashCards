# SPDX-License-Identifier: GPL-3.0-or-later

import sys
import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Adw, Gtk, Gio
from .window import Window


class FlashcardsApplication(Adw.Application):
    """The main application singleton class."""

    def __init__(self):
        super().__init__(application_id='io.github.fkinoshita.FlashCards',
                         flags=Gio.ApplicationFlags.DEFAULT_FLAGS)
        self.create_action('quit', lambda *_: self.quit(), ['<primary>q'])
        self.create_action('close', lambda *_: self.props.active_window.close(), ['<primary>w'])
        self.create_action('about', self.on_about_action)
        self.create_action('preferences', self.on_preferences_action)


    def do_activate(self):
        """Called when the application is activated.

        We raise the application's main window, creating it if
        necessary.
        """
        win = self.props.active_window
        if not win:
            win = Window(application=self)
        win.present()


    def on_about_action(self, widget, _):
        """Callback for the app.about action."""
        builder = Gtk.Builder.new_from_resource(
            "/io/github/fkinoshita/FlashCards/about_dialog.ui"
        )
        about_dialog = builder.get_object("about_dialog")
        about_dialog.set_transient_for(self.props.active_window)
        about_dialog.present()



    def on_preferences_action(self, widget, _):
        """Callback for the app.preferences action."""
        print('app.preferences action activated')


    def create_action(self, name, callback, shortcuts=None):
        """Add an application action.

        Args:
            name: the name of the action
            callback: the function to be called when the action is
              activated
            shortcuts: an optional list of accelerators
        """
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f"app.{name}", shortcuts)


def main(version):
    """The application's entry point."""
    app = FlashcardsApplication()
    return app.run(sys.argv)
