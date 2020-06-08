import sys, io, pkgutil
from multiprocessing import Pool, Manager

import pickle
import pandas as pd
import numpy as np

from phonemizer.phonemize import phonemize
from panphon import FeatureTable

embeddings_name = 'embedding.p'
nbow_name = 'nbow.p'

# Generator to yield all results that we are going to generate
def build_phrases(words):
    short_popular_words = [ x for x in words[:len(words)//20] if len(x) < 5 ]
    num_phrases = len(words) * len(short_popular_words) * 2
    print(f"Number of phrases: {num_phrases}")
    for s in short_popular_words:
        for w in words:
            yield s + ' ' + w
            yield w + ' ' + s

ft = FeatureTable()

# Load embeddings
embeddings_csv = pkgutil.get_data('panphon', 'data/ipa_all.csv')
embeddings_pd = pd.read_csv( io.BytesIO(embeddings_csv), dtype=str )
# Pull out lookup column that contains the IPA strings
ipa_list = list(embeddings_pd['ipa'])

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

if __name__ == '__main__':
    # Load top 10,000 english words
    with open('top-10000.txt') as f:
        english_words = f.read().splitlines()

    # Find short words to compose with other words

    embeddings_pd = embeddings_pd.drop(['ipa'], axis='columns')
    # Values in the array are not numerical so we use this dict to convert them 
    numerical_values = {'-': -1, '0': 0, '+': 1}
    embeddings_np = embeddings_pd.applymap(lambda x: numerical_values[x]).to_numpy(dtype=np.float32)
    print(f"Saving embeddings to {embeddings_name}")
    pickle.dump( embeddings_np, open(embeddings_name, 'wb') )
    # Multiply by the subjective embeddings that come with panphon (so that not all features are worth the same
    # weights_np = np.array(ft.weights, dtype=np.float32)
    # embeddings_np = embeddings_np * weights_np

    print('Generating nbow')
    def generate_nbow_parallel(shared_dict, word):
        shared_dict[word] = generate_nbow_entry(word)
        print(f"Finished {word}")
    pool = Pool(16)
    manager = Manager()
# Create shared dictionary
    nbow = manager.dict()
# iterator that adds nbow to arguments of generator_nbow_parallel
    phrase_nbow_generator = ( (nbow, phrase) for phrase in build_phrases(english_words) )
    pool.starmap(
            generate_nbow_parallel,
            phrase_nbow_generator
            )
    print("Finished generating")
    pickle.dump( dict(nbow), open( nbow_name, "wb" ) )
    print(f"Saved to file {nbow_name}")
