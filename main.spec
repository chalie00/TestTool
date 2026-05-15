# -*- mode: python ; coding: utf-8 -*-

import os
import sys

from PyInstaller.utils.hooks import collect_data_files


def find_vlc_dir():
    candidates = [
        os.path.join(os.environ.get('ProgramFiles', ''), 'VideoLAN', 'VLC'),
        os.path.join(os.environ.get('ProgramFiles(x86)', ''), 'VideoLAN', 'VLC'),
    ]
    for path in candidates:
        if path and os.path.exists(os.path.join(path, 'libvlc.dll')):
            return path
    return None


def find_tcl_tk_datas():
    base_dir = sys.base_prefix
    tcl_root = os.path.join(base_dir, 'tcl')
    data_specs = [
        ('_tcl_data', os.path.join(tcl_root, 'tcl8.6')),
        ('_tk_data', os.path.join(tcl_root, 'tk8.6')),
        ('tcl8', os.path.join(tcl_root, 'tcl8')),
    ]
    collected = []

    for dest, src in data_specs:
        if not os.path.isdir(src):
            continue

        for root, _, files in os.walk(src):
            rel_root = os.path.relpath(root, src)
            target_dir = dest if rel_root == '.' else os.path.join(dest, rel_root)
            for file_name in files:
                collected.append((os.path.join(root, file_name), target_dir))

    return collected


vlc_dir = find_vlc_dir()
vlc_binaries = []
vlc_datas = [('Capture\\\\', 'Capture'), ('Command\\\\', 'Command'), ('Design\\\\', 'Design'), ('Image\\\\', 'Image'), ('Log\\\\', 'Log')]
tcl_tk_datas = find_tcl_tk_datas()

if vlc_dir:
    vlc_binaries.extend([
        (os.path.join(vlc_dir, 'libvlc.dll'), '.'),
        (os.path.join(vlc_dir, 'libvlccore.dll'), '.'),
    ])
    vlc_datas.append((os.path.join(vlc_dir, 'plugins'), 'plugins'))

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=vlc_binaries,
    datas=vlc_datas + tcl_tk_datas + collect_data_files('ttkwidgets'),
    hiddenimports=['mss', 'requests', 'screeninfo', 'vlc', '_tkinter'],
    hookspath=['pyinstaller_hooks'],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='TestTool',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir='C:\\Temp',
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
