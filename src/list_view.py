# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Adw, Gtk

@Gtk.Template(resource_path='/io/github/fkinoshita/FlashCards/ui/list_view.ui')
class ListView(Gtk.Box):
    __gtype_name__ = 'ListView'

    decks_list = Gtk.Template.Child()
    new_deck_button = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
