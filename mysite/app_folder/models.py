from app_folder import app_run, db


class Skill(db.Model):

    __tablename__ = 'skills'
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('skills.id'))
    name = db.Column(db.String(250))
    children = db.relationship("Skill",
                               backref=db.backref('parent', remote_side=[id]))

