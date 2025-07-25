#!/usr/bin/env python3
"""
Comprehensive test script for rm command logic validation.
Tests the is_dangerous_rm_command function without executing actual rm commands.
"""

import sys
import os
import re
import shlex

# Add the hooks directory to path to import the functions
sys.path.insert(0, '/home/yoda/.claude/hooks')

# Test both original and new logic
def original_is_dangerous_rm_command(command):
    """Original logic - blocks all rm -rf commands"""
    normalized = ' '.join(command.lower().split())
    
    patterns = [
        r'\brm\s+.*-[a-z]*r[a-z]*f',
        r'\brm\s+.*-[a-z]*f[a-z]*r',
        r'\brm\s+--recursive\s+--force',
        r'\brm\s+--force\s+--recursive',
        r'\brm\s+-r\s+.*-f',
        r'\brm\s+-f\s+.*-r',
    ]
    
    for pattern in patterns:
        if re.search(pattern, normalized):
            return True
    
    dangerous_paths = [
        r'/',
        r'/\*',
        r'~',
        r'~/',
        r'\$HOME',
        r'\.\.',
        r'\*',
        r'\.',
        r'\.\s*$',
    ]
    
    if re.search(r'\brm\s+.*-[a-z]*r', normalized):
        for path in dangerous_paths:
            if re.search(path, normalized):
                return True
    
    return False

def is_safe_rm_path(path):
    """New whitelist logic with absolute path support"""
    path = path.strip()
    
    # Get user home directory
    user_home = os.path.expanduser('~')
    
    safe_relative_patterns = [
        r'^\./[\w\-_./]+$',
        r'^[\w\-_.]+/$',
        r'^[\w\-_.]+$',
    ]
    
    safe_parent_patterns = [
        r'^\.\./[\w\-_./]+$',
        r'^\.\./[\w\-_.]+/$',
        r'^\.\./[\w\-_.]+$',
        r'^\.\./(node_modules|build|dist|target|tmp|temp|logs|cache)(/.*)?$',
    ]
    
    # Safe absolute paths within user home directory
    safe_absolute_patterns = [
        # Project-related directories within home
        rf'^{re.escape(user_home)}/[\w\-_.]+/.*/(node_modules|build|dist|target|\.gradle|\.next|\.nuxt|tmp|temp|cache|logs|\.cache|coverage|__pycache__|\.pytest_cache|\.mypy_cache)(/.*)?$',
        # Direct safe directories in home subdirectories
        rf'^{re.escape(user_home)}/.*/(node_modules|build|dist|target|\.gradle|\.next|\.nuxt|tmp|temp|cache|logs|\.cache|coverage|__pycache__|\.pytest_cache|\.mypy_cache)(/.*)?$',
        # Safe file extensions in home directory
        rf'^{re.escape(user_home)}/.*\.(log|tmp|cache|temp)$',
    ]
    
    safe_directories = [
        'node_modules', 'build', 'dist', 'target', '.next', '.nuxt',
        'tmp', 'temp', 'cache', 'logs', '.cache', 'coverage',
        '__pycache__', '.pytest_cache', '.mypy_cache', '.gradle'
    ]
    
    safe_file_patterns = [
        r'.*\.(log|tmp|cache|temp)$',
        r'.*\.log\.\d+$',
    ]
    
    if path in safe_directories or path.rstrip('/') in safe_directories:
        return True
    
    for pattern in safe_relative_patterns:
        if re.match(pattern, path):
            return True
    
    for pattern in safe_parent_patterns:
        if re.match(pattern, path):
            return True
    
    # Check absolute patterns within user home
    for pattern in safe_absolute_patterns:
        if re.match(pattern, path):
            return True
    
    for pattern in safe_file_patterns:
        if re.match(pattern, path):
            return True
    
    return False

def new_is_dangerous_rm_command(command):
    """New hybrid whitelist+blacklist logic"""
    normalized = ' '.join(command.lower().split())
    
    has_rf_flags = bool(re.search(r'\brm\s+.*-[a-z]*r[a-z]*f|\brm\s+.*-[a-z]*f[a-z]*r|\brm\s+--recursive\s+--force|\brm\s+--force\s+--recursive|\brm\s+-r\s+.*-f|\brm\s+-f\s+.*-r', normalized))
    
    if not has_rf_flags:
        return False
    
    path_part = re.sub(r'\brm\s+(-[a-z]*|--\w+)*\s*', '', command).strip()
    
    try:
        paths = shlex.split(path_part) if path_part else []
    except ValueError:
        paths = path_part.split() if path_part else []
    
    always_dangerous_patterns = [
        r'^/$',
        r'^/\*$',
        r'^~$',
        r'^~/$',
        r'^\$HOME$',
        r'^\.\.$',
        r'^\.\./\*$',
        r'^\*$',
        r'^\.$',
        r'^/usr(/.*)?$',
        r'^/etc(/.*)?$',
        r'^/var(/.*)?$',
        r'^/boot(/.*)?$',
        r'^/sys(/.*)?$',
        r'^/proc(/.*)?$',
    ]
    
    for path in paths:
        path = path.strip().strip('"\'')
        
        for dangerous_pattern in always_dangerous_patterns:
            if re.match(dangerous_pattern, path):
                return True
        
        if not is_safe_rm_path(path):
            return True
    
    return False

def run_tests():
    """Run comprehensive test suite"""
    print("🧪 Testing RM Command Logic")
    print("=" * 50)
    
    # CRITICAL: Commands that MUST be blocked
    dangerous_commands = [
        "rm -rf /",
        "rm -rf /*",
        "rm -rf ~",
        "rm -rf ~/",
        "rm -rf $HOME",
        "rm -rf .",
        "rm -rf ..",
        "rm -rf ../*",
        "rm -rf *",
        "rm -fr /",
        "rm --recursive --force /",
        "rm -rf /usr",
        "rm -rf /etc",
        "rm -rf /var",
        "rm -rf /boot",
        "rm -rf /sys",
        "rm -rf /proc",
    ]
    
    # Commands that SHOULD be allowed
    safe_commands = [
        "rm -rf node_modules",
        "rm -rf build",
        "rm -rf dist",
        "rm -rf ./build",
        "rm -rf ./dist/output",
        "rm -rf ../node_modules",
        "rm -rf ../build",
        "rm -rf ../dist/assets",
        "rm -rf temp.log",
        "rm -rf cache/",
        "rm -rf logs/",
        "rm -rf .cache",
        "rm -rf __pycache__",
        "rm -rf .pytest_cache",
        "rm file.txt",  # No -rf flags
        "rm -f file.txt",  # No recursive flag
        # Absolute paths within user home (these should now be allowed)
        "rm -rf /home/yoda/Library/Projects/VR/bubbles-game/bubble-test/android/.gradle",
        "rm -rf /home/yoda/projects/myapp/node_modules",
        "rm -rf /home/yoda/code/react-app/build",
        "rm -rf /home/yoda/workspace/dist",
        "rm -rf /home/yoda/tmp/temp.log",
    ]
    
    # Edge cases
    edge_cases = [
        'rm -rf "node_modules"',  # Quoted paths
        "rm -rf node_modules build dist",  # Multiple paths
        "rm -rf",  # No paths
        "rm -rf ../node_modules ./build",  # Mixed paths
    ]
    
    print("🚨 Testing DANGEROUS commands (must be blocked):")
    all_dangerous_blocked = True
    for cmd in dangerous_commands:
        original_result = original_is_dangerous_rm_command(cmd)
        new_result = new_is_dangerous_rm_command(cmd)
        
        status = "✅" if new_result else "❌ CRITICAL FAILURE"
        print(f"  {status} {cmd:<30} -> Blocked: {new_result}")
        
        if not new_result:
            all_dangerous_blocked = False
            print(f"    🚨 CRITICAL: This dangerous command would NOT be blocked!")
    
    print(f"\n✅ Testing SAFE commands (should be allowed):")
    all_safe_allowed = True
    for cmd in safe_commands:
        original_result = original_is_dangerous_rm_command(cmd)
        new_result = new_is_dangerous_rm_command(cmd)
        
        status = "✅" if not new_result else "⚠️"
        print(f"  {status} {cmd:<30} -> Blocked: {new_result} (was: {original_result})")
        
        if new_result:
            all_safe_allowed = False
    
    print(f"\n🔍 Testing EDGE cases:")
    for cmd in edge_cases:
        original_result = original_is_dangerous_rm_command(cmd)
        new_result = new_is_dangerous_rm_command(cmd)
        
        print(f"  📝 {cmd:<30} -> Blocked: {new_result} (was: {original_result})")
    
    print("\n" + "=" * 50)
    print("📊 SUMMARY:")
    print(f"✅ All dangerous commands blocked: {all_dangerous_blocked}")
    print(f"✅ All safe commands allowed: {all_safe_allowed}")
    
    if all_dangerous_blocked and all_safe_allowed:
        print("🎉 ALL TESTS PASSED - Safe to deploy!")
        return True
    else:
        print("❌ TESTS FAILED - DO NOT DEPLOY!")
        if not all_dangerous_blocked:
            print("🚨 CRITICAL: Some dangerous commands would not be blocked!")
        return False

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)