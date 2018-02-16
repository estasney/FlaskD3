from flask import render_template, redirect, url_for, request, abort, jsonify, Response
from operator import itemgetter
from app_folder import app_run
from app_folder.models import Skill, Association

import pandas as pd

import random
import colorsys

def bright_color():
    h,s,l = random.random(), 0.5 + random.random()/2.0, 0.4 + random.random()/5.0
    r,g,b = [int(256*i) for i in colorsys.hls_to_rgb(h,l,s)]
    return (r, g, b)

@app_run.route("/")
def index():

    return render_template('index.html')

@app_run.route("/data")
def data():
    """
    On request, this returns origins and targets of a lookup term
    """

    term = request.args.get('term').lower()
    c = bright_color()

    data = []  # Holds response

    if term:
        pass
    else:
        abort(401)

    limit = request.args.get('limit')
    if limit:
        limit = int(limit)
        if limit < 3:
            limit = 3
    else:
        limit = 3

    # Locate skill object
    skill = Skill.query.filter_by(name=term).first()
    origin_data = sorted(skill.get_origins_data(), key=itemgetter(1), reverse=True)[:limit]

    # Find where it is target
    target_data = sorted(skill.get_targets_data(), key=itemgetter(1), reverse=True)[:limit]


    for o in origin_data:
        td = {'source': o[0].title(), 'target': skill.name.title(), 'count': o[1], 'color': c}
        data.append(td)

    for t in target_data:
        td = {'source': skill.name.title(), 'target': t[0].title(), 'count': t[1], 'color': c}
        data.append(td)

    # colors


    return jsonify({'data': data})






