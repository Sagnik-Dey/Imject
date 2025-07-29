from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
build_options = {'packages': ["app"], 'excludes': [], "include_files":["app/", "assets/", "databases/", "styles/", "resources/"]}

base = 'gui'

executables = [
    Executable('main.py', base=base, target_name = 'imject', icon="assets/icons/logo.ico")
]

setup(name='Imject',
      version = '1.0',
      description = 'Imject',
      options = {'build_exe': build_options},
      executables = executables)
