import json

from waitress import serve
from pyramid.config import Configurator
from pyramid.view import view_config

from nltk.corpus import wordnet as wn


POS_MAP = {
    'n': wn.NOUN,
    'v': wn.VERB,
    'a': wn.ADJ,
    'd': wn.ADV,
}

def hello_world(request):
    word = request.GET.get('q', None)
    pos = request.GET.get('p', None)
    meaning = get_nltk_meaning(word, pos)
    return {word: meaning}


def get_pos(pos):
    return POS_MAP.get(pos, None)

def get_nltk_meaning(word, pos):
    meanings = []
    for sense in wn.synsets(word, pos=get_pos(pos)):
        meanings.append(sense.definition())
    return meanings


if __name__ == '__main__':
    with Configurator() as config:
        config.add_route('hello', '/')
        config.add_view(hello_world, route_name='hello', renderer='json')
        app = config.make_wsgi_app()
    serve(app, host='0.0.0.0', port=6543)

