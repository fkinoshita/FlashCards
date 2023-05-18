/* flashcards-welcome.c
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

struct _FlashcardsWelcome
{
  GtkBox                parent_instance;

  /* Template widgets */
  GtkButton            *create_deck_button;
};

G_DEFINE_FINAL_TYPE (FlashcardsWelcome, flashcards_welcome, GTK_TYPE_BOX)

enum {
  START,
  N_SIGNALS,
};

static guint signals [N_SIGNALS] = {0, };

/* Callbacks */

static void
start (GtkButton         *button,
       FlashcardsWelcome *self)
{
  g_signal_emit (self, signals[START], 0);
}

/* Overrides */

static void
flashcards_welcome_class_init (FlashcardsWelcomeClass *klass)
{
  GtkWidgetClass *widget_class = GTK_WIDGET_CLASS (klass);

  signals[START] = g_signal_new ("start",
                                 FLASHCARDS_TYPE_WELCOME,
                                 G_SIGNAL_RUN_FIRST,
                                 0,
                                 NULL, NULL,
                                 g_cclosure_marshal_VOID__VOID,
                                 G_TYPE_NONE,
                                 0);

  gtk_widget_class_set_template_from_resource (widget_class, "/io/github/fkinoshita/FlashCards/flashcards-welcome.ui");
  gtk_widget_class_bind_template_child (widget_class, FlashcardsWelcome, create_deck_button);

  gtk_widget_class_bind_template_callback (widget_class, start);
}

static void
flashcards_welcome_init (FlashcardsWelcome *self)
{
  gtk_widget_init_template (GTK_WIDGET (self));
}

GtkWidget*
flashcards_welcome_new (void)
{
  return g_object_new (FLASHCARDS_TYPE_WELCOME, NULL);
}
