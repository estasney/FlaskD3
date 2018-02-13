from flask import render_template, redirect, url_for, request, abort, jsonify, Response
from operator import itemgetter
from app_folder import app_run
from app_folder.models import Skill, Association

import pandas as pd

@app_run.route("/")
def index():

    return render_template('index.html')

@app_run.route("/data")
def data():
    """
    On request, this returns origins and targets of a lookup term

    """

    term = request.args.get('term')
    if term:
        pass
    else:
        abort(401)
    limit = request.args.get('limit')
    if limit:
        limit = int(limit)


    # Locate skill object
    skill = Skill.query.filter_by(name=term).first()

    # Data as origin
    origin_data = skill.get_origins_data()
    # Sorted
    origin_data = sorted(origin_data, key=itemgetter(1), reverse=True)

    if limit:
        origin_data = origin_data[:limit]

    # Find where it is target
    target_data = skill.get_targets_data()
    target_data = sorted(target_data, key=itemgetter(1), reverse=True)

    if limit:
        target_data = target_data[:limit]

    data = []
    for o in od:
        td = {'source': o[0], 'target': skill.name, 'count': o[1]}
        data.append(td)

    for t in target_data:
        td = {'source': skill.name, 'target': t[0], 'count': t[1]}
        data.append(td)

    return jsonify({'dzta': data})






