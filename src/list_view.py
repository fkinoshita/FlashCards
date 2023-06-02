# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Adw, Gtk

@Gtk.Template(resource_path='/io/github/fkinoshita/FlashCards/ui/list_view.ui')
class ListView(Gtk.Box):
    __gtype_name__ = 'ListView'

    delete_button = Gtk.Template.Child()
    selection_mode_button = Gtk.Template.Child()
    decks_list = Gtk.Template.Child()
    new_deck_button = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


    def set_selection_mode(self, active):
        if active:
            self.delete_button.set_visible(True)
            self.new_deck_button.set_visible(False)

            for row in self.decks_list.observe_children():
                row.edit_button.set_visible(False)
                row.next_icon.set_visible(False)
                row.revealer.set_reveal_child(True)

                if row.revealer.get_reveal_child():
                    row.revealer.set_margin_end(12)
        else:
            self.delete_button.set_visible(False)
            self.new_deck_button.set_visible(True)

            for row in self.decks_list.observe_children():
                row.edit_button.set_visible(True)
                row.next_icon.set_visible(True)
                row.revealer.set_reveal_child(False)

                if not row.revealer.get_reveal_child():
                    row.revealer.set_margin_end(0)

                row.checkbox.set_active(False)

