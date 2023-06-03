# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Adw, Gtk

@Gtk.Template(resource_path='/io/github/fkinoshita/FlashCards/ui/deck_view.ui')
class DeckView(Gtk.Box):
    __gtype_name__ = 'DeckView'

    back_button = Gtk.Template.Child()
    delete_button = Gtk.Template.Child()
    cancel_button = Gtk.Template.Child()
    selection_mode_button = Gtk.Template.Child()
    menu_button = Gtk.Template.Child()

    deck_icon = Gtk.Template.Child()
    edit_icon_button = Gtk.Template.Child()
    emoji_chooser = Gtk.Template.Child()
    page_title = Gtk.Template.Child()
    name_entry = Gtk.Template.Child()
    cards_list = Gtk.Template.Child()
    new_card_button = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.cards_list.connect('selected-rows-changed', self.__cards_selected_rows_changed)
        self.cancel_button.connect('clicked', lambda *_: self.set_selection_mode(False))


    def __cards_selected_rows_changed(self, list):
        if len(list.get_selected_rows()) <= 0:
            self.delete_button.set_sensitive(False)
        else:
            self.delete_button.set_sensitive(True)


    def set_selection_mode(self, active):
        if active:
            self.cards_list.set_selection_mode(Gtk.SelectionMode.MULTIPLE)

            self.cancel_button.set_visible(True)
            self.delete_button.set_visible(True)
            self.new_card_button.set_visible(False)
            self.selection_mode_button.set_visible(False)
            self.menu_button.set_visible(False)

            for row in self.cards_list.observe_children():
                if row.get_name() == 'GtkBox':
                    continue

                row.edit_button.set_visible(False)
                row.revealer.set_reveal_child(True)

                if row.revealer.get_reveal_child():
                    row.revealer.set_margin_end(12)

            self.cards_list.get_first_child().checkbox.set_active(True)
        else:
            self.cards_list.set_selection_mode(Gtk.SelectionMode.NONE)

            self.cancel_button.set_visible(False)
            self.delete_button.set_visible(False)
            self.new_card_button.set_visible(True)
            self.selection_mode_button.set_visible(True)
            self.menu_button.set_visible(True)

            for row in self.cards_list.observe_children():
                if row.get_name() == 'GtkBox':
                    continue

                row.edit_button.set_visible(True)
                row.revealer.set_reveal_child(False)

                if not row.revealer.get_reveal_child():
                    row.revealer.set_margin_end(0)

                row.checkbox.set_active(False)

