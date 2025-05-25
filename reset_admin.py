from app import create_app, db
from app.models import User
from flask_bcrypt import Bcrypt


app = create_app()
bcrypt = Bcrypt(app)

def reset_admin():
    with app.app_context():
        try:
            
            User.query.filter_by(username='admin').delete()
            
           
            new_admin = User(
                username='admin',
                email='admin@gmail.com',
                password=bcrypt.generate_password_hash('examen2025').decode('utf-8'),
                role='admin'
            )
            db.session.add(new_admin)
            db.session.commit()
            
           
            admin = User.query.filter_by(username='admin').first()
            if admin:
                print("✅ Admin réinitialisé avec succès!")
                print(f"Username: {admin.username}")
                print(f"Email: {admin.email}")
                print("Mot de passe: examen2025")
            else:
                print("❌ Échec de la création de l'admin")
                
        except Exception as e:
            db.session.rollback()
            print(f"❌ Erreur lors de la réinitialisation: {str(e)}")

if __name__ == '__main__':
    reset_admin()