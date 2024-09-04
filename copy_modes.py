# copy_modes.py

import pyautogui
import time
import pyperclip

def no_copy():
    pass

def ctrl_c_copy():
    pyautogui.hotkey('ctrl', 'c')

def c_copy():
    pyautogui.hotkey('c')

def jpdb_copy():
    pyautogui.hotkey('ctrl', 'l')
    pyautogui.write("cs6767")
    time.sleep(0.1)
    pyautogui.press('enter')
    time.sleep(0.1)


def mokuro():
    # Select all and copy the text
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.1)
    pyautogui.hotkey('ctrl', 'c')

    # Retrieve the copied text from the clipboard
    copied_text = pyperclip.paste()

    # Split the text by lines
    lines = copied_text.splitlines()

    # Remove the line containing "Volume"
    modified_lines = [line for line in lines if line.strip() != "Volume"]

    # Join the lines back together
    modified_text = "\n".join(modified_lines)

    # Put the modified text back into the clipboard
    pyperclip.copy(modified_text)




# The custom copy is meant to be used with jpdb.io to copy the current sentence using a bookmarklet.
# It can be used with Firefox (not Chrome)

# Bookmark name: "copy sentence", Keyword: "cs6767", URL: "javascript:(function(){var e=document.querySelector("div.sentence");function t(e){let n="";for(const r of e.childNodes)r.nodeType===Node.TEXT_NODE?n+=r.textContent:r.tagName!==%22RT%22&&(n+=t(r));return%20n}navigator.clipboard.writeText(t(e)).then(()=%3E{console.log(%22Sentence%20copied!%22)},()=%3E{console.error(%22Copy%20failed%22)})})();"


copy_modes = [
    {"name": "No Copy", "function": no_copy},
    {"name": "Ctrl+C Copy", "function": ctrl_c_copy},
    {"name": "C Copy", "function": c_copy},
    {"name": "JPDB Copy", "function": jpdb_copy},
    {"name": "Mokuro", "function": mokuro}
]