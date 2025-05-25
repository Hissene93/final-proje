from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField, FloatField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Nom utilisateur', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    confirm_password = PasswordField('Confirmer mot de passe', 
                                   validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Rôle', choices=[('student', 'Étudiant'), ('teacher', 'Enseignant'), ('admin', 'Admin')])
    
    
    first_name = StringField('Prénom')
    last_name = StringField('Nom')
    age = IntegerField('Âge')
    class_level = StringField('Classe')
    contact = StringField('Contact')
    
    submit = SubmitField("S'inscrire")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Ce nom d\'utilisateur est déjà pris.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Cet email est déjà utilisé.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    remember = BooleanField('Se souvenir de moi')
    submit = SubmitField('Se connecter')

class CourseForm(FlaskForm):
    name = StringField('Nom du cours', validators=[DataRequired()])
    teacher = SelectField('Enseignant', coerce=int, validators=[DataRequired()])
    credits = IntegerField('Crédits', validators=[DataRequired()])
    submit = SubmitField('Enregistrer')

class GradeForm(FlaskForm):
    student = SelectField('Étudiant', coerce=int, validators=[DataRequired()])
    course = SelectField('Cours', coerce=int, validators=[DataRequired()])
    grade = FloatField('Note', validators=[DataRequired()])
    submit = SubmitField('Enregistrer')
class StudentForm(FlaskForm):
    username = StringField('Nom utilisateur', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    first_name = StringField('Prénom', validators=[DataRequired()])
    last_name = StringField('Nom', validators=[DataRequired()])
    age = IntegerField('Âge')
    class_level = StringField('Classe')
    contact = StringField('Contact')
    submit = SubmitField('Ajouter')