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
  GtkButton            *new_deck_button;
};

G_DEFINE_FINAL_TYPE (FlashcardsDecks, flashcards_decks, GTK_TYPE_BOX)

enum {
  NEW,
  N_SIGNALS,
};

static guint signals [N_SIGNALS] = {0, };

/* Callbacks */

static void
on_new_deck (GtkButton         *button,
             FlashcardsDecks *self)
{
  g_signal_emit (self, signals[NEW], 0);
}

/* Overrides */

static void
flashcards_decks_class_init (FlashcardsDecksClass *klass)
{
  GtkWidgetClass *widget_class = GTK_WIDGET_CLASS (klass);

  signals[NEW] = g_signal_new ("new_deck",
                               FLASHCARDS_TYPE_DECKS,
                               G_SIGNAL_RUN_FIRST,
                               0,
                               NULL, NULL,
                               g_cclosure_marshal_VOID__VOID,
                               G_TYPE_NONE,
                               0);

  gtk_widget_class_set_template_from_resource (widget_class, "/io/github/fkinoshita/FlashCards/flashcards-decks.ui");
  gtk_widget_class_bind_template_child (widget_class, FlashcardsDecks, new_deck_button);

  gtk_widget_class_bind_template_callback (widget_class, on_new_deck);
}

static void
flashcards_decks_init (FlashcardsDecks *self)
{
  gtk_widget_init_template (GTK_WIDGET (self));
}

GtkWidget*
flashcards_decks_new (void)
{
  return g_object_new (FLASHCARDS_TYPE_DECKS, NULL);
}

