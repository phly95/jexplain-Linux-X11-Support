# lin_keyboard.py

import platform
import threading
import time
import pyautogui

if platform.system() == 'Windows':
    import keyboard as kb
else:
    from pynput import keyboard

class LinKeyboard:
    def __init__(self):
        self.current_keys = set()
        self.combinations = {}
        self.listener = None
        self.is_running = False
        self.action_in_progress = False
        self.lock = threading.Lock()
        self.all_keys_released_event = threading.Event()  # Add this event

    def add_combination(self, keys, on_activate):
        if platform.system() == 'Windows':
            # Convert the set of keys to a string for Windows
            key_str = '+'.join(keys)
            self.combinations[key_str] = on_activate
        else:
            self.combinations[frozenset(keys)] = on_activate

    def _on_press(self, key):
        if self.action_in_progress:
            return

        with self.lock:
            key_str = self._get_key_str(key)
            self.current_keys.add(key_str)
            self.all_keys_released_event.clear()  # Clear the event when a key is pressed

            for combo, action in self.combinations.items():
                if combo.issubset(self.current_keys):
                    self.action_in_progress = True
                    threading.Thread(target=self._execute_action, args=(action,)).start()
                    break

    def _on_release(self, key):
        with self.lock:
            key_str = self._get_key_str(key)
            self.current_keys.discard(key_str)

            if not self.current_keys:  # Check if all keys are released
                self.all_keys_released_event.set()  # Set the event if all keys are released

        if key == keyboard.Key.esc:
            self.stop()
            return False

    def _execute_action(self, action):
        try:
            # Wait for all keys to be released before executing the action
            self.all_keys_released_event.wait()
            action()
        finally:
            self.action_in_progress = False

    def _get_key_str(self, key):
        try:
            return key.char.lower()
        except AttributeError:
            return str(key).split('.')[-1].lower()

    def start(self):
        if not self.is_running:
            self.is_running = True
            if platform.system() == 'Windows':
                self._start_windows()
            else:
                self.listener = keyboard.Listener(on_press=self._on_press, on_release=self._on_release)
                self.listener.start()

    def _start_windows(self):
        def check_keys():
            while self.is_running:
                time.sleep(0.05)
                for combo, action in self.combinations.items():
                    if all(kb.is_pressed(key) for key in combo.split('+')):
                        while any(kb.is_pressed(key) for key in combo.split('+')):
                            pass
                        action()

        self.listener = threading.Thread(target=check_keys)
        self.listener.start()

    def stop(self):
        if self.is_running:
            self.is_running = False
            if platform.system() == 'Windows':
                kb.unhook_all()
            else:
                if self.listener:
                    self.listener.stop()

    def join(self):
        if self.listener:
            self.listener.join()

    @staticmethod
    def simulate_key_press(key):
        pyautogui.press(key)

    @staticmethod
    def simulate_hotkey(*keys):
        pyautogui.hotkey(*keys)

def simulate_after_delay(delay, func, *args, **kwargs):
    def delayed_func():
        time.sleep(delay)
        func(*args, **kwargs)
    threading.Thread(target=delayed_func).start()
