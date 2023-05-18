/* flashcards-window.c
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

#include "flashcards-window.h"

struct _FlashcardsWindow
{
  AdwApplicationWindow  parent_instance;

  /* Template widgets */
  GtkStack             *main_stack;
  AdwLeaflet           *leaflet;

  GtkButton            *create_deck_button;
};

G_DEFINE_FINAL_TYPE (FlashcardsWindow, flashcards_window, ADW_TYPE_APPLICATION_WINDOW)

/* Callbacks */

static void
start (GtkButton *button,
            gpointer   user_data)
{
  FlashcardsWindow *window;

  window = FLASHCARDS_WINDOW (user_data);

  gtk_stack_set_visible_child_name (window->main_stack, "decks-view");
}

static void
show_deck_creation (GtkButton *button,
                    gpointer   user_data)
{
  FlashcardsWindow *window;

  window = FLASHCARDS_WINDOW (user_data);

  adw_leaflet_navigate (window->leaflet, ADW_NAVIGATION_DIRECTION_FORWARD);
}

static void
show_decks (GtkButton *button,
            gpointer   user_data)
{
  FlashcardsWindow *window;

  window = FLASHCARDS_WINDOW (user_data);

  adw_leaflet_navigate (window->leaflet, ADW_NAVIGATION_DIRECTION_BACK);
}

/* Overrides */

static void
flashcards_window_class_init (FlashcardsWindowClass *klass)
{
  GtkWidgetClass *widget_class = GTK_WIDGET_CLASS (klass);

  gtk_widget_class_set_template_from_resource (widget_class, "/io/github/fkinoshita/FlashCards/flashcards-window.ui");
  gtk_widget_class_bind_template_child (widget_class, FlashcardsWindow, main_stack);
  gtk_widget_class_bind_template_child (widget_class, FlashcardsWindow, leaflet);

  gtk_widget_class_bind_template_child (widget_class, FlashcardsWindow, create_deck_button);

  gtk_widget_class_bind_template_callback (widget_class, start);
  gtk_widget_class_bind_template_callback (widget_class, show_decks);
  gtk_widget_class_bind_template_callback (widget_class, show_deck_creation);
}

static void
flashcards_window_init (FlashcardsWindow *self)
{
  gtk_widget_init_template (GTK_WIDGET (self));
}
