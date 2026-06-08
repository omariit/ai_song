#!/usr/bin/env python
"""
Complete cleanup - Remove all temporary and unnecessary files
تنظيف نهائي - حذف جميع الملفات المؤقتة والغير ضرورية
"""

import os
import shutil

# Files to remove
FILES_TO_REMOVE = [
    "app_new.py",
    "generate_song_new.py",
    "test_logging.py",
    "test_simple_logging.py",
    "cleanup.py",
    "UPGRADE_NOTES.md",
    "LOGGING_SYSTEM.md",
    "final_cleanup.py",  # Remove this script too
]

print("=" * 70)
print("🧹 FINAL CLEANUP - حذف الملفات المؤقتة")
print("=" * 70)
print()

deleted = []
skipped = []

for filename in FILES_TO_REMOVE:
    if os.path.exists(filename):
        try:
            os.remove(filename)
            deleted.append(filename)
            print(f"✓ تم الحذف: {filename}")
        except Exception as e:
            print(f"✗ خطأ: {filename} - {e}")
            skipped.append(filename)
    else:
        print(f"- غير موجود: {filename}")

print()
print("=" * 70)
print(f"✅ تم الانتهاء! ({len(deleted)} ملفات محذوفة)")
print("=" * 70)
print()

print("📂 الملفات المتبقية المهمة:")
print("-" * 70)

important_files = {
    ".gitignore": "قوانين Git",
    "app.py": "تطبيق Flask",
    "generate_song.py": "محرك التوليد",
    "startup.py": "برنامج البدء",
    "requirements.txt": "المكتبات",
    "README.md": "التوثيق الرئيسي",
    "QUICK_START.md": "البدء السريع",
    "PROJECT_SUMMARY.md": "ملخص المشروع",
    "templates/index.html": "واجهة الويب",
}

for filename, desc in important_files.items():
    exists = "✓" if os.path.exists(filename) else "✗"
    print(f"  {exists} {filename:<30} - {desc}")

print()
print("=" * 70)
print("✨ المشروع جاهز للاستخدام!")
print("=" * 70)
print()
print("🚀 للبدء:")
print("   python startup.py")
print()
