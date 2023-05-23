project(
  'flashcards',
  version: '0.1.0',
  meson_version: '>= 0.62.0',
  license: 'GPL-3.0-or-later',
)

i18n = import('i18n')
python = import('python')
gnome = import('gnome')


project_id = 'io.github.fkinoshita.FlashCards'
project_name = 'FlashCards'
package_url = 'https://github.com/fkinoshita/FlashCards'
issue_url = 'https://github.com/fkinoshita/FlashCards/issues/new'
copyright = '© 2023 Felipe Kinoshita.'
contributors = '\n'.join([
  'Felipe Kinoshita https://fkinoshita.gitlab.io',
])
designers = '\n'.join([
  'Tobias Bernard https://tobiasbernard.com',
])
artists = '\n'.join([
  '',
])

dependency('gtk4', version: '>=4.9')
dependency('libadwaita-1', version: '>=1.2')

DATA_DIR = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())

application_id = project_id
version = meson.project_version()

top_source_dir = meson.current_source_dir()
gettext_package = meson.project_name()

subdir('data')
subdir('src')
subdir('po')

gnome.post_install(
  glib_compile_schemas: true,
  gtk_update_icon_cache: true,
  update_desktop_database: true,
)
