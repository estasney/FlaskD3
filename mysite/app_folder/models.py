from operator import itemgetter
from sqlalchemy.ext.orderinglist import ordering_list
from app_folder import app_run, db


class Skill(db.Model):

    __tablename__ = 'skills'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500))

    def add_target(self, target_skill, count):
        Association(self, target_skill, count)
        return self

    def get_targets(self):
        return [x.target for x in self.origin]

    def get_targets_data(self):
        return [(x.target.name, x.count) for x in self.origin]

    def get_origins(self):
        return [x.origin for x in self.target]

    def get_origins_data(self):
        return [(x.origin.name, x.count) for x in self.target]


class Association(db.Model):

    __tablename__ = 'association'
    origin_id = db.Column(db.Integer, db.ForeignKey('skills.id'), primary_key=True)

    target_id = db.Column(db.Integer, db.ForeignKey('skills.id'), primary_key=True)

    target = db.relationship("Skill", primaryjoin=target_id==Skill.id, backref='target', order_by='Association.count',
                             collection_class=ordering_list('count'))

    origin = db.relationship("Skill", primaryjoin=origin_id==Skill.id, backref='origin', order_by='Association.count',
                             collection_class=ordering_list('count'))

    count = db.Column(db.Integer)

    def __init__(self, origin, target, count):
        self.origin = origin
        self.target = target
        self.origin_id = origin.id
        self.target_id = target.id
        self.count = count


class Node(db.Model):
    __tablename__ = 'node'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    scores = db.Column(db.Float)

    def neighbors(self):
        highers = [(x.higher_node.name, x.freq, x.higher_node.scores) for x in self.lower_edges if x.higher_node.id != self.id]
        lowers = [(x.lower_node.name, x.freq, x.lower_node.scores) for x in self.higher_edges if x.lower_node.id != self.id]
        combined = highers + lowers
        return sorted(combined, key=itemgetter(1), reverse=True)


class Edge(db.Model):
    __tablename__ = 'edge'

    lower_id = db.Column(
        db.Integer,
        db.ForeignKey('node.id'),
        primary_key=True)

    higher_id = db.Column(
        db.Integer,
        db.ForeignKey('node.id'),
        primary_key=True)

    lower_node = db.relationship(
        "Node",
        primaryjoin=lower_id == Node.id,
        backref='lower_edges')

    higher_node = db.relationship(
        "Node",
        primaryjoin=higher_id == Node.id,
        backref='higher_edges')

    freq = db.Column(db.Integer, default=0)

    def __init__(self, nodes: list):
        node_dict = {node.id: node for node in nodes}
        lowest_id, highest_id = min([node.id for node in nodes]), max([node.id for node in nodes])
        n1, n2 = node_dict[lowest_id], node_dict[highest_id]

        self.lower_node = n1
        self.higher_node = n2


node_links = {}
TOP_N = 10
LAYERS = 10


def filter_top(neighbors, top_n=TOP_N, expanded=None):
    sorted_neighbors = sorted(neighbors, key=itemgetter(2), reverse=True)
    if expanded:
        sorted_neighbors = [neighbor for neighbor in sorted_neighbors if neighbor[0] not in expanded]
    sorted_neighbors = [neighbor for neighbor in sorted_neighbors][:top_n]
    return sorted_neighbors

def process_node(node_name):
    node = Node.query.filter_by(name=node_name).first()
    neighbors = filter_top(node.neighbors())
    for n in neighbors:
        if node_name in node_links:
            if n not in node_links[node_name]:
                ol = node_links[node_name]
                ol.append(n)
                node_links[node_name] = ol

def expand(root, layers=LAYERS):
    root_neighbors = filter_top(root.neighbors())
    layer_counter = 0
    expanded = {}
    checked = []
    while layer_counter < layers:
        if not expanded:
            for rn in root_neighbors:
                dict_n = expanded.get(root.name, [])
                dict_n.append(rn[0])
                expanded[root.name] = dict_n
            layer_counter += 1
            checked.append(root.name)
            continue
        for targets in list(expanded.values()):
            for target in targets:
                if target in checked:
                    continue
                a_node = Node.query.filter_by(name=target).first()
                a_neighbors = filter_top(a_node.neighbors(), top_n=TOP_N, expanded=expanded)

                for b in a_neighbors:
                    n_dict = expanded.get(target, [])
                    n_dict.append(b[0])
                    expanded[target] = n_dict
                checked.append(target)
        layer_counter += 1
        continue
    for k in expanded.keys():
        for v in expanded[k]:
            yield (k, v)