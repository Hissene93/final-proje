from app import create_app, db
from app.models import User, Student, Course, Grade

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Student': Student, 'Course': Course, 'Grade': Grade}

if __name__ == '__main__':
    app.run(debug=True)