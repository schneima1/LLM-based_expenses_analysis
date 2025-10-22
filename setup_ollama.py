"""
Ollama Setup Helper

This script helps you set up Ollama for the Bank Transaction Analyzer.
It checks if Ollama is installed, running, and has the required models.
"""

import subprocess
import sys
import time

def run_command(command):
    """Run a shell command and return the output."""
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=10
        )
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def check_ollama_installed():
    """Check if Ollama is installed."""
    print("Checking Ollama installation...")
    success, stdout, stderr = run_command("ollama --version")
    
    if success:
        print(f"✅ Ollama is installed: {stdout.strip()}")
        return True
    else:
        print("❌ Ollama is not installed")
        print()
        print("📥 Download Ollama from: https://ollama.com/download")
        print()
        return False

def check_ollama_running():
    """Check if Ollama service is running."""
    print("\nChecking if Ollama is running...")
    success, stdout, stderr = run_command("ollama list")
    
    if success:
        print("✅ Ollama is running")
        return True, stdout
    else:
        print("❌ Ollama is not running")
        print()
        print("To start Ollama:")
        print("  Windows: Ollama should auto-start, or run 'ollama serve'")
        print("  Linux/Mac: Run 'ollama serve' in a separate terminal")
        print()
        return False, ""

def parse_models(ollama_list_output):
    """Parse the output of 'ollama list' to get model names."""
    models = []
    lines = ollama_list_output.strip().split('\n')
    
    # Skip header line
    for line in lines[1:]:
        if line.strip():
            parts = line.split()
            if parts:
                models.append(parts[0])
    
    return models

def check_models(model_list_output):
    """Check which recommended models are installed."""
    recommended_model = 'qwen3:4b-instruct-2507-q4_K_M'
    
    installed_models = parse_models(model_list_output)
    
    print("\nChecking recommended model...")
    print(f"Installed models: {', '.join(installed_models) if installed_models else 'None'}")
    print()
    
    # Check if the recommended model is installed
    is_installed = any(recommended_model in installed or 'qwen3' in installed.lower() for installed in installed_models)
    
    if is_installed:
        print(f"✅ {recommended_model} (or qwen3 variant) - Installed")
        return [recommended_model]
    else:
        print(f"⚪ {recommended_model} - Not installed")
        return []

def pull_model(model_name):
    """Pull a model from Ollama."""
    print(f"\n📥 Pulling {model_name}...")
    print("This may take a few minutes depending on your internet connection.")
    print()
    
    success, stdout, stderr = run_command(f"ollama pull {model_name}")
    
    if success:
        print(f"✅ Successfully pulled {model_name}")
        return True
    else:
        print(f"❌ Failed to pull {model_name}")
        print(f"Error: {stderr}")
        return False

def main():
    print("=" * 60)
    print("Ollama Setup Helper for Bank Transaction Analyzer")
    print("=" * 60)
    print()
    
    # Check installation
    if not check_ollama_installed():
        sys.exit(1)
    
    # Check if running
    is_running, models_output = check_ollama_running()
    if not is_running:
        print("\n⚠️  Please start Ollama first, then run this script again.")
        sys.exit(1)
    
    # Check models
    found_models = check_models(models_output)
    
    # Recommend model if none found
    if not found_models:
        print()
        print("⚠️  Recommended model not found.")
        print()
        print("The app needs the qwen3:4b-instruct-2507-q4_K_M model to work.")
        print()
        
        response = input("Would you like to pull qwen3:4b-instruct-2507-q4_K_M now? (y/n): ").lower().strip()
        
        if response == 'y':
            if pull_model('qwen3:4b-instruct-2507-q4_K_M'):
                print()
                print("✅ Setup complete! You can now use the app.")
            else:
                print()
                print("❌ Setup failed. Please try manually:")
                print("   ollama pull qwen3:4b-instruct-2507-q4_K_M")
        else:
            print()
            print("To pull the model manually, run:")
            print("   ollama pull qwen3:4b-instruct-2507-q4_K_M")
    else:
        print()
        print(f"✅ You have the recommended model installed.")
        print("You're ready to use the app!")
    
    print()
    print("=" * 60)
    print("Model Information:")
    print("-" * 60)
    print("• qwen3:4b-instruct-2507-q4_K_M - Required for the app")
    print("  Fast, accurate, optimized for German text")
    print()
    print("To pull the model:")
    print("   ollama pull qwen3:4b-instruct-2507-q4_K_M")
    print()
    print("To see all available models:")
    print("   Visit: https://ollama.com/library")
    print("=" * 60)

if __name__ == "__main__":
    main()
