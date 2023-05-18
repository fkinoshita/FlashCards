/* flashcards-decks.c
 *
 * Copyright 2023 Felipe Kinoshita
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#include "config.h"

#include "flashcards-decks.h"

struct _FlashcardsDecks
{
  GtkBox                parent_instance;

  /* Template widgets */
  AdwLeaflet           *leaflet;
  GtkListBox           *decks;
  GtkButton            *new_deck_button;

  GtkBox               *list;
  GtkBox               *cards;
};

G_DEFINE_FINAL_TYPE (FlashcardsDecks, flashcards_decks, GTK_TYPE_BOX)

/* Callbacks */

static void
on_new_deck (GtkButton         *button,
             FlashcardsDecks   *self)
{
  adw_leaflet_navigate (self->leaflet, ADW_NAVIGATION_DIRECTION_FORWARD);
}

static void
on_row_activated (GtkButton       *button,
                  FlashcardsDecks *self)
{
  adw_leaflet_set_visible_child (self->leaflet, GTK_WIDGET (self->cards));
}

static void
on_row_edit (GtkButton       *button,
             FlashcardsDecks *self)
{
  adw_leaflet_navigate (self->leaflet, ADW_NAVIGATION_DIRECTION_FORWARD);
}

static void
go_back (GtkButton       *button,
         FlashcardsDecks *self)
{
  adw_leaflet_set_visible_child (self->leaflet, GTK_WIDGET (self->list));
  /* adw_leaflet_navigate (self->leaflet, ADW_NAVIGATION_DIRECTION_BACK); */
}

/* Overrides */

static void
flashcards_decks_class_init (FlashcardsDecksClass *klass)
{
  GtkWidgetClass *widget_class = GTK_WIDGET_CLASS (klass);

  gtk_widget_class_set_template_from_resource (widget_class, "/io/github/fkinoshita/FlashCards/flashcards-decks.ui");
  gtk_widget_class_bind_template_child (widget_class, FlashcardsDecks, leaflet);
  gtk_widget_class_bind_template_child (widget_class, FlashcardsDecks, new_deck_button);
  gtk_widget_class_bind_template_child (widget_class, FlashcardsDecks, decks);

  gtk_widget_class_bind_template_child (widget_class, FlashcardsDecks, list);
  gtk_widget_class_bind_template_child (widget_class, FlashcardsDecks, cards);

  gtk_widget_class_bind_template_callback (widget_class, on_new_deck);
  gtk_widget_class_bind_template_callback (widget_class, go_back);
}

static void
flashcards_decks_init (FlashcardsDecks *self)
{
  gtk_widget_init_template (GTK_WIDGET (self));

  for (int i = 0; i < 4; i++) {
    AdwActionRow *row;
    GtkImage *icon;
    GtkButton *button;
    GtkButton *edit_button;

    row = ADW_ACTION_ROW (adw_action_row_new ());
    icon = GTK_IMAGE (gtk_image_new_from_icon_name ("go-next-symbolic"));
    button = GTK_BUTTON (gtk_button_new ());
    edit_button = GTK_BUTTON ( gtk_button_new_from_icon_name ("document-edit-symbolic"));

    adw_preferences_row_set_title (ADW_PREFERENCES_ROW (row), "Espanol");

    gtk_widget_add_css_class (GTK_WIDGET (edit_button), "flat");
    gtk_widget_add_css_class (GTK_WIDGET (edit_button), "circular");
    gtk_widget_set_size_request (GTK_WIDGET (edit_button), 50, 32);
    adw_action_row_add_suffix (row, GTK_WIDGET (edit_button));

    adw_action_row_add_suffix (row, GTK_WIDGET (icon));

    adw_action_row_set_activatable_widget (row, GTK_WIDGET (button));

    g_signal_connect (edit_button, "clicked", G_CALLBACK (on_row_edit), self);
    g_signal_connect (row, "activated", G_CALLBACK (on_row_activated), self);

    gtk_list_box_append (self->decks, GTK_WIDGET (row));
  }
}

GtkWidget*
flashcards_decks_new (void)
{
  return g_object_new (FLASHCARDS_TYPE_DECKS, NULL);
}

