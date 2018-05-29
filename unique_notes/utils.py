def unique_word_count(text):
    text = text.lower()
    text = text.replace('\n', ' ')
    words_list = text.split(' ')
    return len(set(words_list))
