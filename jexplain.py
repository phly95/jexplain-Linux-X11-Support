# jexplain.py

import os
import json
import time
import pyperclip
import pyautogui
from lin_keyboard import LinKeyboard, simulate_after_delay
from copy_modes import copy_modes
from jp_process import jp_process, jp_process_lite, chat_with, kj_process, tr_process, tr_agressive, mnemonic_process, speak
from win_focus import set_title, winfocus, clear_screen, clear_input_buffer
import subprocess
import threading

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
config_dir = os.path.join(script_dir, 'config')
os.makedirs(config_dir, exist_ok=True)

# Path to the file storing the current copy mode
copy_mode_file = os.path.join(config_dir, 'current_copy_mode.json')

# Load the current copy mode
def load_copy_mode():
    if os.path.exists(copy_mode_file):
        with open(copy_mode_file, 'r') as f:
            return json.load(f)['mode']
    return 0  # Default to no_copy

# Save the current copy mode
def save_copy_mode(mode):
    with open(copy_mode_file, 'w') as f:
        json.dump({'mode': mode}, f)

# Initialize the current copy mode
current_copy_mode = load_copy_mode()

# Initialize the LinKeyboard
lin_kb = LinKeyboard()

def force_current_focus(): # Workaround to fix X11 focus issues.
    # Get the ID of the currently active window
    active_window_id = get_active_window_id()

    # Ensure the original window is in focus (X11 focus loss workaround)
    winfocus("jexplain_window")
    time.sleep(0.1)
    focus_window(active_window_id)

def get_active_window_id():
    return subprocess.check_output(["xdotool", "getactivewindow"]).decode().strip()

def focus_window(window_id):
    subprocess.run(["xdotool", "windowactivate", window_id])

def on_ctrl_win_z():
    clear_screen()

    # force_current_focus()

    # Perform the copy operation
    copy_modes[current_copy_mode]['function']()  # Execute the current copy mode

    # Switch back to the jexplain window
#     winfocus("jexplain_window")

    # Process the copied content
    jp_process_lite()

    print("\n***\n", end="")

def on_ctrl_win_bracket_right():
    clear_screen()

    force_current_focus()

    pyautogui.hotkey('ctrl', 'c')
    winfocus("jexplain_window")
    mnemonic = mnemonic_process()
    pyperclip.copy(mnemonic)
    print("\n***\n", end="")

def on_ctrl_win_bracket_left():
    global current_copy_mode
    current_copy_mode = (current_copy_mode + 1) % len(copy_modes)
    save_copy_mode(current_copy_mode)
    print(f"Copy mode changed to: {copy_modes[current_copy_mode]['name']}")

def on_ctrl_win_x():
    # force_current_focus()
    copy_modes[current_copy_mode]['function']()
    speak('ja-JP-ShioriNeural')
    print("***\n", end="")

def on_ctrl_win_f12():
    force_current_focus()
    simulate_after_delay(0.1, LinKeyboard.simulate_hotkey, 'ctrl', 'c')
    speak('en-US-AvaNeural')
    print("***\n", end="")

def on_ctrl_win_a():
    clear_input_buffer()
    chat_with(input("\nAsk a question: "))
    print("\n***\n", end="")

def on_ctrl_win_tab():
    tr_process()
    print("\n***\n", end="")

def on_ctrl_win_equals():
    tr_agressive()
    print("\n***\n", end="")

def on_ctrl_win_k():
    print("Kanji Explanation:")
    kj_process()
    print("\n***\n", end="")

# Add key combinations
lin_kb.add_combination({'ctrl', 'cmd', 'z'}, on_ctrl_win_z)
lin_kb.add_combination({'ctrl', 'cmd', ']'}, on_ctrl_win_bracket_right)
lin_kb.add_combination({'ctrl', 'cmd', '['}, on_ctrl_win_bracket_left)
lin_kb.add_combination({'ctrl', 'cmd', 'x'}, on_ctrl_win_x)
lin_kb.add_combination({'ctrl', 'cmd', 'f12'}, on_ctrl_win_f12)
lin_kb.add_combination({'ctrl', 'cmd', 'a'}, on_ctrl_win_a)
lin_kb.add_combination({'ctrl', 'cmd', 'tab'}, on_ctrl_win_tab)
lin_kb.add_combination({'ctrl', 'cmd', '='}, on_ctrl_win_equals)
lin_kb.add_combination({'ctrl', 'cmd', 'k'}, on_ctrl_win_k)

def monitor_clipboard():
    previous_clipboard_content = pyperclip.paste()
    identifier = "[MPV]"
    while True:
        time.sleep(0.05)  # Adjust the sleep interval as needed
        current_clipboard_content = pyperclip.paste()
        if current_clipboard_content != previous_clipboard_content:
            if current_clipboard_content.startswith(identifier):
                # Remove the identifier
                processed_content = current_clipboard_content[len(identifier):].strip()
                previous_clipboard_content = current_clipboard_content
                pyperclip.copy(processed_content)
                on_ctrl_win_z()
                # Optionally, update the clipboard with the processed content
                # pyperclip.copy(processed_content)

# Main execution
if __name__ == "__main__":
    set_title("jexplain_window")
    print("Ready for scanning")

    # Start listening for key events
    lin_kb.start()

    # Start clipboard monitoring thread
    clipboard_thread = threading.Thread(target=monitor_clipboard, daemon=True)
    clipboard_thread.start()

    try:
        # Keep the script running
        while True:
            time.sleep(0.05)
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        # Stop listening for key events
        lin_kb.stop()
