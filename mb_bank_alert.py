import os
import sys
import time
import threading
import queue
import re
import zipfile
import urllib.request
import shutil
from datetime import datetime
import pygame
import paho.mqtt.client as mqtt
from config_utils import ConfigManager

# ─────────────────────────────────────────────
#   CẤU HÌNH & KHỞI TẠO
# ─────────────────────────────────────────────
config_manager = ConfigManager()
config = config_manager.load_config()

if not config:
    if not config_manager.interactive_setup():
        sys.exit(1)
    config = config_manager.load_config()

ADAFRUIT_IO_USERNAME = config.get("ADAFRUIT_IO_USERNAME")
ADAFRUIT_IO_KEY = config.get("ADAFRUIT_IO_KEY")
FEED_NAME = config.get("FEED_NAME")
MQTT_TOPIC = f"{ADAFRUIT_IO_USERNAME}/feeds/{FEED_NAME}"

# Cấu hình nguồn âm thanh từ GitHub
SOUNDS_REPO_ZIP = "https://github.com/hoafd/sounds_numbers_vi-VN/archive/refs/heads/main.zip"

if getattr(sys, 'frozen', False):
    INTERNAL_SOUNDS = os.path.join(sys._MEIPASS, "sounds")
    EXTERNAL_SOUNDS = os.path.join(os.path.dirname(sys.executable), "sounds")
    SOUNDS_DIR = INTERNAL_SOUNDS if os.path.exists(INTERNAL_SOUNDS) and len(os.listdir(INTERNAL_SOUNDS)) > 10 else EXTERNAL_SOUNDS
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    SOUNDS_DIR = os.path.join(BASE_DIR, "sounds")

speech_queue = queue.Queue()
SOUND_CACHE = {} 

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def auto_download_sounds():
    global SOUNDS_DIR
    if os.path.exists(SOUNDS_DIR) and len([f for f in os.listdir(SOUNDS_DIR) if f.endswith(".wav")]) >= 20:
        return 
    print("[...] Dang tai thu vien am thanh tu GitHub...")
    target_dir = os.path.join(BASE_DIR, "sounds")
    zip_path = os.path.join(BASE_DIR, "sounds_master.zip")
    extract_path = os.path.join(BASE_DIR, "temp_sounds")
    try:
        urllib.request.urlretrieve(SOUNDS_REPO_ZIP, zip_path)
        with zipfile.ZipFile(zip_path, 'r') as zip_ref: zip_ref.extractall(extract_path)
        source_folder = os.path.join(extract_path, "sounds_numbers_vi-VN-main", "sounds_wav")
        if not os.path.exists(target_dir): os.makedirs(target_dir)
        for file in os.listdir(source_folder):
            if file.endswith(".wav"): shutil.move(os.path.join(source_folder, file), os.path.join(target_dir, file))
        SOUNDS_DIR = target_dir
    except: pass
    finally:
        if os.path.exists(zip_path): os.remove(zip_path)
        if os.path.exists(extract_path): shutil.rmtree(extract_path)

def init_audio():
    try:
        auto_download_sounds()
        pygame.mixer.init()
        if os.path.exists(SOUNDS_DIR):
            for file in os.listdir(SOUNDS_DIR):
                if file.endswith(".wav"):
                    key = file.replace(".wav", "")
                    SOUND_CACHE[key] = pygame.mixer.Sound(os.path.join(SOUNDS_DIR, file))
        print(f"[OK] Audio Ready (Path: {os.path.basename(SOUNDS_DIR)})")
    except Exception as e: print(f"[ERR] Audio: {e}")

# ─────────────────────────────────────────────
#   XỬ LÝ SỐ
# ─────────────────────────────────────────────
def number_to_sound_keys(number_str):
    try:
        num = int(''.join(filter(str.isdigit, str(number_str))))
        if num == 0: return ["0", "dong"]
        def read_three_digits(n, show_zero=False):
            res = []
            h, t, u = n // 100, (n // 10) % 10, n % 10
            if h > 0 or show_zero: res.extend([str(h), "tram"])
            if t == 0: 
                if h > 0 and u > 0: res.append("le")
            elif t == 1: res.append("10")
            else: res.extend([str(t), "muoi"])
            if t > 1 and u == 1: res.append("mot")
            elif t > 0 and u == 5: res.append("lam")
            elif u > 0: res.append(str(u))
            return res
        final = ["prefix"]; units = ["", "nghin", "trieu", "ty", "nghin", "trieu"]
        chunks = []
        temp_num = num
        while temp_num > 0:
            chunks.append(temp_num % 1000); temp_num //= 1000
        for i in range(len(chunks)-1, -1, -1):
            if chunks[i] > 0:
                final.extend(read_three_digits(chunks[i], i < len(chunks)-1))
                if units[i]: final.append(units[i])
        return final + ["dong"]
    except: return []

def speech_worker():
    while True:
        try:
            amount_str = speech_queue.get()
            if amount_str is None: break
            keys = number_to_sound_keys(amount_str)
            for k in keys:
                if k in SOUND_CACHE:
                    chan = SOUND_CACHE[k].play()
                    while chan and chan.get_busy(): time.sleep(0.01)
            speech_queue.task_done()
        except: pass

threading.Thread(target=speech_worker, daemon=True).start()

# ─────────────────────────────────────────────
#   LOG GIAO DỊCH CHUYÊN NGHIỆP
# ─────────────────────────────────────────────
def log_transaction_pretty(payload):
    """Hiển thị log 3 dòng dùng thời gian ngân hàng"""
    try:
        parts = payload.split(" || ")
        sotien = parts[0] if len(parts) >= 1 else payload
        thoigian = parts[1].strip("[]") if len(parts) >= 2 else datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        noidung = parts[2] if len(parts) >= 3 else "Khong ro noi dung"
        
        print("\n" + "─"*50)
        print(f"[{thoigian}]")
        print(f"+ {sotien} VND")
        print(f"ND: {noidung}")
        print("─"*50)
    except:
        print(f"\n[!] New Message: {payload}")

# ─────────────────────────────────────────────
#   MQTT CALLBACKS
# ─────────────────────────────────────────────
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"[OK] Dang cho thong bao tu Adafruit IO...")
        client.subscribe(MQTT_TOPIC)
    else: print(f"[ERR] RC={rc}")

def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode("utf-8").strip()
        if payload:
            # 1. Ghi log đẹp mắt
            log_transaction_pretty(payload)
            
            # 2. Lấy số tiền để đọc loa (Luôn là phần đầu tiên)
            match = re.search(r'([\d.]+)', payload.split(" || ")[0])
            if match:
                speech_queue.put(match.group(1))
    except: pass

def main():
    clear_console()
    print(f"--- MB-BANK BALANCE ALERT (PREMIUM LOG) ---")
    init_audio()
    client = mqtt.Client(client_id=f"mb_{int(time.time())}")
    client.username_pw_set(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)
    client.on_connect = on_connect; client.on_message = on_message
    print("[...] Dang ket noi server...")
    try:
        client.connect("io.adafruit.com", 1883, 60)
        client.loop_forever()
    except KeyboardInterrupt:
        print("\n[OK] Da dung."); sys.exit(0)
    except: time.sleep(5); main()

if __name__ == "__main__":
    main()
