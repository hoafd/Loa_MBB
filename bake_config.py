import os
from config_utils import ConfigManager

def main():
    print("[PRE-BUILD] Baking configuration for standalone build...")
    manager = ConfigManager()
    
    if not os.path.exists(".env"):
        print("[!] Error: No .env file found to bake.")
        return False
        
    # We want to create the .data_config in the current directory 
    # so PyInstaller can pick it up.
    # Normally bake_config() deletes .env, which is what we want for Build 2.
    # However, let's just use the logic to generate the file.
    
    # Temporarily set secret_file to current dir for bundling
    original_secret = manager.secret_file
    manager.secret_file = os.path.join(os.getcwd(), ".data_config")
    
    success = manager.bake_config()
    
    if success:
        print(f"[OK] Created obfuscated config at: {manager.secret_file}")
    else:
        print("[FAIL] Baking failed.")
    return success

if __name__ == "__main__":
    main()
