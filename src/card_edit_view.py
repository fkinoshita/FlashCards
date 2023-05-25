# card_edit_page.py
#
# Copyright 2023 Felipe Kinoshita
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
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

