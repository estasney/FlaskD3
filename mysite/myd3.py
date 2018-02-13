from app_folder import app_run, db
from app_folder.models import Skill


@app_run.shell_context_processor
def make_shell_context():
    return {'db': db, 'Skill': Skill}


