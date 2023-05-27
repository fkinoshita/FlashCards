moduledir = join_paths(DATA_DIR, 'flashcards')

conf = configuration_data()

conf.set('VERSION', version)
conf.set('APPID', application_id)
conf.set('GETTEXT_PACKAGE', meson.project_name())
conf.set('LOCALE_DIR', join_paths(get_option('prefix'), get_option('datadir'), 'locale'))
conf.set('NAME', project_name)
conf.set('PYTHON', python.find_installation('python3').path())
conf.set('DATA_DIR', DATA_DIR)
conf.set('APPID', application_id)

configure_file(
  input: 'flashcards.in',
  output: 'flashcards',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir'),
  install_mode: 'r-xr--r--'
)

flashcards_sources = [
  '__init__.py',
  'main.py',
  'window.py',
  'welcome.py',
  'list_view.py',
  'deck_view.py',
  'card_view.py',
  'card_edit_view.py',
  'deck_row.py',
  'card_row.py',
]

install_data(flashcards_sources, install_dir: moduledir)
