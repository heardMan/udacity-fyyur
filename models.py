
from flask_sqlalchemy import SQLAlchemy

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

db = SQLAlchemy()

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    #set the one to many ralationship at the parent level
    genre = db.relationship('Venue_Genre', backref='Venue')
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_url = db.Column(db.String(500))
    facebook_url = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String(120))
    #set the one to many ralationship at the parent level
    shows = db.relationship('Show', backref='Venue')

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    #set the one to many ralationship at the parent level
    genre = db.relationship("Artist_Genre", backref="Artist_Genre") 
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_url = db.Column(db.String(500), nullable=False)
    facebook_url = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String(120))
    #set the one to many ralationship at the parent level
    shows = db.relationship('Show', backref="Artist")

class Show(db.Model):
    __tablename__ = 'Show'

    id = db.Column(db.Integer, primary_key=True)
    #set the one to many ralationship at the child level
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'))
    #set the one to many ralationship at the child level
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'))
    start_time = db.Column(db.DateTime(timezone=False), nullable=False)

class Venue_Genre(db.Model):
      __tablename__ = 'Venue_Genre'

      id = db.Column(db.Integer, primary_key=True)
      #set the one to many ralationship at the child level
      venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'))
      genre = db.Column(db.String(120), nullable=False)

class Artist_Genre(db.Model):
      __tablename__ = 'Artist_Genre'

      id = db.Column(db.Integer, primary_key=True)
      #set the one to many ralationship at the child level
      artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'))
      genre = db.Column(db.String(120), nullable=False)