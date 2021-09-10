from datetime import datetime
from os import name
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flaskapp import app, db , login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    stripe_acc_id = db.Column(db.String(30), unique=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    first_name =  db.Column(db.String(20))
    last_name =  db.Column(db.String(20))
    contact_number = db.Column(db.Integer)
    adderss = db.Column(db.String(120))
    city = db.Column(db.String(30))
    loc_state = db.Column(db.String(30))
    zip_code = db.Column(db.Integer)
    country = db.Column(db.String(30))
    personal_details_complete = db.Column(db.Boolean, nullable=False, default=False)
    is_creator = db.Column(db.Boolean, nullable=False, default=False)
    events = db.relationship('Event', backref='event_author', lazy=True)
    tagp1 = db.Column(db.String(20))
    tagp2 = db.Column(db.String(20))
    tagp3 = db.Column(db.String(20))
    preferences_complete = db.Column(db.Boolean, nullable=False, default=False)
    tags = db.relationship('Tag', backref='tag_author', lazy=True)
    location = db.Column(db.String(255), default='')
    is_profile_company = db.Column(db.Boolean, nullable=False, default=False)
    company_details = db.Column(db.String(1800), default='')
    event_details_complete = db.Column(db.Boolean, nullable=False, default=False)
    is_profile_complete = db.Column(db.Boolean, nullable=False, default=False)
    is_account_verified = db.Column(db.Boolean, nullable=False, default=False)
    times_logged_in = db.Column(db.Integer, nullable=False, default=0)
    wishlistitems = db.relationship('Wishlist', backref='wishlist_user', lazy=True)
    cartitems = db.relationship('Cart', backref='cart_user', lazy=True)
    is_stripe_complete = db.Column(db.Boolean, nullable=False, default=False)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    def get_verify_account_token(self, expires_sec=600):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user2_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    @staticmethod
    def verify_account_verification_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user2_id = s.loads(token)['user2_id']
        except:
            return None
        return User.query.get(user2_id)


class Event(db.Model):
    __tablename__ = "event"

    id = db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    is_enabled = db.Column(db.Boolean, nullable=False, default=False)
    title = db.Column(db.String(30), nullable=False)
    description = db.Column(db.String(1800), nullable=False)
    banner = db.Column(db.String(20), nullable=False, default='defaultEventBanner.jpg')
    location = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False)
    date_end = db.Column(db.Date)
    time = db.Column(db.Time, nullable=False)
    time_end = db.Column(db.Time)
    days = db.Column(db.String(255), nullable=False)
    pre_knowledge = db.Column(db.String(255), nullable=False)
    tags = db.Column(db.String(255), nullable=False)
    schedule = db.Column(db.String(255))
    image1 = db.Column(db.String(20), nullable=False, default='defaultEventBanner.jpg')
    image2 = db.Column(db.String(20))
    image3 = db.Column(db.String(20))
    image4 = db.Column(db.String(20))
    image5 = db.Column(db.String(20))
    image6 = db.Column(db.String(20))
    image7 = db.Column(db.String(20))
    direction = db.Column(db.String(255))
    equipment = db.Column(db.String(255))
    min_tickets = db.Column(db.Integer)
    offers_bool = db.Column(db.Boolean, nullable=False, default=False)
    attendee1 = db.Column(db.Integer)
    discount1 = db.Column(db.Integer)
    attendee2 = db.Column(db.Integer)
    discount2 = db.Column(db.Integer)
    attendee3 = db.Column(db.Integer)
    discount3 = db.Column(db.Integer)
    attendee4 = db.Column(db.Integer)
    discount4 = db.Column(db.Integer)
    attendee5 = db.Column(db.Integer)
    discount5 = db.Column(db.Integer)
    attendee6 = db.Column(db.Integer)
    discount6 = db.Column(db.Integer)
    attendee7 = db.Column(db.Integer)
    discount7 = db.Column(db.Integer)
    attendee8 = db.Column(db.Integer)
    discount8 = db.Column(db.Integer)
    fee_cancel = db.Column(db.Boolean, nullable=False, default=False)
    prioritize = db.Column(db.Boolean, nullable=False, default=False)


class Customer(db.Model):
    __tablename__ = "customer"

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)


class Wishlist(db.Model):
    __tablename__ = "wishlist"

    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    event = db.relationship('Event', backref='event_wishlist', lazy=True)
    user = db.relationship('User', backref='wishlist_user', lazy=True)

class Cart(db.Model):
    __tablename__ = "cart"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    event = db.relationship('Event', backref='event_cart', lazy=True)
    user = db.relationship('User', backref='user_cart', lazy=True)

class Notification(db.Model):
    __tablename__ = "notification"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    read = db.Column(db.Boolean, nullable=False, default=False)
    event = db.Column(db.String(30), nullable=False)
    title = db.Column(db.String(30), nullable=False)
    thumb = db.Column(db.String(20), nullable=False, default='defaultEventBanner.jpg')
    fullname =  db.Column(db.String(20))

class Messages(db.Model):
    __tablename__ = "message"

    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    sendername = db.Column(db.String(40), nullable=False)
    receiver = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    read = db.Column(db.Boolean, nullable=False, default=False)
    content = db.Column(db.String(300), nullable=False)

class Booking(db.Model):
    __tablename__ = "booking"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)

class Tag(db.Model):
    __tablename__ = "tag"

    id = db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    tag_title = db.Column(db.String(255), nullable=False, default='')