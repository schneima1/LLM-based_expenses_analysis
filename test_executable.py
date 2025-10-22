"""
Test script to verify the executable works correctly
Run this AFTER building the executable
"""

import subprocess
import sys
from pathlib import Path

def test_executable():
    """Test the built executable"""
    print("=" * 70)
    print("Testing Bank Transaction Analyzer Executable")
    print("=" * 70)
    print()
    
    exe_path = Path("release/BankTransactionAnalyzer.exe")
    
    # Check if executable exists
    if not exe_path.exists():
        print("❌ ERROR: Executable not found!")
        print(f"   Expected location: {exe_path.absolute()}")
        print()
        print("   Build the executable first:")
        print("   1. Run: build_executable.bat")
        print("   2. Then run this test script")
        return False
    
    print(f"✅ Executable found: {exe_path.absolute()}")
    print(f"   Size: {exe_path.stat().st_size / 1024 / 1024:.1f} MB")
    print()
    
    # Check if README exists
    readme_path = Path("release/README_USER.md")
    if readme_path.exists():
        print(f"✅ User README found: {readme_path.absolute()}")
    else:
        print(f"⚠️  User README missing: {readme_path.absolute()}")
    print()
    
    # Check Ollama
    print("Checking Ollama installation...")
    try:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            print("✅ Ollama is installed and running")
            print()
            print("Available models:")
            for line in result.stdout.split('\n')[:10]:  # Show first 10 lines
                if line.strip():
                    print(f"   {line}")
        else:
            print("⚠️  Ollama might not be installed or running")
            print("   Install from: https://ollama.com/download")
    except FileNotFoundError:
        print("❌ Ollama not found in PATH")
        print("   Install from: https://ollama.com/download")
    except Exception as e:
        print(f"⚠️  Could not check Ollama: {e}")
    
    print()
    print("=" * 70)
    print("Test Summary")
    print("=" * 70)
    print()
    print("Next steps:")
    print("1. ✅ Executable is built and ready")
    print("2. 📝 Test it manually:")
    print(f"      cd {exe_path.parent}")
    print(f"      .\\{exe_path.name}")
    print("3. 📦 Package for distribution:")
    print("      - Zip the 'release' folder")
    print("      - Include README_USER.md")
    print("      - Share with users")
    print()
    print("Users only need:")
    print("   • Windows 10/11")
    print("   • Ollama installed (https://ollama.com/download)")
    print("   • Downloaded AI model: ollama pull qwen3:4b-instruct-2507-q4_K_M")
    print()
    
    return True

if __name__ == "__main__":
    success = test_executable()
    sys.exit(0 if success else 1)
