# -*- mode: python -*-
a = Analysis(['hgincpush\\__init__.py'],
             pathex=['F:\\Projects\\GitHub\\hg-incpush'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='hg-incpush.exe',
          debug=False,
          strip=None,
          upx=True,
          console=True , icon='icon.ico')
