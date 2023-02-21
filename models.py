

# from flask import Flask
# from flask_migrate import Migrate
# from flask_moment import Moment
# from flask_sqlalchemy import SQLAlchemy
# import datetime

# app = Flask(__name__)
# moment = Moment(app)
# app.config.from_object('config')
# db = SQLAlchemy(app)
# migrate = Migrate(app, db)

# # # ----------------------------------------------------------------------------#
# # # Models.
# # # ----------------------------------------------------------------------------#


# class Venue(db.Model):
#     __tablename__ = 'Venue'

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String)
#     genres = db.Column(db.ARRAY(db.String()), nullable=False)
#     address = db.Column(db.String(120))
#     city = db.Column(db.String(120))
#     state = db.Column(db.String(120))
#     phone = db.Column(db.String(120))
#     image_link = db.Column(db.String(500))
#     website = db.Column(db.String(120))
#     facebook_link = db.Column(db.String(120))
#     seeking_talent = db.Column(db.String(120), nullable=False, default=False)
#     seeking_description = db.Column(db.String(120))
#     shows = db.relationship('Shows', backref='Venue', lazy=True)


# class Artist(db.Model):
#     __tablename__ = 'Artists'

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String)
#     genres = db.Column(db.ARRAY(db.String()), nullable=False)
#     city = db.Column(db.String(120))
#     state = db.Column(db.String(120))
#     phone = db.Column(db.String(120))
#     image_link = db.Column(db.String(500))
#     website = db.Column(db.String(120))
#     facebook_link = db.Column(db.String(120))
#     seeking_venue = db.Column(db.String(120), nullable=False, default=False)
#     seeking_description = db.Column(db.String(120))
#     shows = db.relationship('Shows', backref='Artists', lazy=True)

# # TODO: implement any missing fields, as a database migration using Flask-Migrate

# # TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.


# class Shows(db.Model):
#     __tablename__ = 'Shows'

#     id = db.Column(db.Integer, primary_key=True)
#     artist_id = db.Column(db.Integer, db.ForeignKey(
#         'Artists.id'), nullable=False)
#     venue_id = db.Column(db.Integer, db.ForeignKey(
#         'Venue.id'), nullable=False)
#     # start_time = db.Column(datetime)
