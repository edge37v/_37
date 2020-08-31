from app import create_app, db
from app.models import User, Plan

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Plan': Plan}

#l_monthly
#l_yearly

