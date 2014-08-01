# hg-incpush

Simple python script used for simple incremental pushes when using mercurial. This can be helpful when a single push gets too large and produces 400 Bad Request errors.

## Usage

```
$> hg-incpush --help
usage: __init__.py [-h] [-v] [-s S] [-f F] -p PATH [-d]

Mercurlial incremental push helper (1.0). By Moritz Wundke

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -s S                  Maximum size in MB a bucket can hold
  -f F                  Number of max file a bucket can hold
  -p PATH, --path PATH  Path to the mercurial clone
  -d, --dry             Perform a dryrun printing into the log the content of
                        the possible buckets
```
## Install

To be able to use this utility on a machine that features python 2.7+ you can proceed with the standart python package installation.

```
python setup.py install
```

The installartion process installs the package and a script entry point ```hg-incpush```

## Standalone (Windows)

If python is not present in the target machine a simple standalone executable can be build using PyInstaller, the required files are alerady provided for the purpose. To create your standalone executable just install the [PyInstaller package][PyInstaller], execute the ```config.bat``` file and then the ```build.bat``` file. Once the process has finished you will find the standlone exe within the dist folder.


[PyInstaller]: http://example.com/
