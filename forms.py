
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, validators,TelField, \
    EmailField, SelectField, SubmitField, BooleanField, DateField ,TimeField, HiddenField
from wtforms.validators import ValidationError, DataRequired, \
    Email, EqualTo, Length, NumberRange, AnyOf,NoneOf  
from wtforms.fields  import BooleanField  
from wtforms_components import DateRange
from datetime import datetime, date, timedelta
import logging
   

# company registration form 
class CompanyRegistrationForm(FlaskForm):
    company = StringField(label=('Business Name'), 
        validators=[DataRequired(), 
        Length(max=100)]) 
    contact = StringField(label=('Contact'))    
    firstname = StringField(label=('First Name'), 
        validators=[DataRequired(), 
        Length(max=50)])    
    lastname = StringField(label=('Last Name'), 
        validators=[DataRequired(), 
        Length(max=50)])
    phone = TelField(label=('Contact Number'), render_kw={"placeholder": "000-000-0000"},     
        validators=[DataRequired(),
        Length(min=9,max=20)])
    email = EmailField(label=('Email'), render_kw={"placeholder": "myname@example.com"},
    validators=[DataRequired(),  
    Length(max=50)])
    address1 = StringField(label=('Address'), 
        validators=[DataRequired(), 
        Length(max=300)])
    address2 = StringField(label=('Address 2'), 
        validators=[ 
        Length(max=300)]) 
    city = StringField(label=('City'), 
        validators=[DataRequired(), 
        Length(max=50)]) 
    state = StringField(label=('State'), 
        validators=[DataRequired(), 
        Length(max=50)])
    zipcode = StringField(label=('Zip Code'), 
        validators=[DataRequired(), 
        Length(max=15)])
    country = SelectField(label=('Country'), choices=[],
    validators=[DataRequired(message = 'Please select a country')])   
    password = PasswordField(label=('Password'), 
        render_kw={"pattern": "(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*_=+-]).{4,16}", "data-toggle":"tooltip" ,"data-placement":"top",
         "title":"Must contain at least one number and one uppercase and lowercase letter and one symbol, and at least 4 or more characters"},
        validators=[DataRequired(), 
        Length(min=4, message='Password should be at least %(min)d characters long')])
    confirm_password = PasswordField(
        label=('Confirm Password'), 
        validators=[DataRequired(),
        EqualTo('password', message='Both password fields must be equal!')
        ])     
    submit = SubmitField(label=('Submit'))


    
    # validation for the phone numbers
    def validate_phone(self,phone):        
        for char in self.phone.data:
            if  char.isdigit()==False and char!='-':
                raise ValidationError(
                    f"Character {char} is not allowed in contact number.")            
             
# employee registration form 
class EmployeeRegistrationForm(FlaskForm):   
    company = SelectField(label=('Company'), choices=[],
    validators=[DataRequired(message = 'Please select a company')])  
    contact = StringField(label=('Contact'))    
    firstname = StringField(label=('First Name'), 
        validators=[DataRequired(), 
        Length(max=50)])    
    lastname = StringField(label=('Last Name'), 
        validators=[DataRequired(), 
        Length(max=50)])
    phone = TelField(label=('Contact Number'), render_kw={"placeholder": "000-000-0000"},     
        validators=[DataRequired(),
        Length(min=9,max=20)])
    email = EmailField(label=('Email'), render_kw={"placeholder": "myname@example.com"},
    validators=[DataRequired(),  
    Length(max=50)])
    address1 = StringField(label=('Address'), 
        validators=[DataRequired(), 
        Length(max=300)])
    address2 = StringField(label=('Address 2'), 
        validators=[ 
        Length(max=300)]) 
    city = StringField(label=('City'), 
        validators=[DataRequired(), 
        Length(max=50)]) 
    state = StringField(label=('State'), 
        validators=[DataRequired(), 
        Length(max=50)])
    zipcode = StringField(label=('Zip Code'), 
        validators=[DataRequired(), 
        Length(max=15)])
    country = SelectField(label=('Country'), choices=[],
        validators=[DataRequired(message = 'Please select a country')])   
    password = PasswordField(label=('Password'), 
        render_kw={"pattern": "(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*_=+-]).{4,16}", "data-toggle":"tooltip" ,"data-placement":"top",
         "title":"Must contain at least one number and one uppercase and lowercase letter and one symbol, and at least 4 or more characters"},
        validators=[DataRequired(), 
        Length(min=4, message='Password should be at least %(min)d characters long')])
    confirm_password = PasswordField(
        label=('Confirm Password'), 
        validators=[DataRequired(),
        EqualTo('password', message='Both password fields must be equal!')
        ])
    public_profile = BooleanField (label=('Public Profile'))
    submit = SubmitField(label=('Submit'))
    
    # validation for the phone numbers
    def validate_phone(self,phone):        
        for char in self.phone.data:
            if  char.isdigit()==False and char!='-':
                raise ValidationError(
                    f"Character {char} is not allowed in contact number.")            
                 


# login form 
class loginform(FlaskForm):
    email = EmailField(label=('Email'), render_kw={"placeholder": "myname@example.com"},
    validators=[DataRequired(),  
    Length(max=50)])
    password = PasswordField(
        label=('Password'), 
        validators=[DataRequired()])
    submit = SubmitField(label=('Submit'))   

# cafe signup form
class CafeSignupForm(FlaskForm):
    date = DateField(label=('Date:'),
        format='%Y-%m-%d',
        default =date.today,
        render_kw={"min": date.today(), "max": (date.today() + timedelta(days=30))}
        )
    # start_time = TimeField(label=('Start Time:'),
    #     default =datetime.now,
    #     step="900"
    #     )
    # end_time = TimeField(label=('End Time:'),
    #     default =datetime.now() + timedelta(hours=1),
    #     step="900"
    #     )
    start_time = SelectField(label=('Start Time:'), choices=[],
        validators=[DataRequired()]) 
    end_time = SelectField(label=('End Time:'), choices=[],
        validators=[DataRequired()])   
    companyid = HiddenField(label=('Company ID:'))                 
    submit = SubmitField(label=('Submit'))
   
    # validate start time greater then end time
    def validate_end_time(self, end_time):
        start = str(self.start_time.data)  
        end =  str(self.end_time.data)       
        (h, m) = start.split(':')
        resultstart = int(h) * 60 + int(m) 
        (h, m) = end.split(':')
        resultend = int(h) * 60 + int(m) 
        # check that the end time is 60 minutes greater then start time            
        if (resultstart + 60) > resultend:    
            raise ValidationError("End time 1 hour from start")


# Account update form 
class AccountUpdateForm(FlaskForm):
    company = StringField(label=('Business Name'), 
        validators=[Length(max=100)]) 
    contact = StringField(label=('Contact'))    
    firstname = StringField(label=('First Name'), 
        validators=[Length(max=50)])    
    lastname = StringField(label=('Last Name'), 
        validators=[DataRequired(), 
        Length(max=50)])
    phone = TelField(label=('Contact Number'), render_kw={"placeholder": "000-000-0000"},     
        validators=[DataRequired(),
        Length(min=9,max=20)])        
    address1 = StringField(label=('Address'), 
        validators=[DataRequired(), 
        Length(max=300)])
    address2 = StringField(label=('Address 2'), 
        validators=[ 
        Length(max=300)]) 
    city = StringField(label=('City'), 
        validators=[DataRequired(), 
        Length(max=50)]) 
    state = StringField(label=('State'), 
        validators=[DataRequired(), 
        Length(max=50)])
    zipcode = StringField(label=('Zip Code'), 
        validators=[DataRequired(), 
        Length(max=15)])
    country = SelectField(label=('Country'), choices=[],
    validators=[DataRequired(message = 'Please select a country')])
    public_profile = BooleanField (label=('Public Profile'))    
    # public_profile_hidden = BooleanField (label=('Public Profile Hidden'))   
    submit = SubmitField(label=('Update'))       
    
# update password form
class PasswordUpdateForm(FlaskForm):
    password = PasswordField(label=('Password'), 
        render_kw={"pattern": "(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*_=+-]).{4,16}", "data-toggle":"tooltip" ,"data-placement":"top",
        "title":"Must contain at least one number and one uppercase and lowercase letter and one symbol, and at least 4 or more characters"},
        validators=[DataRequired(), 
        Length(min=4, message='Password should be at least %(min)d characters long')])
    confirm_password = PasswordField(
        label=('Confirm Password'), 
        validators=[DataRequired(),
        EqualTo('password', message='Both password fields must be equal!')
        ])
        
    submit = SubmitField(label=('Submit'))
    


                    
            

