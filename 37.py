from app import create_app, db
from app.models import Text

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'Text': Text}


