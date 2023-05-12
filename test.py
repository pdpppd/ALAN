import re

def extract_sequence(text):
    match = re.search('[ACGT]+', text)
    if match:
        return match.group()
    else:
        return None

text = "do blast with this nt sequence TAGCTGATCGATCGATCGATCGTAGCTAGCTAGCTA"
sequence = extract_sequence(text)
print(sequence)  # prints: TACGATCGATCGATCGATCGA
