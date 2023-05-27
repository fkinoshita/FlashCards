# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Adw, Gtk

@Gtk.Template(resource_path='/io/github/fkinoshita/FlashCards/ui/card_row.ui')
class CardRow(Adw.ActionRow):
    __gtype_name__ = 'CardRow'

    edit_button = Gtk.Template.Child()

    def __init__(self, card, **kwargs):
        super().__init__(**kwargs)

        self.set_title(card.front)

