import panphon
import panphon.distance
from phonemizer.phonemize import phonemize
import pickle
from pathlib import Path
import sys

english_words = ['gruyere', 'children', 'respect']

dst = panphon.distance.Distance()

# Generate lookup table of english pronunciations
def gen_phonemes():
    with open('top-10000.txt') as f:
        english_words = f.read().splitlines()
    english_phonemes = {}
    num_words = 10000
    for i in range(num_words):
        e = english_words[i]
        english_phonemes[e] = phonemize(e, language='en-us', backend='espeak')
        print(f"{ (i / num_words) * 100 }% done")
    pickle.dump( english_phonemes, open( "english_phonemes.p", "wb" ) )

if not Path('english_phonemes.p').exists():
    gen_phonemes()
english_phonemes = pickle.load( open( "english_phonemes.p", "rb" ) )

spanish_word = next(sys.stdin).rstrip()
# spanish_word = 'bolígrafo'
spanish_ipa = phonemize(spanish_word, language='es', backend='espeak')

english_matches = {}
for english_word, english_ipa in english_phonemes.items():
    english_matches[english_word] = dst.jt_weighted_feature_edit_distance_div_maxlen(english_ipa, spanish_ipa)

N = 100
res = dict(sorted(english_matches.items(), key=lambda x: x[1])[:N])

for word, similarity in res.items():
    print(f"{word[:-1].ljust(10)}: {similarity}")
