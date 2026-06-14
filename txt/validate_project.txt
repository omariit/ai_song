#!/usr/bin/env python
"""
Final validation script - verify all required files and configurations
"""

import os
import sys

def check_file(filename, description=""):
    """Check if a file exists"""
    exists = os.path.exists(filename)
    status = "✓" if exists else "✗"
    desc = f" ({description})" if description else ""
    print(f"  {status} {filename}{desc}")
    return exists

def check_directory(dirname, description=""):
    """Check if a directory exists"""
    exists = os.path.isdir(dirname)
    status = "✓" if exists else "✗"
    desc = f" ({description})" if description else ""
    print(f"  {status} {dirname}/{desc}")
    return exists

def main():
    print("=" * 70)
    print("🔍 Final Project Validation")
    print("=" * 70)
    
    all_ok = True
    
    print("\n📁 Required Files:")
    print("-" * 70)
    
    required_files = [
        ("app.py", "Flask application"),
        ("generate_song.py", "Song generation engine"),
        ("startup.py", "Quick start script"),
        ("requirements.txt", "Dependencies"),
        ("README.md", "Documentation"),
        (".gitignore", "Git ignore rules"),
    ]
    
    for filename, desc in required_files:
        if not check_file(filename, desc):
            all_ok = False
    
    print("\n📁 Required Directories:")
    print("-" * 70)
    
    required_dirs = [
        ("templates", "Web interface"),
    ]
    
    for dirname, desc in required_dirs:
        if not check_directory(dirname, desc):
            all_ok = False
    
    print("\n📁 Required Templates:")
    print("-" * 70)
    
    if os.path.isdir("templates"):
        template_files = [
            ("templates/index.html", "Web UI"),
        ]
        for filename, desc in template_files:
            if not check_file(filename, desc):
                all_ok = False
    
    print("\n📝 Optional Files:")
    print("-" * 70)
    
    optional_files = [
        ("PROJECT_SUMMARY.md", "Project summary"),
        ("final_cleanup.py", "Cleanup script"),
    ]
    
    for filename, desc in optional_files:
        check_file(filename, desc)
    
    print("\n📊 File Sizes:")
    print("-" * 70)
    
    py_files = sorted([f for f in os.listdir(".") if f.endswith(".py")])
    for f in py_files:
        if os.path.isfile(f):
            size = os.path.getsize(f) / 1024  # KB
            print(f"  {f:<25} {size:>8.1f} KB")
    
    print("\n" + "=" * 70)
    
    if all_ok:
        print("✅ Project is complete and ready to use!")
        print("\nNext steps:")
        print("  1. Run: python startup.py")
        print("  2. Open: http://localhost:5000")
        print("  3. Enjoy your AI-generated songs!")
    else:
        print("❌ Some required files are missing!")
        print("Please create the missing files.")
        sys.exit(1)
    
    print("\n" + "=" * 70)

if __name__ == "__main__":
    main()
