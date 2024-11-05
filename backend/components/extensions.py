from flask_security import SQLAlchemyUserDatastore
from flask_bcrypt import Bcrypt
from flask_caching import Cache
from .models import db, User, Role

bcrypt = Bcrypt()
cache = Cache()
datastore = SQLAlchemyUserDatastore(db, User, Role)