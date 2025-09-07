#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# ///

import json
import sys
import re
from pathlib import Path

def is_safe_rm_path(path):
    """
    Check if a path is safe for rm -rf operations.
    Returns True if the path matches known safe patterns.
    """
    import os
    path = path.strip()
    
    # Get user home directory
    user_home = os.path.expanduser('~')
    
    # Safe relative paths
    safe_relative_patterns = [
        r'^\./[\w\-_./]+$',  # ./path/to/dir
        r'^[\w\-_.]+/$',     # dirname/
        r'^[\w\-_.]+$',      # dirname
        r'^\.next$',         # .next directory
        r'^\.next/$',        # .next/ directory
        # Subdirectories within safe directories
        r'^(node_modules|build|dist|target|\.next|\.nuxt|tmp|temp|cache|logs|\.cache|coverage|__pycache__|\.pytest_cache|\.mypy_cache|\.gradle)(/.*)?$',
    ]
    
    # Safe parent directory patterns (specific named directories only)
    safe_parent_patterns = [
        r'^\.\./[\w\-_./]+$',      # ../specific/path
        r'^\.\./[\w\-_.]+/$',      # ../dirname/
        r'^\.\./[\w\-_.]+$',       # ../dirname
        r'^\.\./(node_modules|build|dist|target|tmp|temp|logs|cache)(/.*)?$',  # ../safe_dirs
    ]
    
    # Safe absolute paths within user home directory
    safe_absolute_patterns = [
        # Allow all operations under /home/yoda/Library/Projects
        r'^/home/yoda/Library/Projects(/.*)?$',
        # Project-related directories within home
        rf'^{re.escape(user_home)}/[\w\-_.]+/.*/(node_modules|build|dist|target|\.gradle|\.next|\.nuxt|tmp|temp|cache|logs|\.cache|coverage|__pycache__|\.pytest_cache|\.mypy_cache)(/.*)?$',
        # Direct safe directories in home subdirectories
        rf'^{re.escape(user_home)}/.*/(node_modules|build|dist|target|\.gradle|\.next|\.nuxt|tmp|temp|cache|logs|\.cache|coverage|__pycache__|\.pytest_cache|\.mypy_cache)(/.*)?$',
        # Safe file extensions in home directory
        rf'^{re.escape(user_home)}/.*\.(log|tmp|cache|temp)$',
    ]
    
    # Common safe directory names
    safe_directories = [
        'node_modules', 'build', 'dist', 'target', '.next', '.nuxt',
        'tmp', 'temp', 'cache', 'logs', '.cache', 'coverage',
        '__pycache__', '.pytest_cache', '.mypy_cache', '.gradle'
    ]
    
    # Safe file patterns
    safe_file_patterns = [
        r'.*\.(log|tmp|cache|temp)$',  # Safe file extensions
        r'.*\.log\.\d+$',              # Rotated log files
    ]
    
    # Check safe directory names
    if path in safe_directories or path.rstrip('/') in safe_directories:
        return True
    
    # Check relative patterns
    for pattern in safe_relative_patterns:
        if re.match(pattern, path):
            return True
    
    # Check parent directory patterns
    for pattern in safe_parent_patterns:
        if re.match(pattern, path):
            return True
    
    # Check absolute patterns within user home
    for pattern in safe_absolute_patterns:
        if re.match(pattern, path):
            return True
    
    # Check file patterns
    for pattern in safe_file_patterns:
        if re.match(pattern, path):
            return True
    
    return False

def parse_compound_command(command):
    """
    Parse a compound shell command and return individual command segments.
    Splits on shell operators (&&, ||, ;, |) while preserving quoted strings.
    """
    
    # Handle simple cases first
    if not any(op in command for op in ['&&', '||', ';', '|']):
        return [command.strip()]
    
    segments = []
    current_segment = ""
    i = 0
    in_quotes = False
    quote_char = None
    
    while i < len(command):
        char = command[i]
        
        # Handle quotes
        if char in ['"', "'"] and (i == 0 or command[i-1] != '\\'):
            if not in_quotes:
                in_quotes = True
                quote_char = char
            elif char == quote_char:
                in_quotes = False
                quote_char = None
        
        # Check for operators only when not in quotes
        if not in_quotes:
            # Check for two-character operators first
            if i < len(command) - 1:
                two_char = command[i:i+2]
                if two_char in ['&&', '||']:
                    if current_segment.strip():
                        segments.append(current_segment.strip())
                    current_segment = ""
                    i += 2
                    continue
            
            # Check for single-character operators
            if char in [';', '|']:
                # Make sure it's not part of ||
                if char == '|' and i < len(command) - 1 and command[i+1] == '|':
                    pass  # Skip, will be handled by || above
                elif char == '|' and i > 0 and command[i-1] == '|':
                    pass  # Skip, already handled
                else:
                    if current_segment.strip():
                        segments.append(current_segment.strip())
                    current_segment = ""
                    i += 1
                    continue
        
        current_segment += char
        i += 1
    
    if current_segment.strip():
        segments.append(current_segment.strip())
    
    return segments

def extract_rm_commands(command_segments):
    """
    Extract only the segments that contain dangerous rm commands.
    Filters out safe subcommands like 'git rm', 'docker rm', etc.
    Returns a list of rm command strings.
    """
    rm_commands = []
    
    # Safe parent commands that can have 'rm' as a subcommand
    safe_parent_commands = ['git', 'docker', 'npm', 'yarn', 'cargo', 'apt', 'yum', 'brew', 'pip', 'conda']
    
    for segment in command_segments:
        # Check if this segment contains an rm command
        # Use word boundary to avoid matching 'form', 'arm', etc.
        if not re.search(r'\brm\b', segment):
            continue
            
        # Split the segment into tokens to check command structure
        tokens = segment.strip().split()
        if not tokens:
            continue
            
        # Get the primary command (first non-flag token)
        primary_command = tokens[0]
        
        # If primary command is 'rm', it's potentially dangerous
        if primary_command == 'rm':
            rm_commands.append(segment.strip())
        # If primary command is a safe tool with 'rm' subcommand, skip it
        elif primary_command in safe_parent_commands:
            continue  # Safe subcommand, don't add to rm_commands
        # Check for other patterns where rm might appear dangerously
        # This handles cases like: sudo rm, env VAR=val rm, etc.
        else:
            # Look for rm as a standalone command after other prefixes
            # Split on common command separators and check each part
            rm_found = False
            for i, token in enumerate(tokens):
                if token == 'rm' and (i == 0 or tokens[i-1] in ['sudo', 'env', 'exec', 'xargs', 'parallel']):
                    rm_found = True
                    break
            
            if rm_found:
                rm_commands.append(segment.strip())
    
    return rm_commands

def is_dangerous_rm_command(command):
    """
    Detect dangerous rm commands using hybrid whitelist+blacklist approach.
    Blocks rm -rf unless all target paths are safe and none are dangerous.
    Now handles compound commands properly.
    """
    # Parse compound command and extract only rm commands
    command_segments = parse_compound_command(command)
    rm_commands = extract_rm_commands(command_segments)
    
    # If no rm commands found, it's safe
    if not rm_commands:
        return False
    
    # Check each rm command individually
    for rm_command in rm_commands:
        if is_dangerous_single_rm_command(rm_command):
            return True
    
    return False

def is_dangerous_single_rm_command(command):
    """
    Check if a single rm command is dangerous.
    This contains the original logic for checking individual rm commands.
    """
    # Normalize command by removing extra spaces and converting to lowercase
    normalized = ' '.join(command.lower().split())
    
    # Check if command has recursive+force flags
    has_rf_flags = bool(re.search(r'\brm\s+.*-[a-z]*r[a-z]*f|\brm\s+.*-[a-z]*f[a-z]*r|\brm\s+--recursive\s+--force|\brm\s+--force\s+--recursive|\brm\s+-r\s+.*-f|\brm\s+-f\s+.*-r', normalized))
    
    if not has_rf_flags:
        return False  # Allow rm without recursive+force flags
    
    # Extract paths from the command
    # Remove the rm command and flags to get the paths
    path_part = re.sub(r'\brm\s+(-[a-z]*|--\w+)*\s*', '', command).strip()
    
    # Split paths (handle quoted paths)
    import shlex
    try:
        paths = shlex.split(path_part) if path_part else []
    except ValueError:
        # If shlex fails, fall back to simple split
        paths = path_part.split() if path_part else []
    
    # Always dangerous patterns (override whitelist)
    always_dangerous_patterns = [
        r'^/$',              # Root directory
        r'^/\*$',            # Root with wildcard
        r'^~$',              # Home directory
        r'^~/$',             # Home directory path
        r'^\$HOME$',         # Home environment variable
        r'^\.\.$',           # Parent directory (bare)
        r'^\.\./\*$',        # Parent with wildcard
        r'^\*$',             # Bare wildcard
        r'^\.$',             # Current directory (bare)
        r'^/usr(/.*)?$',     # System directories
        r'^/etc(/.*)?$',
        r'^/var(/.*)?$',
        r'^/boot(/.*)?$',
        r'^/sys(/.*)?$',
        r'^/proc(/.*)?$',
    ]
    
    # Check each path
    for path in paths:
        path = path.strip().strip('"\'')  # Remove quotes
        
        # Check for always dangerous patterns first
        for dangerous_pattern in always_dangerous_patterns:
            if re.match(dangerous_pattern, path):
                return True
        
        # Check if path is safe according to whitelist
        if not is_safe_rm_path(path):
            return True  # Block if not explicitly safe
    
    return False  # Allow if all paths are safe and none are dangerous

def is_env_file_access(tool_name, tool_input):
    """
    Check if any tool is trying to access .env files containing sensitive data.
    """
    if tool_name in ['Read', 'Edit', 'MultiEdit', 'Write', 'Bash']:
        # Check file paths for file-based tools
        if tool_name in ['Read', 'Edit', 'MultiEdit', 'Write']:
            file_path = tool_input.get('file_path', '')
            if '.env' in file_path and not file_path.endswith('.env.sample'):
                return True
        
        # Check bash commands for .env file access
        elif tool_name == 'Bash':
            command = tool_input.get('command', '')
            # Pattern to detect .env file access (but allow .env.sample)
            env_patterns = [
                r'\b\.env\b(?!\.sample)',  # .env but not .env.sample
                r'cat\s+.*\.env\b(?!\.sample)',  # cat .env
                r'echo\s+.*>\s*\.env\b(?!\.sample)',  # echo > .env
                r'touch\s+.*\.env\b(?!\.sample)',  # touch .env
                r'cp\s+.*\.env\b(?!\.sample)',  # cp .env
                r'mv\s+.*\.env\b(?!\.sample)',  # mv .env
            ]
            
            for pattern in env_patterns:
                if re.search(pattern, command):
                    return True
    
    return False

def main():
    try:
        # Read JSON input from stdin
        input_data = json.load(sys.stdin)
        
        tool_name = input_data.get('tool_name', '')
        tool_input = input_data.get('tool_input', {})
        
        # Check for .env file access (blocks access to sensitive environment files)
        if is_env_file_access(tool_name, tool_input):
            print("BLOCKED: Access to .env files containing sensitive data is prohibited", file=sys.stderr)
            print("Use .env.sample for template files instead", file=sys.stderr)
            sys.exit(2)  # Exit code 2 blocks tool call and shows error to Claude
        
        # Check for dangerous rm -rf commands
        if tool_name == 'Bash':
            command = tool_input.get('command', '')
            
            # Block rm -rf commands with comprehensive pattern matching
            if is_dangerous_rm_command(command):
                print("BLOCKED: Dangerous rm command detected and prevented", file=sys.stderr)
                sys.exit(2)  # Exit code 2 blocks tool call and shows error to Claude
        
        # Ensure log directory exists
        log_dir = Path.cwd() / 'logs'
        log_dir.mkdir(parents=True, exist_ok=True)
        log_path = log_dir / 'pre_tool_use.json'
        
        # Read existing log data or initialize empty list
        if log_path.exists():
            with open(log_path, 'r') as f:
                try:
                    log_data = json.load(f)
                except (json.JSONDecodeError, ValueError):
                    log_data = []
        else:
            log_data = []
        
        # Append new data
        log_data.append(input_data)
        
        # Write back to file with formatting
        with open(log_path, 'w') as f:
            json.dump(log_data, f, indent=2)
        
        sys.exit(0)
        
    except json.JSONDecodeError:
        # Gracefully handle JSON decode errors
        sys.exit(0)
    except Exception:
        # Handle any other errors gracefully
        sys.exit(0)

if __name__ == '__main__':
    main()