# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Adw, Gtk

@Gtk.Template(resource_path='/io/github/fkinoshita/FlashCards/ui/card_view.ui')
class CardView(Gtk.Box):
    __gtype_name__ = 'CardView'

    back_button = Gtk.Template.Child()
    card_box = Gtk.Template.Child()
    front_label = Gtk.Template.Child()
    back_label = Gtk.Template.Child()
    show_answer_button = Gtk.Template.Child()
    edit_button = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

