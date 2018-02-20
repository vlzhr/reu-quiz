# -*- coding: utf-8 -*-
from flask import Flask, render_template, session, request, redirect
from gamer import get_teams, get_team, get_able_stations, add_key, get_statistics, get_full_stations, del_progress
from moder import add_station as add_mstation, add_key as add_mkey, del_station, get_stations as get_mstations

app = Flask(__name__)
app.debug = True
app.secret_key = 'jj'

@app.route("/")
def index():
    return redirect("/panel")
    return render_template("index.html")

@app.route("/panel")
def panel():
    if session.get('team', 0) == 0:
        return render_template("login.html", alert='')
    team = get_team(session['team'])
    team['stations'].reverse()
    able = get_full_stations(team['able'])
    return render_template("panel.html", len=len, able=able, name=session['team'], enumerate=enumerate, team=team, alert=request.args.get('alert',''))

@app.route("/add_station")
def add_station():
    try:
        add_key(request.args['station'], request.args['key'], session['team'])
    except KeyError:
        return redirect(u'/panel?alert=' + request.args['station'])
    return redirect('/panel')

@app.route("/admin")
def admin():
    if session.get('admin', 0) == 0:
        return render_template("login.html", alert=u"Необходимо  войти от имени админа")
    return render_template("teams.html", teams = get_statistics())

@app.route("/logout")
def logout():
    try:
        del session['team']
    except KeyError:
        pass
    try:
        del session['admin']
    except KeyError:
        pass
    return redirect('/')

@app.route("/logging")
def logging():
    if request.args['login'].lower() == 'admin' and request.args['password'] == 'aachen1995':
        session['admin'] = 1
        return redirect('/admin')
    teams = get_teams()
    for n in teams:
        if n['login'].lower() == request.args['login'].lower() and n['password'] == request.args['password']:
            session['team'] = n['login'].lower()
            return redirect('/panel')
    return render_template("login.html", alert=u"Неверные данные")

@app.route("/moder")
def moder():
    if not session.get('admin', 0):
        return render_template("login.html", alert=u"Необходимо войти от имени админа")
    return render_template("moder.html", stations=get_mstations())

@app.route("/mod_stat")
def mod_stat():
    d = request.args
    add_mstation(d['name'], d['parents'], d['type'])
    return redirect('/moder')

@app.route("/mod_key")
def mod_key():
    d = request.args
    add_mkey(d['station'], d['key'], {'n': int(d['n']), 's': int(d['s']), 'c': int(d['c']), 'p': int(d['p']), 'm': int(d['m'])})
    return redirect('/moder')

@app.route("/mod_del")
def mod_del():
    d = request.args
    del_station(d['stat'])
    return redirect('/moder')

@app.route("/restart_game")
def restart_game():
    if not session.get('admin', 0):
        return render_template("login.html", alert=u"Необходимо войти от имени админа")
    del_progress()
    return redirect('/admin')

if __name__=="__main__":
    app.run('127.0.0.1', 80)
