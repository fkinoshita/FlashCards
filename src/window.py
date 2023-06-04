# SPDX-License-Identifier: GPL-3.0-or-later

import os
import json
import uuid

from gi.repository import Adw, Gtk, Gio, GObject

from .welcome import Welcome
from .list_view import ListView
from .deck_view import DeckView
from .card_view import CardView
from .card_edit_view import CardEditView
from .deck_row import DeckRow
from .card_row import CardRow

from . import shared

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

    def __init__(self, name = '', **kargs):
        super().__init__(**kargs)

        self.id = str(uuid.uuid4().hex)
        self.name = name
        self.icon = ''
        self.cards_model = Gio.ListStore.new(Card)
        self.current_index = 0


    def save(self):
        shared.decks_dir.mkdir(parents=True, exist_ok=True)

        cards = []

        for c in self.cards_model:
            card = {
                'front': c.front,
                'back': c.back,
            }
            cards.append(card)

        deck = {
            'id': self.id,
            'name': self.name,
            'icon': self.icon,
            'cards': cards
        }

        json.dump(
            deck,
            (shared.decks_dir / f"{self.id}.json").open("w"),
            indent=4,
            sort_keys=True,
        )


@Gtk.Template(resource_path='/io/github/fkinoshita/FlashCards/ui/window.ui')
class Window(Adw.ApplicationWindow):
    __gtype_name__ = 'Window'

    toast_overlay = Gtk.Template.Child()
    navigation_view = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.decks_model = Gio.ListStore.new(Deck)
        self.current_deck = None

        self._load_decks()

        self.welcome_page = Welcome()
        self.list_view = ListView()
        self.list_view.decks_list.bind_model(self.decks_model, self.__decks_list_create_row)
        self.deck_view = DeckView()
        self.card_view = CardView()

        self._setup_signals()

        if self.decks_model.props.n_items < 1:
            self.navigation_view.add(self.welcome_page)

        self.navigation_view.add(self.list_view)
        self.navigation_view.add(self.deck_view)
        self.navigation_view.add(self.card_view)


    def __decks_list_create_row(self, deck):
        if not self.list_view.decks_list.has_css_class('boxed-list'):
            self.list_view.decks_list.add_css_class('boxed-list')

        row = DeckRow(deck)
        row.edit_button.connect('clicked', self.__on_edit_deck_button_clicked, deck)
        row.connect('activated', self.__on_deck_activated, deck)
        row.checkbox.connect('toggled', self.__on_deck_checkbox_toggled, row)

        return row


    def cards_list_create_row(self, card):
        if not self.deck_view.cards_list.has_css_class('boxed-list'):
            self.deck_view.cards_list.add_css_class('boxed-list')

        self.deck_view.selection_mode_button.set_visible(True)

        row = CardRow(card)
        row.connect('activated', self.__on_edit_card_button_clicked, card)
        row.edit_button.connect('clicked', self.__on_edit_card_button_clicked, card)
        row.checkbox.connect('toggled', self.__on_card_checkbox_toggled, row)

        return row


    def __on_start_button_clicked(self, button):
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


    def __on_deck_activated(self, row, deck):
        self.current_deck = deck

        if not self.list_view.decks_list.get_selection_mode() == Gtk.SelectionMode.NONE:
            return

        if self.current_deck.cards_model.props.n_items == 0:
            self._go_to_deck(False)
            return

        self.card_view.front_label.set_label(self.current_deck.cards_model[self.current_deck.current_index].front)
        self.card_view.back_label.set_label(self.current_deck.cards_model[self.current_deck.current_index].back)

        self.navigation_view.push_by_tag("card_view")
        self.navigation_view.replace_with_tags(["list_view", "card_view"])


    def __on_edit_deck_button_clicked(self, button, deck):
        self.current_deck = deck
        self._go_to_deck(False)


    def __on_deck_checkbox_toggled(self, button, row):
        if button.get_active():
            self.list_view.decks_list.select_row(row)
            return

        self.list_view.decks_list.unselect_row(row)


    def __on_edit_card_button_clicked(self, _button, card):
        if not self.deck_view.cards_list.get_selection_mode() == Gtk.SelectionMode.NONE:
            return

        self._show_card_edit_dialog(card)


    def __on_card_checkbox_toggled(self, button, row):
        if button.get_active():
            self.deck_view.cards_list.select_row(row)
            return

        self.deck_view.cards_list.unselect_row(row)


    def __on_new_card_button_clicked(self, button):
        card = Card()
        card.front = ''
        card.back = ''

        self.current_deck.cards_model.append(card)
        self._show_card_edit_dialog(card)


    def __on_deck_name_changed(self, entry):
        self.current_deck.name = entry.get_text()
        self.current_deck.save()

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
                self.navigation_view.pop()
                return

            self.card_view.front_label.set_label(self.current_deck.cards_model[self.current_deck.current_index].front)
            self.card_view.back_label.set_label(self.current_deck.cards_model[self.current_deck.current_index].back)
        else:
            for child in self.card_view.card_box.observe_children():
                child.set_visible(True)

            button.set_label(_('Next'))

            if self.current_deck.current_index + 1 == self.current_deck.cards_model.props.n_items:
                button.set_label(_('Done'))


    def __on_card_edit_button_changed(self, button):
        self._go_to_deck(False)
        self._show_card_edit_dialog(self.current_deck.cards_model[self.current_deck.current_index])


    def __on_emoji_picked(self, emoji_chooser, emoji_text):
        self.current_deck.icon = emoji_text
        self.current_deck.save()
        self.deck_view.deck_icon.set_label(self.current_deck.icon)
        self.decks_model.emit('items-changed', 0, 0, 0)


    def __on_deck_selection_mode_button_clicked(self, button):
        if self.list_view.decks_list.get_selection_mode() == Gtk.SelectionMode.NONE:
            self.list_view.set_selection_mode(True)
            return

        self.list_view.set_selection_mode(False)


    def __on_deck_delete_button_clicked(self, button):
        for row in self.list_view.decks_list.get_selected_rows():
            found, position = self.decks_model.find(row.deck)
            if found:
                self.decks_model.remove(position)
                os.remove(shared.decks_dir / f"{row.deck.id}.json")

        self.list_view.set_selection_mode(False)

        if self.decks_model.props.n_items < 1:
            deck = Deck()
            self.current_deck = deck
            self._go_to_deck(True)
            self.decks_model.append(deck)


    def __on_card_selection_mode_button_clicked(self, button):
        if self.deck_view.cards_list.get_selection_mode() == Gtk.SelectionMode.NONE:
            self.deck_view.set_selection_mode(True)
            return

        self.deck_view.set_selection_mode(False)


    def __on_card_delete_button_clicked(self, button):
        for row in self.deck_view.cards_list.get_selected_rows():
            if row.get_name() == 'GtkBox':
                continue

            found, position = self.current_deck.cards_model.find(row.card)
            if found:
                self.current_deck.cards_model.remove(position)
                self.current_deck.save()

        self.deck_view.set_selection_mode(False)

        if self.current_deck.cards_model.props.n_items < 1:
            self.deck_view.selection_mode_button.set_visible(False)


    def _setup_signals(self):
        self.decks_model.connect('items-changed', lambda *_: self.list_view.decks_list.bind_model(self.decks_model, self.__decks_list_create_row))

        self.welcome_page.start_button.connect('clicked', self.__on_start_button_clicked)

        self.list_view.new_deck_button.connect('clicked', self.__on_new_deck_button_clicked)
        self.list_view.selection_mode_button.connect('clicked', self.__on_deck_selection_mode_button_clicked)
        self.list_view.delete_button.connect('clicked', self.__on_deck_delete_button_clicked)

        self.deck_view.new_card_button.connect('clicked', self.__on_new_card_button_clicked)
        self.deck_view.selection_mode_button.connect('clicked', self.__on_card_selection_mode_button_clicked)
        self.deck_view.delete_button.connect('clicked', self.__on_card_delete_button_clicked)

        self.card_view.show_answer_button.connect('clicked', self.__on_show_answer_button_clicked)
        self.card_view.edit_button.connect('clicked', self.__on_card_edit_button_changed)

        self.deck_view.emoji_chooser.connect('emoji-picked', self.__on_emoji_picked)


    def _load_decks(self):
        decks = []

        if shared.decks_dir.is_dir():
            for open_file in shared.decks_dir.iterdir():
                data = json.load(open_file.open())
                decks.append(data)

        for d in decks:
            deck = Deck(d['name'])
            deck.id = d['id']
            deck.icon = d['icon']

            for c in d['cards']:
                card = Card()
                card.front = c['front']
                card.back = c['back']

                deck.cards_model.append(card)

            self.decks_model.append(deck)


    def _go_to_deck(self, is_new: bool):
        self.navigation_view.push_by_tag("deck_view")
        self.navigation_view.replace_with_tags(["list_view", "deck_view"])

        if self.current_deck.cards_model.props.n_items < 1:
            self.deck_view.cards_list.remove_css_class('boxed-list')

        self.deck_view.cards_list.bind_model(self.current_deck.cards_model, self.cards_list_create_row)

        title = ''
        if is_new:
            title = _('New Deck')
        else:
            title = _('Edit Deck')

        self.deck_view.page_title.set_title(title);
        self.deck_view.name_entry.set_text(self.current_deck.name)
        self.deck_view.deck_icon.set_text(self.current_deck.icon)
        self.deck_view.name_entry.connect('changed', self.__on_deck_name_changed)

        if is_new:
            self.deck_view.name_entry.grab_focus()


    def _show_card_edit_dialog(self, card):
        dialog = Adw.Window(transient_for=self,
                            modal=True)
        dialog.set_size_request(300, 300)
        dialog.set_default_size(420, 420)

        trigger = Gtk.ShortcutTrigger.parse_string("Escape");
        close_action = Gtk.CallbackAction().new(lambda dialog, _: dialog.close())
        shortcut = Gtk.Shortcut().new(trigger, close_action)
        dialog.add_shortcut(shortcut)

        view = Adw.ToolbarView()

        top = Adw.HeaderBar()
        title = Adw.WindowTitle(title=_('Edit Card'))
        top.set_title_widget(title)
        view.add_top_bar(top)

        card_edit_view = CardEditView(self, card)
        view.set_content(card_edit_view)

        dialog.set_content(view)

        dialog.present()


