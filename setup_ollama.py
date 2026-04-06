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
    recommended_llm = 'gemma4:e4b'
    recommended_emb = 'nomic-embed-text-v2-moe'
    
    installed_models = parse_models(model_list_output)
    
    print("\nChecking recommended models...")
    print(f"Installed models: {', '.join(installed_models) if installed_models else 'None'}")
    print()
    
    # Check if the recommended models are installed
    llm_installed = any(recommended_llm in installed for installed in installed_models)
    emb_installed = any(recommended_emb in installed for installed in installed_models)
    
    missing_models = []
    
    if llm_installed:
        print(f"✅ {recommended_llm} - Installed")
    else:
        print(f"⚪ {recommended_llm} - Not installed")
        missing_models.append(recommended_llm)
        
    if emb_installed:
        print(f"✅ {recommended_emb} - Installed")
    else:
        print(f"⚪ {recommended_emb} - Not installed")
        missing_models.append(recommended_emb)
        
    return missing_models

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
    missing_models = check_models(models_output)
    
    # Recommend models if none found
    if missing_models:
        print()
        print(f"⚠️  Missing recommended models: {', '.join(missing_models)}")
        print()
        print("The app works best with these models.")
        print()
        
        for model in missing_models:
            response = input(f"Would you like to pull {model} now? (y/n): ").lower().strip()
            
            if response == 'y':
                if pull_model(model):
                    print(f"✅ Successfully pulled {model}")
                else:
                    print(f"❌ Failed to pull {model}. Please try manually: ollama pull {model}")
            else:
                print(f"To pull {model} manually, run: ollama pull {model}")
    else:
        print()
        print(f"✅ You have all recommended models installed.")
        print("You're ready to use the app!")
    
    print()
    print("=" * 60)
    print("Model Information:")
    print("-" * 60)
    print("• gemma4:e4b - Recommended for LLM classification")
    print("• nomic-embed-text-v2-moe - Recommended for Embedding classification")
    print()
    print("To pull models manually:")
    print("   ollama pull gemma4:e4b")
    print("   ollama pull nomic-embed-text-v2-moe")
    print()
    print("To see all available models:")
    print("   Visit: https://ollama.com/library")
    print("=" * 60)

if __name__ == "__main__":
    main()
