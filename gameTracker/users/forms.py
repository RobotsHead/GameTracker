from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from gameTracker.models import User





class RegistrationForm(FlaskForm):
    firstname = StringField('Firstname',
                            validators=[DataRequired(), Length(min=2, max=20)])
    lastname = StringField('Lastname',
                            validators=[DataRequired(), Length(min=2, max=30)])
    username = StringField('Username',
                            validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                    validators=[DataRequired(), EqualTo('password')])
                                
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()        
        if user:
            raise ValidationError('That username is taken, Please choose another.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()        
        if user:
            raise ValidationError('That email is taken, Please choose another.')

    

class LoginForm(FlaskForm):   
    username = StringField('Username') 
    email = StringField('Email')
    password = PasswordField('Password', validators=[DataRequired()])  
    remember = BooleanField('Remember Me')                                
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    firstname = StringField('Firstname',
                            validators=[Length(min=2, max=20)])
    lastname = StringField('Lastname',
                            validators=[Length(min=2, max=30)])
    username = StringField('Username',
                            validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])]) 
                             
    submit = SubmitField('Update')

    def validate_username(self, username):
        
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()        
            if user:
                raise ValidationError('That username is taken, Please choose another.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()        
            if user:
                raise ValidationError('That email is taken, Please choose another.')

class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])    
                             
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()        
        if user is None:
            raise ValidationError('There is no account with that email.')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
                                
    submit = SubmitField('Reset Password')
