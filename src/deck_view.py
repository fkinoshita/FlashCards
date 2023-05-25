# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Adw, Gtk

@Gtk.Template(resource_path='/io/github/fkinoshita/FlashCards/ui/deck_view.ui')
class DeckView(Gtk.Box):
    __gtype_name__ = 'DeckView'

    back_button = Gtk.Template.Child()
    deck_icon = Gtk.Template.Child()
    edit_icon_button = Gtk.Template.Child()
    emoji_chooser = Gtk.Template.Child()
    page_title = Gtk.Template.Child()
    name_entry = Gtk.Template.Child()
    cards_list = Gtk.Template.Child()
    new_card_button = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
