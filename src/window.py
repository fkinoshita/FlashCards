# window.py
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

from gi.repository import Adw, Gtk, Gio, GObject

from .welcome import FlashcardsWelcome
from .decks import FlashcardsDecks


class Card(GObject.Object):
    __gtype_name__ = 'Card'

    front = GObject.Property(type=str)
    back = GObject.Property(type=str)

    def __init__(self, **kargs):
        super().__init__(**kargs)


class Deck(GObject.Object):
    __gtype_name__ = 'Deck'

    name = GObject.Property(type=str)
    cards_model = GObject.Property(type=Gio.ListStore)

    def __init__(self, **kargs):
        super().__init__(**kargs)

        self.name = _('New Deck')
        self.cards_model = Gio.ListStore.new(Card)


@Gtk.Template(resource_path='/io/github/fkinoshita/FlashCards/window.ui')
class FlashcardsWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'FlashcardsWindow'

    leaflet = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.decks_model = Gio.ListStore.new(Deck)
        self.current_deck = None

        self.welcome_page = FlashcardsWelcome()
        self.decks_page = FlashcardsDecks()

        self.decks_page.decks_list.bind_model(self.decks_model, self.__decks_list_create_row)

        self._setup_signals()

        self.leaflet.append(self.welcome_page)
        self.leaflet.append(self.decks_page)


    def _setup_signals(self):
        self.decks_model.connect('items-changed', lambda *_: self.decks_page.decks_list.bind_model(self.decks_model, self.__decks_list_create_row))

        self.welcome_page.start_button.connect('clicked', self.__on_start_button_clicked)
        self.decks_page.new_deck_button.connect('clicked', self.__on_new_deck_button_clicked)
        self.decks_page.new_card_button.connect('clicked', self.__on_new_card_button_clicked)


    def __on_start_button_clicked(self, button):
        if self.decks_model.props.n_items < 1:
            deck = Deck()

            self.current_deck = deck

            self.decks_model.append(deck)

            self.decks_page.edit_page_title.set_title(_('Create Deck'));

            self.leaflet.set_visible_child(self.decks_page)
            self.decks_page.leaflet.set_visible_child(self.decks_page.edit_page)
            self.decks_page.deck_name.connect('changed', self.__on_deck_name_changed)
            self.decks_page.deck_name.grab_focus()

            return

        self.leaflet.set_visible_child(self.decks_page)


    def __on_new_deck_button_clicked(self, button):
        deck = Deck()

        self.decks_model.append(deck)


    def __on_new_card_button_clicked(self, button):
        card = Card()
        card.front = _('Something')
        card.back = _('Something Else')

        self.current_deck.cards_model.append(card)


    def __decks_list_create_row(self, deck):
        if not self.decks_page.decks_list.has_css_class('boxed-list'):
            self.decks_page.decks_list.add_css_class('boxed-list')

        row = Adw.ActionRow()
        row.set_title(deck.name)
        row.set_activatable(True)

        suffix = Gtk.Box()
        suffix.set_spacing(12)
        suffix.set_valign(Gtk.Align.CENTER)

        edit_button = Gtk.Button()
        edit_button.set_icon_name('document-edit-symbolic')
        edit_button.add_css_class('circular')
        suffix.append(edit_button)

        edit_button.connect('clicked', self.__on_edit_deck_button_clicked, deck)

        icon = Gtk.Image.new_from_icon_name('go-next-symbolic')
        suffix.append(icon)

        row.add_suffix(suffix)

        row.connect('activated', self.__on_deck_activated)

        return row


    def __on_deck_activated(self, row):
        # go to cards page

        self.decks_page.leaflet.set_visible_child(self.decks_page.card_page)


    def __on_edit_deck_button_clicked(self, button, deck):
        # go to edit page

        self.current_deck = deck

        if self.current_deck.cards_model.props.n_items < 1:
            self.decks_page.cards_list.remove_css_class('boxed-list')

        self.decks_page.cards_list.bind_model(self.current_deck.cards_model, self.__cards_list_create_row)

        self.decks_page.edit_page_title.set_title(_('Edit Deck'));

        self.decks_page.deck_name.set_text(self.current_deck.name)
        self.decks_page.deck_name.connect('changed', self.__on_deck_name_changed)
        self.decks_page.deck_name.grab_focus()

        self.decks_page.leaflet.set_visible_child(self.decks_page.edit_page)


    def __on_deck_name_changed(self, entry):
        self.current_deck.name = entry.get_text()

        self.decks_model.emit('items-changed', 0, 0, 0)


    def __cards_list_create_row(self, card):
        if not self.decks_page.cards_list.has_css_class('boxed-list'):
            self.decks_page.cards_list.add_css_class('boxed-list')

        row = Adw.ActionRow()
        row.set_title(card.front)
        row.set_activatable(True)

        suffix = Gtk.Box()
        suffix.set_spacing(12)
        suffix.set_valign(Gtk.Align.CENTER)

        edit_button = Gtk.Button()
        edit_button.set_icon_name('document-edit-symbolic')
        edit_button.add_css_class('circular')
        suffix.append(edit_button)

        row.add_suffix(suffix)

        return row
    
