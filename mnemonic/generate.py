import sys, io, pkgutil
from p_tqdm import p_map

import pickle
import pandas as pd
import numpy as np

from phonemizer.phonemize import phonemize
from panphon import FeatureTable

embeddings_name = 'embedding.p'
nbow_name = 'nbow.p'

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
    return word, segments_index, np.ones(len(segs),dtype=np.float32)

if __name__ == '__main__':
    # Load top 10,000 english words
    with open('top-10000.txt') as f:
        english_words = f.read().splitlines()

    embeddings_pd = embeddings_pd.drop(['ipa'], axis='columns')
    # Values in the array are not numerical so we use this dict to convert them 
    numerical_values = {'-': -1, '0': 0, '+': 1}
    embeddings_np = embeddings_pd.applymap(lambda x: numerical_values[x]).to_numpy(dtype=np.float32)
    print(f"Saving embeddings to {embeddings_name}")
    pickle.dump( embeddings_np, open(embeddings_name, 'wb') )
    # Multiply by the subjective embeddings that come with panphon (so that not all features are worth the same
    # weights_np = np.array(ft.weights, dtype=np.float32)
    # embeddings_np = embeddings_np * weights_np

    print("Generating NBOW")
    nbow_list = p_map(generate_nbow_entry, english_words)
    # To make a dictionary, build a new list with the word name as the key
    nbow = dict( ((nbow[0],nbow) for nbow in nbow_list) )
    print("Finished generating")
    pickle.dump( dict(nbow), open( nbow_name, "wb" ) )
    print(f"Saved to file {nbow_name}")
