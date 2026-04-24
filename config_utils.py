import os
import sys
import base64
import json
import shutil
from dotenv import load_dotenv, dotenv_values

import subprocess

class ConfigManager:
    """
    Handles the 'Capture and Bake' configuration workflow with Hardware Binding.
    """
    
    def _get_machine_id(self):
        """Retrieves a unique hardware ID in a portable way (Windows/Linux/Mac)."""
        try:
            import uuid
            # Use MAC address as a stable hardware identifier
            node = uuid.getnode()
            return str(uuid.UUID(int=node))
        except Exception:
            import socket
            return socket.gethostname()

    def __init__(self, env_file_name=".env"):
        # Determine base directory
        if getattr(sys, 'frozen', False):
            # Compiled EXE mode
            self.base_dir = os.path.dirname(sys.executable)
            self.secret_dir = os.path.join(self.base_dir, "_internal")
        else:
            # Script mode
            self.base_dir = os.path.dirname(os.path.abspath(__file__))
            self.secret_dir = os.path.join(self.base_dir, "venv")

        self.env_file = os.path.join(self.base_dir, env_file_name)
        
        # Dynamic XOR Key: Hardcoded Salt + Machine UUID
        self._XOR_KEY = f"MB_SALT_2026_{self._get_machine_id()}"
        
        # Ensure secret dir exists (for script mode fallback)
        if not os.path.exists(self.secret_dir):
            self.secret_dir = self.base_dir
        self.secret_file = os.path.join(self.secret_dir, ".data_config")

    def _xor_cipher(self, data):
        """Simple XOR cipher for obfuscation."""
        return "".join(chr(ord(c) ^ ord(self._XOR_KEY[i % len(self._XOR_KEY)])) 
                       for i, c in enumerate(data))

    def _sanitize_config(self, config):
        """Automatically parses Adafruit URLs if pasted into the config."""
        # Priority 1: Check for a dedicated ADAFRUIT_URL key
        # Priority 2: Check ADAFRUIT_IO_USERNAME or FEED_NAME for a URL
        targets = ["ADAFRUIT_URL", "ADAFRUIT_IO_USERNAME", "FEED_NAME"]
        
        for key in targets:
            val = config.get(key, "")
            if val and "io.adafruit.com/api/v2/" in val:
                parts = val.split("/")
                try:
                    # Index -3 is USERNAME, Index -1 is FEED_NAME
                    username = parts[-3]
                    feed = parts[-1]
                    config["ADAFRUIT_IO_USERNAME"] = username
                    config["FEED_NAME"] = feed
                    # Silently detected
                    break # Stop after first successful detection
                except Exception:
                    pass
        return config

    def bake_config(self):
        """Encodes .env content and cleans up."""
        if not os.path.exists(self.env_file):
            return False

        config = dotenv_values(self.env_file)
        if not config:
            print("[!] .env is empty. Skipping bake.")
            return False
            
        # Auto-parse URLs if present (extracts Username and Feed from full link)
        config = self._sanitize_config(config)
        
        # Convert to JSON and obfuscate
        json_data = json.dumps(config)
        obfuscated_data = self._xor_cipher(json_data)
        encoded_data = base64.b64encode(obfuscated_data.encode()).decode()

        # Save to secret location
        with open(self.secret_file, "w") as f:
            f.write(encoded_data)
        
        print("[+] Configuration secured (Baked).")

        # Cleanup
        try:
            if os.path.exists(self.env_file):
                os.remove(self.env_file)
                print("[+] Plain-text .env removed for security.")
            
            # Recreate clean template directly to .env
            self._create_env_template()
            print("[+] Configuration template restored to .env.")
        except Exception as e:
            print(f"[!] Cleanup notice: {e}")

        return True

    def _create_env_template(self):
        """Creates a default .env template if it's missing."""
        if not os.path.exists(self.env_file):
            content = """# =============================================================
# CẤU HÌNH MB BANK BALANCE ALERT
# =============================================================

# 📡 Cấu hình Adafruit IO
# -------------------------------------------------------------
# CÁCH 1: NHẬP NHANH (KHUYÊN DÙNG - ƯU TIÊN SỐ 1)
# Dán thẳng link Feed URL của bạn vào đây. Hệ thống sẽ tự tách Username và Feed.
# Ví dụ: ADAFRUIT_URL=https://io.adafruit.com/api/v2/your_username/feeds/your_feed_name
ADAFRUIT_URL=

# CÁCH 2: NHẬP THỦ CÔNG (Chỉ dùng nếu ADAFRUIT_URL để trống)
# Tên đăng nhập Adafruit (Lấy từ profile hoặc link feed)
ADAFRUIT_IO_USERNAME=your_username
# Tên Feed nhận dữ liệu (Ví dụ: tien-888)
FEED_NAME=your_feed_name

# 🔑 BIẾN BẮT BUỘC (QUAN TRỌNG NHẤT)
# Lấy tại: https://io.adafruit.com -> IO -> feed nhận dữ liệu -> Nhấn vào biểu tượng chìa khóa (Active Key) góc trên bên phải
ADAFRUIT_IO_KEY=aio_xxxxxxxxxxxxxxxxxxxxxxxxxxxx

# 🎙️ Cấu hình giọng đọc (TTS)
# -------------------------------------------------------------
# vi-VN-HoaiMyNeural (Nữ miền Nam) 
# vi-VN-NamMinhNeural (Nam miền Bắc)
TTS_VOICE=vi-VN-HoaiMyNeural
"""
            with open(self.env_file, "w", encoding="utf-8") as f:
                f.write(content)
            print("[+] New .env template created.")

    def interactive_setup(self):
        """Allows user to input configuration directly in the console."""
        print("\n" + "="*50)
        print(" 🛠️ THIET LAP CAU HINH NHANH")
        print("="*50)
        print(" [Meo]: Ban co the paste (chuot phai) vao day.")
        
        url = input("\n 1. Nhap Adafruit Feed URL (hoac de trong): ").strip()
        user = ""
        feed = ""
        if not url:
            user = input("    -> Nhap Adafruit Username: ").strip()
            feed = input("    -> Nhap Feed Name (vd: tien-888): ").strip()
            
        key = input(" 2. Nhap Adafruit IO Key (Active Key): ").strip()
        
        # Build .env content
        lines = [
            "# TU DONG TAO TU INTERACTIVE SETUP",
            f"ADAFRUIT_URL={url}",
            f"ADAFRUIT_IO_USERNAME={user}",
            f"FEED_NAME={feed}",
            f"ADAFRUIT_IO_KEY={key}",
            "TTS_VOICE=vi-VN-HoaiMyNeural"
        ]
        
        try:
            with open(self.env_file, "w", encoding="utf-8") as f:
                f.write("\n".join(lines))
            print("\n[OK] Da luu cau hinh vao .env. Chuong trinh se thu lai...")
            return True
        except Exception as e:
            print(f"\n[!] Loi khi luu file: {e}")
            return False

    def load_config(self):
        """Loads and decodes the configuration."""
        self._create_env_template()

        # Always check if a new .env exists first to 're-bake'
        if os.path.exists(self.env_file):
            vals = dotenv_values(self.env_file)
            
            # Check only sensitive fields for real data
            has_real_data = False
            sensitive_keys = ["ADAFRUIT_URL", "ADAFRUIT_IO_USERNAME", "ADAFRUIT_IO_KEY", "FEED_NAME"]
            placeholders = [
                "your_username", "your_password", "your_account_number", 
                "aio_xxxxxxxx", "your_feed_name", "your_key", "feed_name"
            ]
            
            for k in sensitive_keys:
                v = vals.get(k, "")
                if v and not any(p in v.lower() for p in placeholders):
                    has_real_data = True
                    break
            
            if has_real_data:
                self.bake_config()

        # If secret file exists, load and decode it
        if os.path.exists(self.secret_file):
            try:
                with open(self.secret_file, "r") as f:
                    encoded_data = f.read()
                
                obfuscated_data = base64.b64decode(encoded_data).decode()
                json_data = self._xor_cipher(obfuscated_data)
                return json.loads(json_data)
            except Exception as e:
                print(f"[!] Error loading hidden config from {self.secret_file}: {e}")
        
        return None
