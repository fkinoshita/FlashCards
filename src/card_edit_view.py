# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Adw, Gtk

@Gtk.Template(resource_path='/io/github/fkinoshita/FlashCards/ui/card_edit_view.ui')
class CardEditView(Gtk.Box):
    __gtype_name__ = 'CardEditView'

    front_side_view = Gtk.Template.Child()
    back_side_view = Gtk.Template.Child()

    def __init__(self, window, card, **kwargs):
        super().__init__(**kwargs)

        self.window = window
        self.card = card

        self.front_side_view.get_buffer().set_text(self.card.front)
        self.back_side_view.get_buffer().set_text(self.card.back)

        self.front_side_view.get_buffer().connect('changed', self.__on_front_side_changed)
        self.back_side_view.get_buffer().connect('changed', self.__on_back_side_changed)


    def __on_front_side_changed(self, buffer):
        (start, end) = buffer.get_bounds()
        text = buffer.get_text(start, end, False)
        self.card.front = text

        self.window.deck_view.cards_list.bind_model(self.window.current_deck.cards_model, self.window.cards_list_create_row)


    def __on_back_side_changed(self, buffer):
        (start, end) = buffer.get_bounds()
        text = buffer.get_text(start, end, False)
        self.card.back = text

