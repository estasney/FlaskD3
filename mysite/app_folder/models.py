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
        highers = [(x.higher_node.name, x.freq) for x in self.lower_edges]
        lowers = [(x.lower_node.name, x.freq) for x in self.higher_edges]
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
