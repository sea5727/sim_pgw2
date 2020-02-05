import sys
from cx_Freeze import setup, Executable


include_files = [
    '/home/ysh8361/.pyenv/versions/3.7.5/envs/sim_pgw2/lib/python3.7/site-packages/cx_Freeze',
    '/home/ysh8361/.pyenv/versions/3.7.5/envs/sim_pgw2/lib/python3.7/site-packages/pyfiglet',
    '/home/ysh8361/.pyenv/versions/3.7.5/envs/sim_pgw2/lib/python3.7/site-packages/gi']
includes = ['pyfiglet', 'gi', 'cx_Freeze']
excludes = []
packages = []

setup(name="test",
      version="0.1",
      description="",
      options={'build_exe': {
          'namespace_packages': ['zope'],
          'excludes': excludes,
          'packages': packages,
          'includes': includes,
          'include_files': include_files,
          'path': sys.path + ['./build/exe.linux-x86_64-3.7/lib/pyfiglet', './build/exe.linux-x86_64-3.7/lib/gi',  './build/exe.linux-x86_64-3.7/lib/cx_Freeze']
      }},
      executables=[Executable("main.py", base='Console')])
