import ctypes
import sys
from ctypes import wintypes
from typing import List

# Constants for volume control
APPCOMMAND_VOLUME_MUTE = 0x80000
APPCOMMAND_VOLUME_UP = 0xA0000
APPCOMMAND_VOLUME_DOWN = 0x90000

# Load user32.dll for sending system commands
user32 = ctypes.WinDLL('user32', use_last_error=True)

def send_app_command(hwnd, app_command):
    """Send an app command to control system audio."""
    user32.SendMessageW(hwnd, 0x319, 0, app_command)

def get_hwnds_for_pid(pid):
    """Return a list of window handles (hwnd) for a given process ID."""
    def callback(hwnd, hwnds):
        if ctypes.windll.user32.IsWindowVisible(hwnd):
            _, found_pid = ctypes.wintypes.DWORD(), ctypes.wintypes.DWORD()
            ctypes.windll.user32.GetWindowThreadProcessId(hwnd, ctypes.byref(found_pid))
            if found_pid.value == pid:
                hwnds.append(hwnd)
        return True

    hwnds = []
    ctypes.windll.user32.EnumWindows(ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.wintypes.HWND, ctypes.POINTER(ctypes.c_void_p))(callback), ctypes.byref(ctypes.create_string_buffer(0)))
    return hwnds

def set_volume(action: str):
    """Set the volume of the system."""
    hwnds = get_hwnds_for_pid(0)  # 0 is a special value for system-wide settings
    for hwnd in hwnds:
        if action == 'mute':
            send_app_command(hwnd, APPCOMMAND_VOLUME_MUTE)
        elif action == 'up':
            send_app_command(hwnd, APPCOMMAND_VOLUME_UP)
        elif action == 'down':
            send_app_command(hwnd, APPCOMMAND_VOLUME_DOWN)

def main():
    """Main function to parse command-line arguments and control volume."""
    if len(sys.argv) != 2 or sys.argv[1] not in ('mute', 'up', 'down'):
        print("Usage: smartflow.py [mute|up|down]")
        sys.exit(1)

    action = sys.argv[1]
    set_volume(action)
    print(f"Volume {action} command sent.")

if __name__ == '__main__':
    main()