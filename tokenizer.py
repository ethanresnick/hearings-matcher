import re

# Convert string to lowercase, remove punctuation and split on space
def tokenize(text):
    # Convert all words to lower case
    processed_text = text.lower()

    # Remove punctuation
    processed_text = re.sub(ur'[\.\,\(\)\;\:\#\%\*\"\$\-\u201c\u201d]+', '', processed_text)

    # Replace atypical whitespace with a single space
    # Remove all numbers too.
    processed_text = re.sub(ur'[\r\t\n\d]+', ' ', processed_text)

    # Join ampersand separated words into a single unit
    processed_text = re.sub(ur' \& ', '&', processed_text)

    # Split to a list, filter empty tokens, and return
    return filter(lambda x: x != "", processed_text.split(" "))


#def TokenError():
#  pass
