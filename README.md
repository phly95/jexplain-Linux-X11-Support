# jexplain
Tool to quickly explain the usage of words in Japanese sentences by using Large Language models (Currently with GPT-4o-mini).

This Readme is a basic description of the program's functions.

## Setup
Before running the program, you'll need to set up the following environment variables for API keys:

* **OPENAI_API_KEY:** Your API key for OpenAI.
* **AZURE_SPEECH_API_KEY:** Your API key for Azure Speech service (optional, for text-to-speech functionality).

To run the program, simply execute the `jexplain.py` file with Python. 

## Global Keyboard Shortcuts:

* **Ctrl+Win+Z:** Explain the meaning of each word in the context of the sentence that is highlighted (autofocuses terminal window)
* **Ctrl+Win+A:** Ask a question to the AI
* **Ctrl+Win+Tab:** Translate the contents of the clipboard using ChatGPT
* **Ctrl+Win+-:** Aggressive translation. Uses chain of thought to generate a literary translation for difficult phrases.
* **Ctrl+Win+K:** Explain the meaning of each Kanji in the highlighted word.
* **Ctrl+Win+]:** Generate a mnemonic sentence with the highlighted text.
* **Ctrl+Win+::** Speak the highlighted Japanese text.
* **Ctrl+Win+F12:** Speak the highlighted English text. 
* **Ctrl+Win+[:** Change the copy mode. This is remembered next time you run the script. See copy_modes.py to see the modes. The mokuro mode works for reading manga btw.

## Functionality

* **Word Explanations:** The program uses the gpt-4o-mini language model API to provide context-specific definitions of Japanese words within sentences including furigana (furigana may contain inaccuracies) 
* **Kanji Breakdown:**  It can also explain the meaning of individual kanji characters within a word. 
* **Translation:**  OpenAI API is used to translate Japanese text into English.
* **Text-to-Speech:**  With the Azure Speech service, you can hear the pronunciation of highlighted Japanese or English text. 
* **Mnemonic Generation:**  The program can create mnemonic sentences using highlighted text to aid in memorization for JPDB.io Kanji pages.
* **AI language model Interaction:**  You can directly ask questions to the gpt-4o-mini language model API for a more conversational experience. The AI will forget everything for each question, so no back and forth chats.

## Additional Notes:

*  Ensure you have the required Python libraries installed (openai, keyboard, pyautogui, pyperclip, win32gui, win32console, azure-cognitiveservices-speech, json, os, time, mecab-python3).
* The program relies on keyboard shortcuts for activation.  
* It utilizes the clipboard for text input.  
* The terminal window is used for displaying outputs. 
* "pip install mecab-python3" should resolve the mecab dependency. Windows binary is here if that doesn't work: https://github.com/ikegami-yukino/mecab/releases . If it's still not working on Windows, see: https://stackoverflow.com/questions/63197703/mecab-importerror-dll-load-failed-the-specified-module-could-not-be-found
