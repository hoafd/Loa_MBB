import asyncio
import edge_tts
import os

async def test_tts(text, voice="vi-VN-HoaiMyNeural"):
    print(f"Testing: {text}")
    try:
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save("test_audio.mp3")
        print(" [OK] Success!")
        if os.path.exists("test_audio.mp3"):
            os.remove("test_audio.mp3")
    except Exception as e:
        print(f" [ERR] Failed: {e}")

async def main():
    # Test 1: Simple text
    await test_tts("Xin chào")
    # Test 2: Large number
    await test_tts("Bạn vừa nhận 9800000 đồng")
    # Test 3: Large number with dots
    await test_tts("Bạn vừa nhận 9.800.000 đồng")
    # Test 4: Transaction ID
    await test_tts("từ N-611401311449")
    # Test 5: Full text
    await test_tts("nhận 9.800.000 đồng từ N-611401311449")

if __name__ == "__main__":
    asyncio.run(main())
