from symspellpy import SymSpell

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

  