import pyperclip
from chat_stream import chat_stream
import asyncio
import subprocess
import re
import azure.cognitiveservices.speech as speechsdk
import os
from furigana_lookup import get_furigana, print_furigana

def jp_process():
    japanese_sentence = pyperclip.paste().replace('\n', '').replace('\r', '')
    bprompt = f'''
Translate and break down this Japanese sentence:
<japanese_sentence>
{japanese_sentence}
</japanese_sentence>

Format:
English Translation: [Full sentence translation]

Breakdown:
- [Word or Phrase]【ふりがな】: Context-specific definition

Rules:
1. Include particles within larger phrases when appropriate
2. Use original word forms
3. Always use 【ふりがな】, even for hiragana
4. Only hiragana in 【】
5. One 【】 per lexical unit (word or meaningful phrase)
6. Keep idiomatic expressions and set phrases together (e.g., 何かの縁)
7. No explanations outside format
8. No spaces in ふりがな

Examples of phrases to keep together:
- 何かの縁【なにかのえん】
- ここまで【ここまで】
- であろう【であろう】
    '''
    # print(bprompt)
    print("Sentence: " + japanese_sentence + "\n")
    asyncio.run(chat_stream(bprompt))

def jp_process_lite():
    japanese_sentence = pyperclip.paste().replace('\n', '').replace('\r', '')
    bprompt = f'''Example:
Japanese Sentence: 私は学生です。

English Translation: I am a student.

Breakdown:
- 私: I
- は: topic marker
- 学生: student
- です: am

Format:
English Translation: [Full sentence translation]

Breakdown:
- [Word]: Context-specific definition

Rules:
1. Include particles.
2. Use original word forms.
3. Include the entire sentence (excluding punctuation) in the breakdown.
4. Do not add any words that are not in the original sentence.
5. Provide the response in plain text format without any formatting (no bold, italics, etc.).
6. Do not provide transliterations, phonetic spellings, romanizations, alphabetizations, or phonetic representations.
7. Keep definitions short, under 3 words.

Translate and break down this Japanese sentence:
{japanese_sentence}'''
    # print(bprompt)
    print("Sentence: " + japanese_sentence + "\n")
        # Get furigana for the sentence
    results = get_furigana(japanese_sentence)
    print("Furigana:")
    print_furigana(results)
    print("")
    asyncio.run(chat_stream(bprompt))

def extract_kanji(text):
    # Use regular expression to find all kanji characters
    kanji_pattern = re.compile(r'[\u4e00-\u9fff]')
    return kanji_pattern.findall(text)

def kj_process():
    input_text = pyperclip.paste().replace('\n', '').replace('\r', '')
    kanji_list = extract_kanji(input_text)
    kanji_string = ', '.join(kanji_list)

    # Append the list of kanji to the input text if there are any kanji characters
    if kanji_list:
        input_text += f" (kanji: {kanji_string})"

    bprompt = f"What does each kanji in the word「{input_text}」 mean? Use the format of \n```\nThe individual kanji for <word> are:\n\n- <kanji> means <define>. In this context, <explain>.\n```"
    # print(bprompt)
    asyncio.run(chat_stream(bprompt))

def mnemonic_process():
    text = pyperclip.paste()
    # Split the text into lines
    lines = text.splitlines()

    # Find the index of the "Info" line
    info_index = lines.index('Info')

    # Join the lines before "Info" into a single string
    result = ', '.join(lines[:info_index])
    main_word = result

    # Find the "Composed of" line and join the following lines into a single string,
    # removing any non-ASCII characters and leading/trailing whitespace
    composed_index = info_index + 1
    while not lines[composed_index].startswith('Composed of'):
        composed_index += 1
    composed_parts = [part for part in (re.sub(r'[^\x00-\x7F]+', '', line.strip()) for line in lines[composed_index+1:]) if part]
    if result:
        result += '; '
    result += ', '.join(composed_parts)
    # bprompt = f'Write a sentence using the following words: {result}. Each word listed should be bolded using markdown (surrounded by two asterisks "**"), except the main word, {main_word} should be surrounded by three asterisks, like so: "***{main_word}***".'
    bprompt = f'''Instructions:
1. Create a single, coherent, and meaningful sentence using ALL and ONLY the words provided in the "Word list" below.
2. The sentence must make logical sense.
3. Do not add, remove, or substitute any words from the given list.
4. Write the sentence first without any formatting.
5. Then, rewrite the same sentence with the following formatting:
   - The main word (specified separately) should be wrapped in triple asterisks: ***main_word***
   - All other words from the provided list should be wrapped in double asterisks: **word**
   - Words not from the list should remain unformatted.

Example:
Word list: argument; say, sloped roof, volume (of a book)
Main word: argument

Example Output:
Unformatted sentence:
I wanted to say there's something wrong about having a sloped roof, but a volume of a book I read invalidated any argument.

Formatted sentence:
I wanted to **say** there's something wrong about having a **sloped roof**, but a **volume** of a book I read invalidated any ***argument***.

Now, please follow the instructions for the following:

Word list: {result}
Main word: {main_word}'''
    # print(bprompt)
    mnemonic = asyncio.run(chat_stream(bprompt))
    return mnemonic

def tr_process():
    japanese_sentence = pyperclip.paste().replace('\n', '').replace('\r', '')
    bprompt = f"Translate this to English:「{japanese_sentence}」. Respond with only the translation without using quotation marks."
    translation = asyncio.run(chat_stream(bprompt))
    return translation

def tr_agressive():
    japanese_sentence = pyperclip.paste().replace('\n', '').replace('\r', '')
    bprompt = f"Break down the sentence and how it may not be a literal translation, then determine the literal and literary translation in English of this: {japanese_sentence}" # Example: 抵抗のできない僕はのけぞるようにして宙を舞う。
    translation = asyncio.run(chat_stream(bprompt))
    return translation

def chat_with(question):
    asyncio.run(chat_stream(question))

def speak(voice):
    japanese_sentence = pyperclip.paste().replace('\n', '').replace('\r', '')
    # This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
    speech_config = speechsdk.SpeechConfig(subscription=os.environ.get("AZURE_SPEECH_API_KEY"), region="eastus")
    audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)

    # The language of the voice that speaks.
    speech_config.speech_synthesis_voice_name=voice#Shiori, Aoi

    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

    # Get text from the console and synthesize to the default speaker.
    speech_synthesis_result = speech_synthesizer.speak_text_async(japanese_sentence).get()

    if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesized for text [{}]".format(japanese_sentence))
    elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_synthesis_result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            if cancellation_details.error_details:
                print("Error details: {}".format(cancellation_details.error_details))
                print("Did you set the speech resource key and region values?")

def process_exists(process_name):
    call = 'TASKLIST', '/FI', 'imagename eq %s' % process_name
    # use buildin check_output right away
    output = subprocess.check_output(call).decode()
    # check in last line for process name
    last_line = output.strip().split('\r\n')[-1]
    # because Fail message could be translated
    return last_line.lower().startswith(process_name.lower())