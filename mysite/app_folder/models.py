import random

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

    target = db.relationship("Skill", primaryjoin=target_id==Skill.id, backref='target')

    origin = db.relationship("Skill", primaryjoin=origin_id==Skill.id, backref='origin')

    count = db.Column(db.Integer)

    def __init__(self, origin, target, count):
        self.origin = origin
        self.target = target
        self.origin_id = origin.id
        self.target_id = target.id
        self.count = count

