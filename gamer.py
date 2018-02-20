from codecs import open
from json import dumps, loads
import os

teams = os.path.join(os.path.dirname(__file__), 'teams.txt')
stations = os.path.join(os.path.dirname(__file__), 'stations.txt')


def get_teams():
    with open(teams, 'r', encoding='utf-8') as f:
        text = f.read()
    return loads(text)['teams']

def get_statistics():
    teams = get_teams()
    new = []
    for n in teams:
        n['res'] = get_res(n['stations'])
        n['able'] = get_able_stations(n['stations'])
        new.append(n)
    return new

def get_res(stations):
    res = {'s': 0, 'n': 0, 'p': 0, 'c': 0, 'm': 0}
    for n in res:
        res[n] = sum([st['res'].get(n, 0) for st in stations])
    return res

def get_team(login):
    teams = get_teams()
    for n in teams:
        if n['login'] == login.lower().strip():
            team = n
            team['able'] = get_able_stations(team['stations'])
            team['res'] = get_res(team['stations'])
            return team
    raise KeyError, "Team not found"

def rewrite_team(team):
    tms = get_teams()
    new = []
    for n in tms:
        if n['login'] == team['login']:
            new.append(team)
        else:
            new.append(n)
    with open(teams, 'w', encoding='utf-8') as f:
        f.write(dumps({"teams": new}))

def del_progress():
    teams = get_teams()
    for n in teams:
        n['stations'] = []
        rewrite_team(n)

def get_stations():
    with open(stations, 'r', encoding='utf-8') as f:
        text = f.read()
    return loads(text)    

def get_full_stations(li):
    dic = {'n': {}, 's': {}, 'p': {}, 'c': {}}
    stats = get_stations()
    for n in li:
        dic[stats[n]['type']][n] = stats[n]
    return dic

def add_key(station, key, login):
    team = get_team(login)
    keys = get_stations()[station]['keys']
    try:
        bonus = keys[key]
    except KeyError:
        raise KeyError, "Wrong key"
    #for n in bonus:
        #team['res'][n] = team['res'].get(n, 0) + bonus[n]
    team['stations'].append({"name": station, "key": key, "res": bonus})
    rewrite_team(team)

def are_in_list(unli, li):
    for n in unli:
        if not n in li:
            return False
    return True

def get_able_stations(stations):
    stations = [n['name'] for n in stations]
    ables = []
    stats = get_stations()
    for station in stats:
        if are_in_list(stats[station]['parents'], stations) and not station in stations:
            ables.append(station)
    return ables
            

