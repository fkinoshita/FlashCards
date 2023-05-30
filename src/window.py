# SPDX-License-Identifier: GPL-3.0-or-later

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
    leaflet = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.decks_model = Gio.ListStore.new(Deck)
        self.current_deck = None

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

        if self.decks_model.props.n_items < 1:
            self.leaflet.append(self.welcome_page)

        self.leaflet.append(self.app_view)


    def __decks_list_create_row(self, deck):
        if not self.list_view.decks_list.has_css_class('boxed-list'):
            self.list_view.decks_list.add_css_class('boxed-list')

        row = DeckRow(deck)
        row.edit_button.connect('clicked', self.__on_edit_deck_button_clicked, deck)
        row.connect('activated', self.__on_deck_activated, deck)

        return row


    def cards_list_create_row(self, card):
        if not self.deck_view.cards_list.has_css_class('boxed-list'):
            self.deck_view.cards_list.add_css_class('boxed-list')

        row = CardRow(card)
        row.connect('activated', self.__on_edit_card_button_clicked, card)
        row.edit_button.connect('clicked', self.__on_edit_card_button_clicked, card)

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


    def __on_card_edit_button_changed(self, button):
        self._go_to_deck(False)
        self._show_card_edit_dialog(self.current_deck.cards_model[self.current_deck.current_index])


    def __on_back_button(self, button):
        self.app_view.get_first_child().set_visible_child(self.list_view)


    def __on_emoji_picked(self, emoji_chooser, emoji_text):
        self.current_deck.icon = emoji_text
        self.current_deck.save()
        self.deck_view.deck_icon.set_label(self.current_deck.icon)
        self.decks_model.emit('items-changed', 0, 0, 0)


    def _setup_signals(self):
        self.decks_model.connect('items-changed', lambda *_: self.list_view.decks_list.bind_model(self.decks_model, self.__decks_list_create_row))

        self.welcome_page.start_button.connect('clicked', self.__on_start_button_clicked)
        self.list_view.new_deck_button.connect('clicked', self.__on_new_deck_button_clicked)
        self.deck_view.new_card_button.connect('clicked', self.__on_new_card_button_clicked)
        self.card_view.show_answer_button.connect('clicked', self.__on_show_answer_button_clicked)
        self.card_view.edit_button.connect('clicked', self.__on_card_edit_button_changed)

        self.deck_view.back_button.connect('clicked', self.__on_back_button)
        self.card_view.back_button.connect('clicked', self.__on_back_button)

        self.deck_view.emoji_chooser.connect('emoji-picked', self.__on_emoji_picked)


    def _go_to_deck(self, is_new: bool):
        self.leaflet.set_visible_child(self.app_view)

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
        dialog.set_size_request(300, 300)
        dialog.set_default_size(420, 420)

        view = Adw.ToolbarView()

        top = Adw.HeaderBar()
        title = Adw.WindowTitle(title=_('Edit Card'))
        top.set_title_widget(title)
        view.add_top_bar(top)

        card_edit_view = CardEditView(self, card)
        view.set_content(card_edit_view)

        dialog.set_content(view)

        dialog.present()


