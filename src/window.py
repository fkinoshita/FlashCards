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

from .welcome import Welcome
from .list_view import ListView
from .deck_view import DeckView
from .card_view import CardView
# from .decks import FlashcardsDecks
from .card_edit_view import CardEditView

class Card(GObject.Object):
    __gtype_name__ = 'Card'

    front = GObject.Property(type=str)
    back = GObject.Property(type=str)

    def __init__(self, **kargs):
        super().__init__(**kargs)


class Deck(GObject.Object):
    __gtype_name__ = 'Deck'

    name = GObject.Property(type=str)
    icon = GObject.Property(type=str)
    cards_model = GObject.Property(type=Gio.ListStore)
    current_index = GObject.Property(type=int)

    def __init__(self, **kargs):
        super().__init__(**kargs)

        self.name = _('New Deck')
        self.icon = '🍕️'
        self.cards_model = Gio.ListStore.new(Card)
        self.current_index = 0


@Gtk.Template(resource_path='/io/github/fkinoshita/FlashCards/ui/window.ui')
class Window(Adw.ApplicationWindow):
    __gtype_name__ = 'Window'

    toast_overlay = Gtk.Template.Child()
    leaflet = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.decks_model = Gio.ListStore.new(Deck)
        self.current_deck = None

        self.welcome_page = Welcome()

        self.app_view = Gtk.Box()

        self.list_view = ListView()
        self.list_view.decks_list.bind_model(self.decks_model, self.__decks_list_create_row)
        self.deck_view = DeckView()
        self.card_view = CardView()

        leaflet = Adw.Leaflet()
        leaflet.set_can_unfold(False)

        leaflet.append(self.list_view)
        leaflet.append(self.deck_view)
        leaflet.append(self.card_view)

        leaflet.set_can_navigate_back(True)

        self.app_view.append(leaflet)

        self._setup_signals()

        self.leaflet.append(self.welcome_page)
        self.leaflet.append(self.app_view)


    def __decks_list_create_row(self, deck):
        if not self.list_view.decks_list.has_css_class('boxed-list'):
            self.list_view.decks_list.add_css_class('boxed-list')

        row = Adw.ActionRow()
        row.set_title_lines(1)
        row.set_title(deck.name)
        row.set_activatable(True)

        prefix = Gtk.Box()
        prefix.set_valign(Gtk.Align.CENTER)
        deck_icon = Gtk.Label(label=deck.icon)
        deck_icon.add_css_class('title-1')
        prefix.append(deck_icon)
        row.add_prefix(prefix)

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


    def cards_list_create_row(self, card):
        if not self.deck_view.cards_list.has_css_class('boxed-list'):
            self.deck_view.cards_list.add_css_class('boxed-list')

        row = Adw.ActionRow()
        row.set_title_lines(1)
        row.set_title(card.front)
        row.set_activatable(True)

        suffix = Gtk.Box()
        suffix.set_spacing(12)
        suffix.set_valign(Gtk.Align.CENTER)

        edit_button = Gtk.Button()
        edit_button.set_icon_name('document-edit-symbolic')
        edit_button.add_css_class('circular')
        suffix.append(edit_button)

        row.connect('activated', self.__on_edit_card_button_clicked, card)
        edit_button.connect('clicked', self.__on_edit_card_button_clicked, card)

        row.add_suffix(suffix)

        return row


    def __on_start_button_clicked(self, button):
        self.leaflet.set_visible_child(self.app_view)

        if self.decks_model.props.n_items < 1:
            deck = Deck()

            self.current_deck = deck
            self._go_to_deck(True)
            self.decks_model.append(deck)

            return


    def __on_new_deck_button_clicked(self, button):
        deck = Deck()
        self.current_deck = deck
        self._go_to_deck(True)
        self.decks_model.append(deck)


    def __on_deck_activated(self, row):
        if self.current_deck.cards_model.props.n_items == 0:
            self._go_to_deck(False)
            return

        self.card_view.front_label.set_label(self.current_deck.cards_model[self.current_deck.current_index].front)
        self.card_view.back_label.set_label(self.current_deck.cards_model[self.current_deck.current_index].back)

        self.app_view.get_first_child().reorder_child_after(self.deck_view, self.card_view)
        self.app_view.get_first_child().set_visible_child(self.card_view)


    def __on_edit_deck_button_clicked(self, button, deck):
        self.current_deck = deck
        self._go_to_deck(False)


    def __on_edit_card_button_clicked(self, _button, card):
        self._show_card_edit_dialog(card)


    def __on_new_card_button_clicked(self, button):
        card = Card()
        card.front = _('')
        card.back = _('')

        self.current_deck.cards_model.append(card)
        self._show_card_edit_dialog(card)


    def __on_deck_name_changed(self, entry):
        self.current_deck.name = entry.get_text()

        self.decks_model.emit('items-changed', 0, 0, 0)


    def __on_show_answer_button_clicked(self, button):
        if button.get_label() == _('Next') or button.get_label() == _('Done'):
            self.current_deck.current_index += 1

            button.set_label(_('Show Answer'))

            for child in self.card_view.card_box.observe_children():
                child.set_visible(False)

            self.card_view.front_label.set_visible(True)

            if self.current_deck.current_index + 1 > self.current_deck.cards_model.props.n_items:
                self.current_deck.current_index = 0
                self.app_view.get_first_child().set_visible_child(self.list_view)
                return

            self.card_view.front_label.set_label(self.current_deck.cards_model[self.current_deck.current_index].front)
            self.card_view.back_label.set_label(self.current_deck.cards_model[self.current_deck.current_index].back)
        else:
            for child in self.card_view.card_box.observe_children():
                child.set_visible(True)

            button.set_label(_('Next'))

            if self.current_deck.current_index + 1 == self.current_deck.cards_model.props.n_items:
                button.set_label(_('Done'))


    def __on_back_button(self, button):
        self.app_view.get_first_child().set_visible_child(self.list_view)


    def __on_emoji_picked(self, emoji_chooser, emoji_text):
        self.current_deck.icon = emoji_text
        self.deck_view.deck_icon.set_label(self.current_deck.icon)
        self.decks_model.emit('items-changed', 0, 0, 0)


    def _setup_signals(self):
        self.decks_model.connect('items-changed', lambda *_: self.list_view.decks_list.bind_model(self.decks_model, self.__decks_list_create_row))

        self.welcome_page.start_button.connect('clicked', self.__on_start_button_clicked)
        self.list_view.new_deck_button.connect('clicked', self.__on_new_deck_button_clicked)
        self.deck_view.new_card_button.connect('clicked', self.__on_new_card_button_clicked)
        self.card_view.show_answer_button.connect('clicked', self.__on_show_answer_button_clicked)

        self.deck_view.back_button.connect('clicked', self.__on_back_button)
        self.card_view.back_button.connect('clicked', self.__on_back_button)

        self.deck_view.emoji_chooser.connect('emoji-picked', self.__on_emoji_picked)


    def _go_to_deck(self, is_new: bool):
        if self.current_deck.cards_model.props.n_items < 1:
            self.deck_view.cards_list.remove_css_class('boxed-list')

        self.deck_view.cards_list.bind_model(self.current_deck.cards_model, self.cards_list_create_row)

        title = ''
        if is_new:
            title = _('Create Deck')
        else:
            title = _('Edit Deck')

        self.deck_view.page_title.set_title(title);
        self.deck_view.name_entry.set_text(self.current_deck.name)
        self.deck_view.deck_icon.set_text(self.current_deck.icon)
        self.deck_view.name_entry.connect('changed', self.__on_deck_name_changed)

        if is_new:
            self.deck_view.name_entry.grab_focus()

        self.app_view.get_first_child().reorder_child_after(self.card_view, self.deck_view)
        self.app_view.get_first_child().set_visible_child(self.deck_view)


    def _show_card_edit_dialog(self, card):
        dialog = Adw.Window(transient_for=self,
                            modal=True)
        dialog.set_size_request(420, 420)

        view = Adw.ToolbarView()

        top = Adw.HeaderBar()
        title = Adw.WindowTitle(title=_('Edit Card'))
        top.set_title_widget(title)
        view.add_top_bar(top)

        card_edit_view = CardEditView(self, card)
        view.set_content(card_edit_view)

        dialog.set_content(view)

        dialog.present()


