from codecs import open
from gamer import stations
from json import loads, dumps

def get_stations():
    with open(stations, 'r', encoding='utf-8') as f:
        return loads(f.read())    

def rewrite_stations(dic):
    with open(stations, 'w', encoding='utf-8') as f:
        f.write(dumps(dic))

def add_station(name, parents, ty):
    name = name.lower().strip()
    if len(parents) == 0:
        parents = []
    else:
        parents = [n.lower().strip() for n in parents.split(',')]
    stations = get_stations()
    stations[name] = {'type': ty, 'parents': parents, 'keys': {}}
    rewrite_stations(stations)

def add_key(station, key, res):
    station = station.lower().strip()
    stations = get_stations()
    stations[station]['keys'][key.strip()] = res
    rewrite_stations(stations)

def del_station(station):
    stations = get_stations()
    try:
        del stations[station]
    except KeyError:
        pass
    rewrite_stations(stations)
