'''Api.py'''
import requests

URL_API = 'https://python.gel.ulaval.ca/quoridor/api/'


def lister_parties(idul):
    ''' Lister les parties.'''
    reponse = requests.get(URL_API + 'lister/', params={'idul': idul})
    if reponse.status_code == 200:
        value = reponse.json()
        return list(map(lambda x: x['id'], value['parties']))
    raise RuntimeError(value['message'])


def initialiser_partie(idul):
    '''Initialiser la partie'''
    rep = requests.post(URL_API + 'initialiser/', data={'idul': idul})
    rep = rep.json()
    if 'message' in rep:
        raise RuntimeError(rep['message'])
    return rep['id'], rep['état']


def jouer_coup(id, type, pos):
    '''Jouer un coup'''
    reponse = requests.post(URL_API + 'jouer/', data={'id':id, 'type':type, 'pos':pos})
    reponse = reponse.json()
    if 'message' in reponse:
        raise RuntimeError(reponse['message'])
    elif 'gagnant' in reponse:
        raise StopIteration(reponse["gagnant"])
    return reponse['état']

