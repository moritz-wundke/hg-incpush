from setuptools import setup, find_packages

ENTRY_POINTS = """\
[console_scripts]
hg-incpush = hgincpush:main
"""

setup(
      name = 'hgincpush'
    , version = '1.0'
    , description = 'Mercurial incremental push helper'
    , author = 'Moritz Wundke'
    , license = 'MIT'
    , packages = find_packages()
    , zip_safe = False
    , entry_points = ENTRY_POINTS
)
