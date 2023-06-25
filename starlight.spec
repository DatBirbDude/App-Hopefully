# -*- mode: python ; coding: utf-8 -*-

block_cipher = None
from kivy.tools.packaging.pyinstaller_hooks import get_deps_all, hookspath, runtime_hooks
#from kivy_deps import sdl2, glew

a = Analysis(['C:\\Users\\Samuel\\PycharmProjects\\App-Hopefully\\main.py'],
    pathex=[],
    #binaries=None,
    hookspath=hookspath(),
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    runtime_hooks=runtime_hooks(),
    **get_deps_all())
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    exclude_binaries=True,
    name='starlight',
    debug=False,
    strip=False,
    upx=True,
    console=False,
)
coll = COLLECT(exe, Tree('C:\\Users\\Samuel\\PycharmProjects\\App-Hopefully'),
               Tree('/Library/Frameworks/SDL2_ttf.framework/Versions/A/Frameworks/FreeType.framework'),
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='starlight')
app = BUNDLE(coll,
             name="starlight.app",
             icon=None,
         bundle_identifier=None)
