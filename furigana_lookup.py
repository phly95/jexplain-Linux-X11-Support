import MeCab
import re

def katakana_to_hiragana(katakana):
    """Convert katakana to hiragana."""
    hiragana = ''
    for char in katakana:
        code = ord(char)
        if 0x30A1 <= code <= 0x30F6:
            hiragana += chr(code - 0x60)
        else:
            hiragana += char
    return hiragana

def is_hiragana_only(word):
    """Check if a word consists only of hiragana characters."""
    return all(0x3040 <= ord(char) <= 0x309F for char in word)

def get_furigana(sentence):
    # Remove punctuation
    sentence = re.sub(r'[^\w\s]', '', sentence)

    # Initialize MeCab
    mecab = MeCab.Tagger()

    # Parse the sentence
    parsed = mecab.parse(sentence)

    # Split the parsed output into lines
    lines = parsed.split('\n')

    # Initialize a list to store the results
    results = []

    # Iterate through the lines
    for line in lines:
        if line == 'EOS' or line == '':
            continue

        # Split the line into components
        components = line.split('\t')
        if len(components) < 2:
            continue

        word = components[0]
        features = components[1].split(',')

        if len(features) < 8:
            continue

        # Extract the furigana
        furigana = features[7]

        # Convert furigana from katakana to hiragana
        furigana = katakana_to_hiragana(furigana)

        # Skip hiragana-only words
        if is_hiragana_only(word):
            continue

        # Append the result to the list
        results.append((word, furigana))

    return results

def print_furigana(results):
    for word, furigana in results:
        print(f"- {word}【{furigana}】")

if __name__ == "__main__":
    sentence = "この存在は太古の昔に葬られており、今は知る者もほとんどいません。"
    results = get_furigana(sentence)
    print_furigana(results)
