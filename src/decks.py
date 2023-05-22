# decks.py
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

@Gtk.Template(resource_path='/io/github/fkinoshita/FlashCards/decks.ui')
class FlashcardsDecks(Gtk.Box):
    __gtype_name__ = 'FlashcardsDecks'

    leaflet = Gtk.Template.Child()

    list_page = Gtk.Template.Child()
    edit_page = Gtk.Template.Child()
    card_page = Gtk.Template.Child()

    decks_list = Gtk.Template.Child()
    new_deck_button = Gtk.Template.Child()

    edit_page_title = Gtk.Template.Child()
    deck_image = Gtk.Template.Child()
    deck_name = Gtk.Template.Child()
    cards_list = Gtk.Template.Child()
    new_card_button = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


    @Gtk.Template.Callback()
    def on_back(self, button):
        self.leaflet.set_visible_child(self.list_page)

