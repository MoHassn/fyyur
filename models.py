#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

# I intended to make genres many to many relationship
# but I found it will result in chages to the form and the front-end
# so I will come back later
# The many to many relationship to enable venue to have multiple genres
# venue_genres = db.Table('venue_genres',
#   db.Column('venue_id',db.Integer, db.ForeignKey('Venue.id', primary_key=True)),
#   db.Column('genres_id',db.Integer, db.ForeignKey('Genres.id', primary_key=True))
# )

# the shows table
# shows = db.Table('Shows',
#   db.Column('venue_id', db.Integer, db.ForeignKey('Venue.id', primary_key=True)),
#   db.Column('artist_id', db.Integer, db.ForeignKey('Artist.id', primary_key=True)),
#   db.Column('start_time', db.DateTime, nullable=False)
# )
class Shows(db.Model):
  __tablename__ = 'Shows'
  id = db.Column(db.Integer, primary_key=True)
  venue_id = db.Column( db.Integer, db.ForeignKey('Venue.id'))
  artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'))
  start_time = db.Column(db.String(120))
  venue = db.relationship("Venue", back_populates='shows')
  artist = db.relationship("Artist", back_populates='shows')

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String(500))
    genres = db.Column(db.String(120))
    shows = db.relationship('Shows', back_populates='venue')

    # shows = db.relationship('Shows', secondary=shows, backref=db.backref('venues', lazy=True))
    # genres = db.relationship('Genres',secondary=venue_genres, backref=db.backref('venues', lazy=True) )


# class Genres(db.Model):
#   __tablename__ = 'Genres'

#   id = db.Column(db.Integer, primary_key=True)
#   name = db.Column(db.String(), nullable=False)


class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String(500))
    shows = db.relationship('Shows', back_populates='artist')


