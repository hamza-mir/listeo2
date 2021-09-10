from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)
app.config['SECRET_KEY'] = '4293218bb0b13ce0b676dfpo35n79209'
app.config['RECAPTCHA_PUBLIC_KEY'] = '6LcXGOsbAAAAANsx-0urRUuzat80Uzg9tlGgDzrL'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6LcXGOsbAAAAADl-BkIavzwu7xTqkBqaLxzFx8Ap'
app.config['STRIPE_PUBLIC_KEY'] = 'pk_test_51JWbYGIvSZNw2tGbPAbO1vFDfFdyVc9TO0O8Hc1m22uuNTCVONxV4vJXIGlzNr6apGwdKK8ZEuQubSt1BA52FVud00uP8Cphuy'
app.config['STRIPE_SECRET_KEY'] = 'sk_test_51JWbYGIvSZNw2tGbfzppq2V2cKmT5c9r9iZovr5tDakEW17ETw6j4dSM2jOyR68IjYUESy0omEE9dPpTI9N0WQ2p00ZTniQ0EK'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://testsite09:zj7y8mMb73KqkJ5@testsite09.mysql.pythonanywhere-services.com/testsite09$fizicality'
app.config['SQLALCHEMY_POOL_RECYCLE'] = 299
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'home'
login_manager.login_message_category = 'info'
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'hamzapython0@gmail.com'
app.config['MAIL_PASSWORD'] = 'hmwypzkescxldkkz'
mail = Mail(app)


from flaskapp import routes