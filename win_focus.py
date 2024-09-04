import os
import re
import sys
import shutil
import pyautogui

# Platform-specific imports
if os.name == 'nt':
    import win32gui
    import win32console
    import msvcrt
else:
    import subprocess
    import fcntl
    import termios
    import signal

def winfocus(title):
    if os.name == 'nt':
        pyautogui.press("alt")
        w.find_window_wildcard(".*jexplain_window.*")
        w.set_foreground()
    else:
        if shutil.which("xdotool"):
            try:
                subprocess.run(["xdotool", "search", "--name", title, "windowfocus"], check=True)
            except subprocess.CalledProcessError:
                print(f"Failed to focus window: {title}")
        else:
            print("xdotool is not installed. Window focusing will not work on Linux.")

def set_title(title):
    if os.name == 'nt':
        win32console.SetConsoleTitle(title)
    else:
        sys.stdout.write(f"\x1b]2;{title}\x07")

def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def print_bottom(text):
    sys.stdout.write("\033[J")  # Clear everything below the cursor
    sys.stdout.write("\033[999;1H")  # Move cursor to the last line
    print(text, end="")

def clear_input_buffer():
    if os.name == 'nt':
        while msvcrt.kbhit():
            msvcrt.getch()
    else:
        termios.tcflush(sys.stdin, termios.TCIOFLUSH)

class WindowMgr:
    """Encapsulates some calls to the winapi for window management"""

    def __init__(self):
        """Constructor"""
        self._handle = None

    def find_window(self, class_name, window_name=None):
        """find a window by its class_name"""
        if os.name == 'nt':
            self._handle = win32gui.FindWindow(class_name, window_name)
        else:
            if shutil.which("xdotool"):
                try:
                    self._handle = subprocess.check_output(["xdotool", "search", "--name", window_name]).strip()
                except subprocess.CalledProcessError:
                    print(f"Failed to find window: {window_name}")
                    self._handle = None
            else:
                print("xdotool is not installed. Window management will not work on Linux.")
                self._handle = None

    def _window_enum_callback(self, hwnd, wildcard):
        """Pass to win32gui.EnumWindows() to check all the opened windows"""
        if os.name == 'nt':
            if re.match(wildcard, str(win32gui.GetWindowText(hwnd))) is not None:
                self._handle = hwnd

    def find_window_wildcard(self, wildcard):
        """find a window whose title matches the wildcard regex"""
        if os.name == 'nt':
            self._handle = None
            win32gui.EnumWindows(self._window_enum_callback, wildcard)
        else:
            if shutil.which("xdotool"):
                try:
                    self._handle = subprocess.check_output(["xdotool", "search", "--name", wildcard]).strip()
                except subprocess.CalledProcessError:
                    print(f"Failed to find window matching: {wildcard}")
                    self._handle = None
            else:
                print("xdotool is not installed. Window management will not work on Linux.")
                self._handle = None

    def set_foreground(self):
        """put the window in the foreground"""
        if os.name == 'nt':
            win32gui.SetForegroundWindow(self._handle)
        else:
            if shutil.which("xdotool") and self._handle:
                try:
                    subprocess.run(["xdotool", "windowfocus", self._handle], check=True)
                except subprocess.CalledProcessError:
                    print("Failed to set window focus")
            else:
                print("xdotool is not installed or window handle is invalid. Cannot set foreground on Linux.")

w = WindowMgr()