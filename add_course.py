from app import create_app, db
from app.models import Course, User

app = create_app()

def add_course():
    with app.app_context():
        try:
            
            teacher = User.query.filter_by(role='teacher').first()
            
            if not teacher:
                print("Aucun enseignant trouvé !")
                return

            new_course = Course(
                name="Mathématiques Avancées",
                teacher_id=teacher.id,
                credits=4
            )
            
            db.session.add(new_course)
            db.session.commit()
            print(f"✅ Cours ajouté avec succès (ID: {new_course.id})")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Erreur: {str(e)}")

if __name__ == '__main__':
    add_course()