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

#include "flashcards-welcome.h"
#include "flashcards-decks.h"
#include "flashcards-window.h"

struct _FlashcardsWindow
{
  AdwApplicationWindow  parent_instance;

  /* Template widgets */
  AdwLeaflet           *leaflet;
  FlashcardsWelcome    *welcome;
  FlashcardsDecks      *decks;
};

G_DEFINE_FINAL_TYPE (FlashcardsWindow, flashcards_window, ADW_TYPE_APPLICATION_WINDOW)

/* Callbacks */

static void
on_start (FlashcardsWelcome *welcome,
          FlashcardsWindow  *self)
{
  adw_leaflet_navigate (self->leaflet, ADW_NAVIGATION_DIRECTION_FORWARD);
}

/* Overrides */

static void
flashcards_window_class_init (FlashcardsWindowClass *klass)
{
  GtkWidgetClass *widget_class = GTK_WIDGET_CLASS (klass);

  gtk_widget_class_set_template_from_resource (widget_class, "/io/github/fkinoshita/FlashCards/flashcards-window.ui");
  gtk_widget_class_bind_template_child (widget_class, FlashcardsWindow, leaflet);
  gtk_widget_class_bind_template_child (widget_class, FlashcardsWindow, welcome);
  gtk_widget_class_bind_template_child (widget_class, FlashcardsWindow, decks);

  gtk_widget_class_bind_template_callback (widget_class, on_start);
}

static void
flashcards_window_init (FlashcardsWindow *self)
{
  FlashcardsWelcome *welcome;
  FlashcardsDecks *decks;

  welcome = FLASHCARDS_WELCOME (flashcards_welcome_new ());
  decks = FLASHCARDS_DECKS (flashcards_decks_new ());

  gtk_widget_init_template (GTK_WIDGET (self));
}
