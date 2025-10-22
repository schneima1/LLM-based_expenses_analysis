# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for Bank Transaction Analyzer

Usage:
    pyinstaller app.spec

This creates a single executable file with all dependencies bundled.
"""

import sys
from pathlib import Path

block_cipher = None

# Get the site-packages directory
site_packages = Path(sys.prefix) / 'Lib' / 'site-packages'

a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=[],
    datas=[
        # Include Streamlit files
        (str(site_packages / 'streamlit' / 'runtime'), 'streamlit/runtime'),
        (str(site_packages / 'streamlit' / 'static'), 'streamlit/static'),
        (str(site_packages / 'altair' / 'vegalite'), 'altair/vegalite'),
    ],
    hiddenimports=[
        'streamlit',
        'streamlit.runtime.scriptrunner.magic_funcs',
        'streamlit.runtime.caching',
        'streamlit.runtime.state',
        'pandas',
        'numpy',
        'ollama',
        'pdfplumber',
        'PIL',
        'PIL.Image',
        'pytesseract',
        'altair',
        'pyarrow',
        'streamlit.components.v1',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'scipy',
        'IPython',
        'jupyter',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='BankTransactionAnalyzer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Set to False to hide console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Add path to .ico file if you have one
)
