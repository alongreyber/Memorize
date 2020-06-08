from flask import Flask, request
app = Flask(__name__)

import pickle

from pathlib import Path
from generate import embeddings_name, nbow_name, generate_nbow_entry
from wmd import WMD

if not Path(embeddings_name).exists():
    raise Exception("Embeddings not found")
if not Path(nbow_name).exists():
    raise Exception("NBOW not found")

embeddings = pickle.load( open(embeddings_name, 'rb') )
nbow = pickle.load( open(nbow_name, 'rb') )

@app.route('/', methods=['POST'])
def get_cognate():
    if not request.is_json() or 'word' not in request.json:
        return jsonify({'status' : 'invalid'})
    spanish_word = request.json['word']
    nbow[spanish_word] = generate_nbow_entry(spanish_word, language='es')
    calc = WMD(embeddings_np, nbow, vocabulary_min=2)
    words_and_scores = calc.nearest_neighbors(spanish_word)
    del nbow[spanish_word]
    return jsonify(words_and_scores)
