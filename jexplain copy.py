import os
import json
from copy_modes import copy_modes

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



from jp_process import jp_process, jp_process_lite, chat_with, kj_process, tr_process, tr_agressive, mnemonic_process, speak#, screen_process
from win_focus import set_title, winfocus, clear_screen, clear_input_buffer
import keyboard
import pyautogui
import time
import pyperclip

set_title("jexplain_window")
print("Ready for scanning")
while True:
        time.sleep(0.05)
        if keyboard.is_pressed('ctrl+win+z'):
                while keyboard.is_pressed('ctrl') or keyboard.is_pressed('win') or keyboard.is_pressed('\\'): #wait until keys are released
                        pass
                clear_screen()
                
                copy_modes[current_copy_mode]['function']()  # Execute the current copy mode

                # winfocus("jexplain_window")
                jp_process_lite()
                print("\n***\n", end="")
        if keyboard.is_pressed('ctrl+win+]'):
                while keyboard.is_pressed('ctrl') or keyboard.is_pressed('win') or keyboard.is_pressed(']'): #wait until keys are released
                        pass
                clear_screen()
                #print("Engaged")
                pyautogui.hotkey('ctrl','c')# 
                winfocus("jexplain_window")
                mnemonic = mnemonic_process()
                pyperclip.copy(mnemonic)
                #winfocus("jexplain_window")
                print("\n***\n", end="")
        if keyboard.is_pressed('ctrl+win+['):
                while keyboard.is_pressed('ctrl') or keyboard.is_pressed('win') or keyboard.is_pressed('['): #wait until keys are released
                        pass
                current_copy_mode = (current_copy_mode + 1) % len(copy_modes)
                save_copy_mode(current_copy_mode)
                print(f"Copy mode changed to: {copy_modes[current_copy_mode]['name']}")
        if keyboard.is_pressed('ctrl+win+x'):
                while keyboard.is_pressed('ctrl') or keyboard.is_pressed('win') or keyboard.is_pressed('x'): #wait until keys are released
                        pass
                # print("Speaking")

                copy_modes[current_copy_mode]['function']()  # Execute the current copy mode

                speak('ja-JP-ShioriNeural')
                print("***\n", end="")
        if keyboard.is_pressed('ctrl+win+f12'):
                while keyboard.is_pressed('ctrl') or keyboard.is_pressed('win') or keyboard.is_pressed('f12'): #wait until keys are released
                        pass
                # print("Speaking")
                time.sleep(0.1)
                pyautogui.hotkey('ctrl','c')# 
                speak('en-US-AvaNeural')
                print("***\n", end="")
        elif keyboard.is_pressed('ctrl+win+a'):
                while keyboard.is_pressed('ctrl') or keyboard.is_pressed('win') or keyboard.is_pressed('a'): #wait until keys are released
                        pass
                clear_input_buffer()
                chat_with(input("\nAsk a question: "))
                print("\n***\n", end="")
        elif keyboard.is_pressed('ctrl+win+tab'):
                while keyboard.is_pressed('ctrl') or keyboard.is_pressed('win') or keyboard.is_pressed('tab'): #wait until keys are released
                        pass
                # pyautogui.hotkey('ctrl', 'c')
                tr_process()
                print("\n***\n", end="")
        elif keyboard.is_pressed('ctrl+win+='):
                while keyboard.is_pressed('ctrl') or keyboard.is_pressed('win') or keyboard.is_pressed('='): #wait until keys are released
                        pass
                # pyautogui.hotkey('ctrl', 'c')
                tr_agressive()
                print("\n***\n", end="")
        elif keyboard.is_pressed('ctrl+win+k'):
                while keyboard.is_pressed('ctrl') or keyboard.is_pressed('win') or keyboard.is_pressed('k'): #wait until keys are released
                        pass
                kj_process()
                print("\n***\n", end="")
