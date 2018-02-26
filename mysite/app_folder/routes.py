from flask import render_template, redirect, url_for, request, abort, jsonify, Response
from operator import itemgetter
from app_folder import app_run
from app_folder.models import Skill, Association, Node, Edge

import pandas as pd

import random
import colorsys
import numpy as np
from gensim.summarization.keywords import get_graph
from gensim.summarization.pagerank_weighted import pagerank_weighted
from operator import itemgetter
import pandas as pd
import math
from colour import Color

def bright_color():
    h,s,l = random.random(), 0.5 + random.random()/2.0, 0.4 + random.random()/5.0
    r,g,b = [int(256*i) for i in colorsys.hls_to_rgb(h,l,s)]
    return (r, g, b)

@app_run.route('/')
def index():
    return 'Navigate to /topics or /keywords'

@app_run.route("/topics")
def topics():
    return render_template('topics.html')

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
        elif limit > 25:
            limit = 25
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

@app_run.route('/keywords')
def keywords():
    return render_template('keywords.html')

def get_cat(x, std_dev):
    return math.floor(x/std_dev)


def assign_deviations(scores_dict):
    std_dev = np.std(list(scores_dict.values()))
    scores_list = [(k, v) for k, v in scores_dict.items()]
    scores_list = sorted(scores_list, key=itemgetter(1))

    df = pd.DataFrame(scores_list)
    df['Cat'] = df[1].apply(lambda x: get_cat(x, std_dev))
    df1 = df[[0, 'Cat']]
    cats_created = df1['Cat'].max() + 1
    cat_dict = dict(list(df1.to_records(index=False)))
    return cat_dict, cats_created

def compute_colors_dict(steps, low="blue", high="red"):
    low = Color(low)
    high = Color(high)
    color_list = list(low.range_to(high, steps))
    color_dict = {}
    for i, color in enumerate(color_list):
        rgb = color.get_rgb()
        rgb_web = []
        for r in rgb:
            rgb_web.append(int(r * 255))
        rgb_web = tuple(rgb_web)
        color_dict[i] = rgb_web
    return color_dict

@app_run.route('/kw_data', methods=['POST'])
def kw_data():
    raw_text = request.form.get('raw_text')
    if raw_text:
        graph = get_graph(raw_text)
    else:
        abort(401)

    edges = graph.edges()
    data = []
    scores = pagerank_weighted(graph)
    dev_dict, dev_count = assign_deviations(scores)
    color_dict = compute_colors_dict(dev_count)
    for edge in edges:
        source, target = edge
        source_score, target_score = int(dev_dict.get(source, 0)), int(dev_dict.get(target, 0))
        source_color, target_color = (color_dict.get(source_score, color_dict[0])), (color_dict.get(target_score, color_dict[0]))
        td = {'source': source, 'source_score': source_score, 'target': target, 'target_score': target_score,
              'source_color': source_color, 'target_color': target_color}
        data.append(td)

    return jsonify({'data': data})

@app_run.route('/jobs')

def jobs():
    return render_template('jobs.html')

@app_run.route('/jobs_data')
def job_data():
    term = request.args.get('term').lower()
    print(term)
    node = Node.query.filter_by(name=term).first()
    print(node)
    if not node:
        abort(401)

    node_neighbors = node.neighbors()
    neighbor_names = [x[0] for x in node_neighbors]
    node_neighbors_scores = {x: Node.query.filter_by(name=x).first().scores for x, y in node_neighbors if x!=term}
    node_neighbors_scores[term] = node.scores

    data = []
    dev_dict, dev_count = assign_deviations(node_neighbors_scores)
    color_dict = compute_colors_dict(dev_count)
    for neighbor in neighbor_names:
        source, target = term, neighbor
        source_score, target_score = int(dev_dict.get(source, 0)), int(dev_dict.get(target, 0))
        source_color, target_color = (color_dict.get(source_score, color_dict[0])), (
        color_dict.get(target_score, color_dict[0]))
        td = {'source': source, 'source_score': source_score, 'target': target, 'target_score': target_score,
              'source_color': source_color, 'target_color': target_color}
        data.append(td)

    return jsonify({'data': data})













