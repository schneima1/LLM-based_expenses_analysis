# -*- mode: python ; coding: utf-8 -*-
"""
Simplified PyInstaller spec for Bank Transaction Analyzer
Builds a standalone executable with minimal dependencies

Usage:
    pyinstaller build_simple.spec

Creates: dist/BankTransactionAnalyzer.exe
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
        # Include Streamlit runtime files
        (str(site_packages / 'streamlit' / 'runtime'), 'streamlit/runtime'),
        (str(site_packages / 'streamlit' / 'static'), 'streamlit/static'),
        (str(site_packages / 'altair' / 'vegalite'), 'altair/vegalite'),
    ],
    hiddenimports=[
        # Core dependencies
        'streamlit',
        'streamlit.runtime.scriptrunner.magic_funcs',
        'streamlit.runtime.caching',
        'streamlit.runtime.state',
        'streamlit.components.v1',
        'pandas',
        'numpy',
        'ollama',
        'pdfplumber',
        'PIL',
        'PIL.Image',
        'altair',
        'pyarrow',
        'pyarrow.parquet',
        # Date/time handling
        'dateutil',
        'dateutil.parser',
        # JSON handling
        'json',
        're',
        'io',
        'pathlib',
        'tempfile',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Exclude optional OCR/PDF dependencies
        'pytesseract',
        'pdf2image',
        'camelot',
        # Exclude heavy unused libraries
        'matplotlib',
        'scipy',
        'pytest',
        'jupyter',
        'notebook',
        'ipython',
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
    upx=True,  # Compress executable
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Show console for Streamlit output
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Add your icon file here if you have one
)
