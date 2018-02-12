from flask import render_template, redirect, url_for, request, abort, jsonify, Response
from operator import itemgetter
from app_folder import app_run

import pandas as pd

f = r"/home/eric/FlaskD3/mysite/app_folder/alltopics5.csv"
df = pd.read_csv(f)


@app_run.route("/")
def index():
    """
    When you request the root path, you'll get the index.html template.

    """
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


    # Find where it is origin
    as_origin = df.loc[df['Origin'].str.lower() == term.lower()]
    as_origin = as_origin.values.tolist()

    # Find where it is target
    as_target = df.loc[df['Target'].str.lower() == term.lower()]
    as_target = as_target.values.tolist()

    data = []
    for o in as_origin:
        td = {'source': o[0], 'target': o[1], 'count': o[2]}
        data.append(td)
    for t in as_target:
        td = {'source': t[0], 'target': t[1], 'count': t[2]}
        data.append(td)

    # Sort the data by count

    data = sorted(data, key=itemgetter('count'), reverse=True)

    if limit:
        data = data[:limit]

    return jsonify({'data': data})






