import re


def split_words_with_underscore(string) -> str:
    """ Create __tablename__ with sqlalchemy. """

    words = []
    current_word = ''

    for char in string:
        if char.isupper():
            words.append(current_word)
            current_word = char.lower()
        else:
            current_word += char

    words.append(current_word)

    return '_'.join(words[1:])


def remove_html_tags(text):
    pattern = r'<.*?>'
    cleaned_text = re.sub(pattern, '', text)
    return cleaned_text
