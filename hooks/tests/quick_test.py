#!/usr/bin/env python3
import sys
sys.path.insert(0, '/home/yoda/.claude/hooks')
from test_rm_logic import new_is_dangerous_rm_command

cmd = 'rm -rf /home/yoda/Library/Projects/VR/bubbles-game/bubble-test/android/.gradle'
result = new_is_dangerous_rm_command(cmd)
print(f'Command: {cmd}')
print(f'Blocked: {result}')
print('✅ Command should now be ALLOWED' if not result else '❌ Command still blocked')