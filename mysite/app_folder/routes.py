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

    # To dictionary form
    origin_data_dict = []
    for od in origin_data:
        td = {od[0]: od[1]}
        origin_data_dict.append(td)

    # Find where it is target
    target_data = skill.get_targets_data()
    target_data = sorted(target_data, key=itemgetter(1), reverse=True)

    if limit:
        target_data = target_data[:limit]

    # To dictionary form
    target_data_dict = []
    for od in target_data:
        td = {od[0]: od[1]}
        target_data_dict.append(td)

    return jsonify({'origin': origin_data_dict, 'target': target_data_dict})






