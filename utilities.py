from symspellpy import SymSpell
from base64 import b64decode, b64encode
import cv2 as cv
import numpy as np
DICTIONARY_PATH = './assets/frequency_dictionary_en_82_765.txt'
BIGRAM_PATH = './assets/frequency_bigramdictionary_en_243_342.txt'

sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)
sym_spell.load_dictionary(DICTIONARY_PATH, term_index=0, count_index=1)
sym_spell.load_bigram_dictionary(BIGRAM_PATH, term_index=0, count_index=2)

def spell_check(texts):

  misspelled = []
  for idx, text in enumerate(texts):
    # max edit distance per lookup (per single word, not per whole input string)
    suggestions = sym_spell.lookup_compound(text, max_edit_distance=0, transfer_casing=False)
    # display suggestion term, edit distance, and term frequency
    if suggestions:
      texts[idx] = suggestions[0]._term

  
def encode(image = [], images = []):
	if len(image) != 0:
		_, buffer = cv.imencode(".png", image)
		return b64encode(buffer).decode('utf-8')
	elif len(images) != 0:
		temp = []
		for image in images:
			if len(image) > 5:
				_, buffer = cv.imencode(".png", image)
				temp.append(b64encode(buffer).decode('utf-8'))
		return temp
	else:
		return None

def decode(image_raw):
  if image_raw is None or len(image_raw) == 0:
    return None
  image_bytes = b64decode(image_raw)
  return cv.imdecode(np.frombuffer(image_bytes, np.uint8), -1)