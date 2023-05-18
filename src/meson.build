flashcards_sources = [
  'main.c',
  'flashcards-application.c',
  'flashcards-welcome.c',
  'flashcards-decks.c',
  'flashcards-window.c',
]

flashcards_deps = [
  dependency('gtk4'),
  dependency('libadwaita-1', version: '>= 1.2'),
]

flashcards_sources += gnome.compile_resources('flashcards-resources',
  'flashcards.gresource.xml',
  c_name: 'flashcards'
)

executable('flashcards', flashcards_sources,
  dependencies: flashcards_deps,
       install: true,
)
