import pickle
from pathlib import Path

from flask import Flask, request, jsonify, Blueprint
from wmd import WMD
from generate import embeddings_name, nbow_name, generate_nbow_entry

app = Flask(__name__)

bp = Blueprint('api', __name__, template_folder='templates')

embeddings = pickle.load( open(embeddings_name, 'rb') )
nbow = pickle.load( open(nbow_name, 'rb') )

@bp.route('/', methods=['POST'])
def get_cognate():
    if not request.is_json \
        or 'word' not in request.json \
        or 'lang' not in request.json:
        return jsonify({'status' : 'invalid'})
    target_word = request.json['word']
    target_language = request.json['lang']
    nbow[target_word] = generate_nbow_entry(target_word, language=target_language)
    calc = WMD(embeddings, nbow, vocabulary_min=2)
    words_and_scores = calc.nearest_neighbors(target_word)
    del nbow[target_word]
    return jsonify(words_and_scores)


app.register_blueprint(bp, url_prefix='/api/mnemonic')
