from flask_wtf import FlaskForm, RecaptchaField
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import Form, FieldList, FormField, StringField, PasswordField, SubmitField, BooleanField, RadioField, TextAreaField, SelectField, DateField, IntegerField
from wtforms.fields.html5 import TelField, EmailField, TimeField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional
from flaskapp.models import User
from flaskapp import bcrypt

class RegistrationForm(FlaskForm):
    username_regis = StringField('Username',
                           validators=[DataRequired(), Length(min=5, max=20)])
    email_regis = EmailField('Email',
                        validators=[DataRequired(), Email()])
    password_regis = PasswordField('Password', validators=[DataRequired()])
    recaptcha = RecaptchaField()
    submit_regis = SubmitField('Sign Up')

    def validate_username_regis(self, username_regis):
        user = User.query.filter_by(username=username_regis.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email_regis(self, email_regis):
        user = User.query.filter_by(email=email_regis.data).first()
        if user:
            raise ValidationError('An account already exists for this email.')



class LoginForm(FlaskForm):
    email_login = StringField('Email/Username',
                        validators=[DataRequired()])
    password_login = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit_login = SubmitField('Login')

    def validate_email_login(self, email_login):
        print('1')
        usere = User.query.filter_by(email=email_login.data).first()
        useru = User.query.filter_by(username=email_login.data).first()
        if (usere or useru) is None:
            print('not ok')
            raise ValidationError('Username/Email does not exist!')

    def validate_password_login(self, password_login):
        usere = User.query.filter_by(email=self.email_login.data).first()
        useru = User.query.filter_by(username=self.email_login.data).first()
        if usere:
            if bcrypt.check_password_hash(usere.password, password_login.data) == False:
                raise ValidationError('Password Incorrect!')
        if useru:
            if bcrypt.check_password_hash(useru.password, password_login.data) == False:
                raise ValidationError('Password Incorrect!')

class OfferForm(Form):
    attendee = IntegerField('Attendee Amount', validators=[DataRequired()])
    discount = IntegerField('Discount', validators=[DataRequired()])

class OfferParentForm(FlaskForm):
    offers = FieldList(FormField(OfferForm),min_entries=1)

class CreateEventForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    price = IntegerField('Price', validators=[DataRequired()])
    date = DateField('Start Date', validators=[DataRequired()])
    date_end = DateField('End Date', validators=[DataRequired()])
    time = TimeField('Start Time', validators=[DataRequired()])
    time_end = TimeField('End Time', validators=[DataRequired()])
    days = StringField('Days', validators=[DataRequired()])
    pre_knowledge = SelectField('Required Knowledge', choices=[('', 'Required level of knowledge for event'), ('none', 'None'), ('basic', 'Basic'), ('expert', 'Expert')], validators=[DataRequired()])
    tags = SelectField('Tags', choices=[('', 'Select a tag'), ('cycling', 'Cycling'), ('hiking', 'Hiking'), ('food', 'Food'), ('music', 'Music'), ('tours', 'Tours'), ('training', 'Training')])
    schedule = StringField('Schedule', validators=[Optional()])
    direction = StringField('Direction', validators=[Optional()])
    equipment = StringField('Equipment', validators=[Optional()])
    min_tickets = IntegerField('Minimum number of Tickets', validators=[Optional()])
    utube_link = StringField('YouTube Video Link', validators=[Optional(), Length(min=26, max=43)])
    repeat_times = IntegerField('Repeat times')
    repeat_recurrence = SelectField('', choices=[('day', 'Day(s)'), ('week', 'Week(s)'), ('month', 'Month(s)'), ('year', 'Year(s)')])
    offers_bool = BooleanField('Offers')
    attendee1 = IntegerField('Attendee Amount', validators=[Optional()])
    discount1 = IntegerField('Discount', validators=[Optional()])
    attendee2 = IntegerField('Attendee Amount', validators=[Optional()])
    discount2 = IntegerField('Discount', validators=[Optional()])
    attendee3 = IntegerField('Attendee Amount', validators=[Optional()])
    discount3 = IntegerField('Discount', validators=[Optional()])
    attendee4 = IntegerField('Attendee Amount', validators=[Optional()])
    discount4 = IntegerField('Discount', validators=[Optional()])
    attendee5 = IntegerField('Attendee Amount', validators=[Optional()])
    discount5 = IntegerField('Discount', validators=[Optional()])
    attendee6 = IntegerField('Attendee Amount', validators=[Optional()])
    discount6 = IntegerField('Discount', validators=[Optional()])
    attendee7 = IntegerField('Attendee Amount', validators=[Optional()])
    discount7 = IntegerField('Discount', validators=[Optional()])
    attendee8 = IntegerField('Attendee Amount', validators=[Optional()])
    discount8 = IntegerField('Discount', validators=[Optional()])
    image1 = FileField('Featured Image', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'bmp']), DataRequired()])
    image2 = FileField('Featured Image 2', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'bmp']), Optional()])
    image3 = FileField('Featured Image 3', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'bmp']), Optional()])
    image4 = FileField('Featured Image 4', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'bmp']), Optional()])
    image5 = FileField('Featured Image 5', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'bmp']), Optional()])
    image6 = FileField('Featured Image 6', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'bmp']), Optional()])
    image7 = FileField('Featured Image 7', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'bmp']), Optional()])
    family = BooleanField('Family Friendly/ Kids Allowed')
    fee_cancel = BooleanField('Fee Cancelation')
    prioritize = BooleanField('Prioritize Event')

class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')

class PersonalDetailForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    contact_number = TelField('Contact Number', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    loc_state = StringField('State', validators=[Optional()])
    zip_code = IntegerField('Zip Code', validators=[DataRequired()])
    country = SelectField('Country', choices=[('', 'Select'), ('AF', 'Afghanistan'), ('AX', 'Åland Islands'), ('AL', 'Albania'), ('DZ', 'Algeria'), ('AD', 'Andorra'), ('AO', 'Angola'), ('AI', 'Anguilla'), ('AQ', 'Antarctica'), ('AG', 'Antigua &amp; Barbuda'), ('AR', 'Argentina'), ('AM', 'Armenia'), ('AW', 'Aruba'), ('AC', 'Ascension Island'), ('AU', 'Australia'), ('AT', 'Austria'), ('AZ', 'Azerbaijan'), ('BS', 'Bahamas'), ('BH', 'Bahrain'), ('BD', 'Bangladesh'), ('BB', 'Barbados'), ('BY', 'Belarus'), ('BE', 'Belgium'), ('BZ', 'Belize'), ('BJ', 'Benin'), ('BM', 'Bermuda'), ('BT', 'Bhutan'), ('BO', 'Bolivia'), ('BA', 'Bosnia &amp; Herzegovina'), ('BW', 'Botswana'), ('BV', 'Bouvet Island'), ('BR', 'Brazil'), ('IO', 'British Indian Ocean Territory'), ('VG', 'British Virgin Islands'), ('BN', 'Brunei'), ('BG', 'Bulgaria'), ('BF', 'Burkina Faso'), ('BI', 'Burundi'), ('KH', 'Cambodia'), ('CM', 'Cameroon'), ('CA', 'Canada'), ('CV', 'Cape Verde'), ('BQ', 'Caribbean Netherlands'), ('KY', 'Cayman Islands'), ('CF', 'Central African Republic'), ('TD', 'Chad'), ('CL', 'Chile'), ('CN', 'China'), ('CO', 'Colombia'), ('KM', 'Comoros'), ('CG', 'Congo - Brazzaville'), ('CD', 'Congo - Kinshasa'), ('CK', 'Cook Islands'), ('CR', 'Costa Rica'), ('CI', 'Côte d’Ivoire'), ('HR', 'Croatia'), ('CW', 'Curaçao'), ('CY', 'Cyprus'), ('CZ', 'Czechia'), ('DK', 'Denmark'), ('DJ', 'Djibouti'), ('DM', 'Dominica'), ('DO', 'Dominican Republic'), ('EC', 'Ecuador'), ('EG', 'Egypt'), ('SV', 'El Salvador'), ('GQ', 'Equatorial Guinea'), ('ER', 'Eritrea'), ('EE', 'Estonia'), ('SZ', 'Eswatini'), ('ET', 'Ethiopia'), ('FK', 'Falkland Islands'), ('FO', 'Faroe Islands'), ('FJ', 'Fiji'), ('FI', 'Finland'), ('FR', 'France'), ('GF', 'French Guiana'), ('PF', 'French Polynesia'), ('TF', 'French Southern Territories'), ('GA', 'Gabon'), ('GM', 'Gambia'), ('GE', 'Georgia'), ('DE', 'Germany'), ('GH', 'Ghana'), ('GI', 'Gibraltar'), ('GR', 'Greece'), ('GL', 'Greenland'), ('GD', 'Grenada'), ('GP', 'Guadeloupe'), ('GU', 'Guam'), ('GT', 'Guatemala'), ('GG', 'Guernsey'), ('GN', 'Guinea'), ('GW', 'Guinea-Bissau'), ('GY', 'Guyana'), ('HT', 'Haiti'), ('HN', 'Honduras'), ('HK', 'Hong Kong SAR China'), ('HU', 'Hungary'), ('IS', 'Iceland'), ('IN', 'India'), ('ID', 'Indonesia'), ('IQ', 'Iraq'), ('IE', 'Ireland'), ('IM', 'Isle of Man'), ('IL', 'Israel'), ('IT', 'Italy'), ('JM', 'Jamaica'), ('JP', 'Japan'), ('JE', 'Jersey'), ('JO', 'Jordan'), ('KZ', 'Kazakhstan'), ('KE', 'Kenya'), ('KI', 'Kiribati'), ('XK', 'Kosovo'), ('KW', 'Kuwait'), ('KG', 'Kyrgyzstan'), ('LA', 'Laos'), ('LV', 'Latvia'), ('LB', 'Lebanon'), ('LS', 'Lesotho'), ('LR', 'Liberia'), ('LY', 'Libya'), ('LI', 'Liechtenstein'), ('LT', 'Lithuania'), ('LU', 'Luxembourg'), ('MO', 'Macao SAR China'), ('MG', 'Madagascar'), ('MW', 'Malawi'), ('MY', 'Malaysia'), ('MV', 'Maldives'), ('ML', 'Mali'), ('MT', 'Malta'), ('MQ', 'Martinique'), ('MR', 'Mauritania'), ('MU', 'Mauritius'), ('YT', 'Mayotte'), ('MX', 'Mexico'), ('MD', 'Moldova'), ('MC', 'Monaco'), ('MN', 'Mongolia'), ('ME', 'Montenegro'), ('MS', 'Montserrat'), ('MA', 'Morocco'), ('MZ', 'Mozambique'), ('MM', 'Myanmar (Burma)'), ('NA', 'Namibia'), ('NR', 'Nauru'), ('NP', 'Nepal'), ('NL', 'Netherlands'), ('NC', 'New Caledonia'), ('NZ', 'New Zealand'), ('NI', 'Nicaragua'), ('NE', 'Niger'), ('NG', 'Nigeria'), ('NU', 'Niue'), ('MK', 'North Macedonia'), ('NO', 'Norway'), ('OM', 'Oman'), ('PK', 'Pakistan'), ('PS', 'Palestinian Territories'), ('PA', 'Panama'), ('PG', 'Papua New Guinea'), ('PY', 'Paraguay'), ('PE', 'Peru'), ('PH', 'Philippines'), ('PN', 'Pitcairn Islands'), ('PL', 'Poland'), ('PT', 'Portugal'), ('PR', 'Puerto Rico'), ('QA', 'Qatar'), ('RE', 'Réunion'), ('RO', 'Romania'), ('RU', 'Russia'), ('RW', 'Rwanda'), ('WS', 'Samoa'), ('SM', 'San Marino'), ('ST', 'São Tomé &amp; Príncipe'), ('SA', 'Saudi Arabia'), ('SN', 'Senegal'), ('RS', 'Serbia'), ('SC', 'Seychelles'), ('SL', 'Sierra Leone'), ('SG', 'Singapore'), ('SX', 'Sint Maarten'), ('SK', 'Slovakia'), ('SI', 'Slovenia'), ('SB', 'Solomon Islands'), ('SO', 'Somalia'), ('ZA', 'South Africa'), ('GS', 'South Georgia &amp; South Sandwich Islands'), ('KR', 'South Korea'), ('SS', 'South Sudan'), ('ES', 'Spain'), ('LK', 'Sri Lanka'), ('BL', 'St. Barthélemy'), ('SH', 'St. Helena'), ('KN', 'St. Kitts &amp; Nevis'), ('LC', 'St. Lucia'), ('MF', 'St. Martin'), ('PM', 'St. Pierre &amp; Miquelon'), ('VC', 'St. Vincent &amp; Grenadines'), ('SR', 'Suriname'), ('SJ', 'Svalbard &amp; Jan Mayen'), ('SE', 'Sweden'), ('CH', 'Switzerland'), ('TW', 'Taiwan'), ('TJ', 'Tajikistan'), ('TZ', 'Tanzania'), ('TH', 'Thailand'), ('TL', 'Timor-Leste'), ('TG', 'Togo'), ('TK', 'Tokelau'), ('TO', 'Tonga'), ('TT', 'Trinidad &amp; Tobago'), ('TA', 'Tristan da Cunha'), ('TN', 'Tunisia'), ('TR', 'Turkey'), ('TM', 'Turkmenistan'), ('TC', 'Turks &amp; Caicos Islands'), ('TV', 'Tuvalu'), ('UG', 'Uganda'), ('UA', 'Ukraine'), ('AE', 'United Arab Emirates'), ('GB', 'United Kingdom'), ('US', 'United States'), ('UY', 'Uruguay'), ('UZ', 'Uzbekistan'), ('VU', 'Vanuatu'), ('VA', 'Vatican City'), ('VE', 'Venezuela'), ('VN', 'Vietnam'), ('WF', 'Wallis &amp; Futuna'), ('EH', 'Western Sahara'), ('YE', 'Yemen'), ('ZM', 'Zambia'), ('ZW', 'Zimbabwe')], validators=[DataRequired()])
    submit = SubmitField('Save')



class CustomerPreferenceForm(FlaskForm):
    preference_1 = SelectField('Preference 1', choices=[('', 'Tags'), ('cycling', 'cycling'), ('hiking', 'hiking'), ('food', 'food')], validators=[DataRequired()])
    preference_2 = SelectField('Preference 2', choices=[('', 'Tags'), ('cycling', 'cycling'), ('hiking', 'hiking'), ('food', 'food')], validators=[DataRequired()])
    preference_3 = SelectField('Preference 3', choices=[('', 'Tags'), ('cycling', 'cycling'), ('hiking', 'hiking'), ('food', 'food')], validators=[DataRequired()])
    submit = SubmitField('Save')
    def validate(self):
        if not Form.validate(self):
            return False
        result = True
        seen = set()
        for field in [self.preference_1, self.preference_2, self.preference_3]:
            if field.data in seen:
                field.errors.append('Please select three different tags.')
                result = False
            else:
                seen.add(field.data)
        return result


class EventDetailForm(FlaskForm):
    location = StringField('Location of Events', validators=[DataRequired()])
    tags = StringField('Tags', validators=[DataRequired()])
    profile_type = RadioField('Choose your profile type', choices=[('personal', 'Personal Account'), ('company', 'Company Account')], validators=[DataRequired()])
    company_details = TextAreaField('Company Details', validators=[Optional()])
    submit = SubmitField('Save')
    def validate_profile_type(self, company_details):
        if self.profile_type.data == 'company':
            if company_details.data == '':
                raise ValidationError('Company Details field cannot be empty')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')

class PersonalisedSearchForm(FlaskForm):
    keyword = StringField('Keyword Search')
    location = StringField('Location')
    category = SelectField('Category', choices=[('', 'All categories'), ('cycling', 'Cycling'), ('hiking', 'Hiking'), ('food', 'Food'), ('music', 'Music'), ('tours', 'Tours'), ('training', 'Training')])
    submitpsf = SubmitField('Search')

class SearchForm(FlaskForm):
    searchword = StringField('Search', validators=[DataRequired()])

class CreatorMsgForm(FlaskForm):
    content_msg = StringField('Message Body', validators=[DataRequired()])
    submit_msg = SubmitField('Send')

