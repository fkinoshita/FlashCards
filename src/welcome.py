# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Adw, Gtk

@Gtk.Template(resource_path='/io/github/fkinoshita/FlashCards/ui/welcome.ui')
class Welcome(Adw.NavigationPage):
    __gtype_name__ = 'Welcome'

    start_button = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
