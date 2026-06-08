#!/usr/bin/env python
"""
FINAL COMPLETION SCRIPT
برنامج الإتمام النهائي - ينظف المشروع ويحضره للاستخدام
"""

import os
import sys
from pathlib import Path

print("=" * 80)
print("🎉 AI SONG GENERATOR - FINAL COMPLETION SCRIPT")
print("=" * 80)
print()

# Files to remove
files_to_remove = [
    "app_new.py",
    "generate_song_new.py",
    "test_logging.py",
    "test_simple_logging.py",
    "cleanup.py",
    "final_cleanup.py",
    "LOGGING_SYSTEM.md",
    "UPGRADE_NOTES.md",
    "validate_project.py",
    "00_READ_ME_FIRST.txt",
    "FILES_MANIFEST.md",
    "FINAL_STATUS.txt",
    "COMPLETION_REPORT.txt",
    "cleanup_all.py",
    "finish_project.py",  # This script itself
]

# Required files
required_files = {
    "app.py": "Flask Application",
    "generate_song.py": "Song Generator Engine",
    "startup.py": "Startup Script",
    "requirements.txt": "Dependencies",
    "README.md": "Main Documentation",
    "QUICK_START.md": "Quick Start Guide",
    "PROJECT_SUMMARY.md": "Project Summary",
    ".gitignore": "Git Configuration",
}

print("📋 CLEANUP PLAN:")
print("-" * 80)
print()
print("Files to DELETE (cleanup):")
for i, f in enumerate(files_to_remove, 1):
    if os.path.exists(f):
        size = os.path.getsize(f) / 1024
        print(f"  {i:2}. ❌ {f:<40} ({size:.1f} KB)")
    else:
        print(f"  {i:2}. - {f:<40} (not found)")

print()
print("Files to KEEP (required):")
for i, (f, desc) in enumerate(required_files.items(), 1):
    exists = "✅" if os.path.exists(f) else "❌"
    print(f"  {i:2}. {exists} {f:<40} {desc}")

print()
print("-" * 80)
print()

# Ask for confirmation
response = input("🤔 Proceed with cleanup? (yes/no): ").strip().lower()
if response not in ["yes", "y"]:
    print("\n❌ Cleanup cancelled.")
    sys.exit(0)

print()
print("🧹 CLEANING UP...")
print("-" * 80)

deleted = 0
failed = 0

for filename in files_to_remove:
    if os.path.exists(filename):
        try:
            os.remove(filename)
            print(f"✓ Deleted: {filename}")
            deleted += 1
        except Exception as e:
            print(f"✗ Failed: {filename} - {e}")
            failed += 1

print()
print("=" * 80)
print(f"✅ Cleanup complete! Deleted {deleted} files")
print("=" * 80)
print()

# Verify required files
print("🔍 VERIFICATION:")
print("-" * 80)

all_present = True
for filename, description in required_files.items():
    if os.path.exists(filename):
        size = os.path.getsize(filename) / 1024
        print(f"✅ {filename:<40} ({size:6.1f} KB) - {description}")
    else:
        print(f"❌ {filename:<40} NOT FOUND!")
        all_present = False

print()

# Check templates
if os.path.exists("templates/index.html"):
    size = os.path.getsize("templates/index.html") / 1024
    print(f"✅ templates/index.html         ({size:6.1f} KB) - Web UI")
else:
    print(f"❌ templates/index.html         NOT FOUND!")
    all_present = False

print()
print("-" * 80)

if all_present:
    print("✅ All required files are present!")
    print()
    print("=" * 80)
    print("🎉 PROJECT IS READY!")
    print("=" * 80)
    print()
    print("🚀 Next steps:")
    print("  1. Install dependencies: pip install -r requirements.txt")
    print("  2. Run the app: python startup.py")
    print("  3. Open browser: http://localhost:5000")
    print("  4. Enjoy creating songs! 🎵")
    print()
else:
    print("⚠️  Some required files are missing!")
    print()
    print("❌ PROJECT IS INCOMPLETE")
    print()

print("=" * 80)
