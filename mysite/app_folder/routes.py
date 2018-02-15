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

    term = request.args.get('term').lower()

    data = []  # Holds response

    if term:
        pass
    else:
        abort(401)

    limit = request.args.get('limit')
    if limit:
        limit = int(limit)
    else:
        limit = 3

    # Locate skill object
    skill = Skill.query.filter_by(name=term).first()
    origin_data = sorted(skill.get_origins_data(), key=itemgetter(1), reverse=True)[:limit]

    # Find where it is target
    target_data = sorted(skill.get_targets_data(), key=itemgetter(1), reverse=True)[:limit]

    # If clicked...
    clicked = request.args.get('clicked')
    if clicked:
        clicked_skill = Skill.query.filter_by(name=term).first()
        clicked_target_data = sorted(clicked_skill.get_targets_data(), key=itemgetter(1), reverse=True)[:limit]
        clicked_origins_data = sorted(clicked_skill.get_origins_data(), key=itemgetter(1), reverse=True)[:limit]
        for o in clicked_origins_data:
            td = {'source': o[0], 'target': clicked_skill.name.title(), 'count': o[1]}
            data.append(td)
        for t in clicked_target_data:
            td = {'source': clicked_skill.name.title(), 'target': t[0], 'count': t[1]}
            data.append(td)

    for o in origin_data:
        td = {'source': o[0], 'target': skill.name.title(), 'count': o[1]}
        data.append(td)

    for t in target_data:
        td = {'source': skill.name.title(), 'target': t[0], 'count': t[1]}
        data.append(td)

    return jsonify({'data': data})






