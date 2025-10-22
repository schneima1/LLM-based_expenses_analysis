"""
Installation Test Script

Run this script to verify all dependencies are installed correctly
and the app is ready to run.
"""

import sys
from typing import Tuple

def test_import(module_name: str, package_name: str = None) -> Tuple[bool, str]:
    """Test if a module can be imported."""
    if package_name is None:
        package_name = module_name
    
    try:
        __import__(module_name)
        return True, f"✅ {package_name}"
    except ImportError as e:
        return False, f"❌ {package_name} - {str(e)}"

def main():
    print("=" * 60)
    print("Bank Transaction Analyzer - Installation Test")
    print("=" * 60)
    print()
    
    # Test core dependencies
    print("Testing Core Dependencies:")
    print("-" * 60)
    
    core_tests = [
        ("streamlit", "Streamlit"),
        ("pandas", "Pandas"),
        ("numpy", "NumPy"),
        ("ollama", "Ollama"),
    ]
    
    core_results = [test_import(mod, name) for mod, name in core_tests]
    for success, msg in core_results:
        print(msg)
    
    print()
    
    # Test PDF dependencies
    print("Testing PDF Processing Dependencies:")
    print("-" * 60)
    
    pdf_tests = [
        ("pdfplumber", "PDFPlumber"),
        ("PyPDF2", "PyPDF2"),
    ]
    
    pdf_results = [test_import(mod, name) for mod, name in pdf_tests]
    for success, msg in pdf_results:
        print(msg)
    
    print()
    
    # Test optional dependencies
    print("Testing Optional Dependencies:")
    print("-" * 60)
    
    optional_tests = [
        ("PIL", "Pillow (PIL)"),
        ("pytesseract", "Pytesseract"),
        ("camelot", "Camelot"),
    ]
    
    optional_results = [test_import(mod, name) for mod, name in optional_tests]
    for success, msg in optional_results:
        print(msg)
    
    print()
    
    # Check Ollama connection
    print("Testing Ollama Connection:")
    print("-" * 60)
    
    try:
        import ollama
        models = ollama.list()
        model_names = [m.get('name', 'unknown') for m in models.get('models', [])]
        
        if model_names:
            print(f"✅ Ollama is running")
            print(f"   Available models: {', '.join(model_names)}")
        else:
            print("⚠️  Ollama is running but no models found")
            print("   Run: ollama pull qwen3")
    except Exception as e:
        print(f"❌ Ollama connection failed: {e}")
        print("   Make sure Ollama is installed and running")
        print("   Visit: https://ollama.com")
    
    print()
    
    # Summary
    print("=" * 60)
    print("Summary:")
    print("-" * 60)
    
    all_core_passed = all(success for success, _ in core_results)
    all_pdf_passed = all(success for success, _ in pdf_results)
    any_optional = any(success for success, _ in optional_results)
    
    if all_core_passed:
        print("✅ All core dependencies installed - App is ready to run!")
        print()
        print("To start the app, run:")
        print("   streamlit run app.py")
    else:
        print("❌ Some core dependencies are missing")
        print()
        print("To install missing dependencies, run:")
        print("   pip install -r requirements.txt")
    
    print()
    
    if not all_pdf_passed:
        print("⚠️  Some PDF processing libraries are missing")
        print("   PDF functionality may be limited")
    
    if not any_optional:
        print("⚠️  Optional dependencies not installed")
        print("   OCR and advanced PDF processing will not work")
        print("   To install: pip install pytesseract camelot-py[cv]")
    
    print()
    print("=" * 60)
    
    # Python version check
    print()
    print("Python Information:")
    print("-" * 60)
    print(f"Python Version: {sys.version}")
    print(f"Python Executable: {sys.executable}")
    
    if sys.version_info < (3, 8):
        print()
        print("⚠️  Warning: Python 3.8 or higher is recommended")

if __name__ == "__main__":
    main()
