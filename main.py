import sys, io, pkgutil
from pathlib import Path
from multiprocessing import Pool, Manager

import pickle
import pandas as pd
import numpy as np

from phonemizer.phonemize import phonemize
from panphon import FeatureTable
from wmd import WMD

# Generate lookup table of english pronunciations
with open('top-10000.txt') as f:
    english_words = f.read().splitlines()

short_popular_words = [ x for x in english_words[:len(english_words)//10] if len(x) < 5 ]
num_phrases = len(english_words) * len(short_popular_words) * 2

print(f"Number of phrases to add: {num_phrases}")

def english_phrases():
    for s in short_popular_words:
        for w in english_words:
            yield s + ' ' + w
            yield w + ' ' + s

ft = FeatureTable()

# Load embeddings and save to pandas
embeddings_csv = pkgutil.get_data('panphon', 'data/ipa_all.csv')
embeddings_pd = pd.read_csv( io.BytesIO(embeddings_csv), dtype=str )
# Pull out lookup column that contains the IPA strings
ipa_list = list(embeddings_pd['ipa'])
embeddings_pd = embeddings_pd.drop(['ipa'], axis='columns')
# Values in the array are not numerical so we use this dict to convert them 
numerical_values = {'-': -1, '0': 0, '+': 1}
embeddings_np = embeddings_pd.applymap(lambda x: numerical_values[x]).to_numpy(dtype=np.float32)
# Multiply by the subjective embeddings that come with panphon (so that not all features are worth the same
# weights_np = np.array(ft.weights, dtype=np.float32)
# embeddings_np = embeddings_np * weights_np

def generate_nbow_entry(word, language='en-us'):
    # Create IPA representation
    ipa = phonemize(word, language=language, backend='espeak')
    # Cut out spaces
    ipa = ipa.replace(' ', '')
    # Use utility to find a list of segments (because some segments are multiple characters) 
    segs = ft.ipa_segs(ipa)
    # This array is a list of indicies into the embeddings
    segments_index = [ ipa_list.index(c) for c in segs ]
    # Nbow is in a strange format
    return (word, segments_index, np.ones(len(segs),dtype=np.float32) )

def generate_nbow_parallel(shared_dict, word):
    shared_dict[word] = generate_nbow_entry(word)
    print(f"{ (len(shared_dict.keys()) / num_phrases)*100 }% done")

if not Path('nbow.p').exists():
    pool = Pool(16)
    manager = Manager()
    # Create shared dictionary
    nbow = manager.dict()
    # iterator that adds nbow to arguments of generator_nbow_parallel
    phrase_nbow_generator = ( (nbow, phrase) for phrase in english_phrases() )
    pool.starmap(
            generate_nbow_parallel,
            phrase_nbow_generator
            )
    pickle.dump( dict(nbow), open( "nbow.p", "wb" ) )
else:
    nbow = pickle.load( open( "nbow.p", "rb" ) )

spanish_word = next(sys.stdin).rstrip()
nbow[spanish_word] = generate_nbow_entry(spanish_word, language='es')
calc = WMD(embeddings_np, nbow, vocabulary_min=2)

for word, score in calc.nearest_neighbors(spanish_word):
    print(f"{word.ljust(10)}:{score}")
