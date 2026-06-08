#!/usr/bin/env python
"""
AI Song Generator - Startup Script
برنامج مساعد للبدء السريع والتحقق من المتطلبات
"""

import os
import sys
import subprocess

def check_python_version():
    """التحقق من نسخة Python"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 10):
        print(f"✗ Python 3.10+ مطلوب (لديك {version.major}.{version.minor})")
        return False
    print(f"✓ Python {version.major}.{version.minor} - محسّن")
    return True

def check_ffmpeg():
    """التحقق من تثبيت FFmpeg"""
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
        print("✓ FFmpeg - مثبت")
        return True
    except:
        print("✗ FFmpeg - غير مثبت")
        print("   التثبيت:")
        print("   Windows: choco install ffmpeg")
        print("   macOS: brew install ffmpeg")
        print("   Linux: sudo apt-get install ffmpeg")
        return False

def check_dependencies():
    """التحقق من المكتبات المطلوبة"""
    required = ["flask", "pydub", "numpy", "torch", "bark"]
    missing = []
    
    for package in required:
        try:
            __import__(package.replace("-", "_"))
            print(f"✓ {package} - مثبت")
        except ImportError:
            missing.append(package)
            print(f"✗ {package} - غير مثبت")
    
    return len(missing) == 0

def main():
    print("=" * 70)
    print("AI Song Generator - بدء البرنامج")
    print("=" * 70)
    print()
    
    # التحقق
    print("التحقق من المتطلبات:")
    print("-" * 70)
    
    checks = [
        ("Python", check_python_version()),
        ("FFmpeg", check_ffmpeg()),
        ("المكتبات", check_dependencies()),
    ]
    
    print()
    print("-" * 70)
    
    all_ok = all(check[1] for check in checks)
    
    if not all_ok:
        print()
        print("✗ بعض المتطلبات ناقصة")
        print()
        print("يرجى تثبيت المكتبات:")
        print("  pip install -r requirements.txt")
        print()
        return
    
    print("✓ جميع المتطلبات محسّنة!")
    print()
    print("=" * 70)
    print("بدء البرنامج...")
    print("=" * 70)
    print()
    
    # تشغيل التطبيق
    try:
        os.system("python app.py")
    except KeyboardInterrupt:
        print("\n\nتم إيقاف البرنامج بنجاح.")

if __name__ == "__main__":
    main()
