from app import create_app, db
from app.models import User, Student

app = create_app()
if __name__ == "__main__":
    app.run(debug=True)


