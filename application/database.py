from sqlalchemy.ext.declarative import declarative_base

from flask_sqlalchemy import SQLAlchemy

# initialize sqlalchemy instance
db = SQLAlchemy()

# initialize declarative base
Base = declarative_base()
