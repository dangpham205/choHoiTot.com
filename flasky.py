from app import create_app, db
from app.models import User, Student

app = create_app()
if __name__ == "__main__":
    app.run(debug=True)

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Student=Student)

@app.before_first_request
def create_tables():
    db.create_all()