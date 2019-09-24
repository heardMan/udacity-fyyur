#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
import sys
from flask import Flask, render_template, request, Response, flash, redirect, url_for, jsonify
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

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

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


#  Index
#  ----------------------------------------------------------------
@app.route('/')
def index():
  return render_template('pages/home.html')

#  Venues - Read All
#  ----------------------------------------------------------------
@app.route('/venues')
def venues():
  
  venues = Venue.query.all()
  cities = []
  data1 = []

  for venue in venues:
    location = (venue.city, venue.state)
    _venue_ = {}
    _venue_['id'] = venue.id
    _venue_['name'] = venue.name
    upcoming_shows = []
    for show in venue.shows:
      if show.start_time > datetime.utcnow():
        upcoming_shows.append(show)
    _venue_['num_upcoming_shows'] = len(upcoming_shows)
    if location not in cities:
      cities.append(location)
      area = {}
      area['city'] = venue.city
      area['state'] = venue.state
      area['venues'] = []
      area['venues'].append(_venue_)
      data1.append(area)
    else:
      city_index = cities.index(location)
      data1[city_index]['venues'].append(_venue_)
  data2 = []
  for area in data1:
    sorted_venues = sorted(area['venues'], key=lambda k: k['num_upcoming_shows'], reverse=True)
    area['venues'] = sorted_venues
  sorted_areas = sorted(data1, key=lambda k: k['venues'][0]['num_upcoming_shows'], reverse=True)
  return render_template('pages/venues.html', areas=data1);

#  Venues - Search Route
#  ----------------------------------------------------------------
@app.route('/venues/search', methods=['POST'])
def search_venues():
  search_term = request.form.get('search_term', '')
  print(search_term)
  query_results = Venue.query.filter(Venue.name.ilike('%{}%'.format(search_term))).all()
  response={
    "count": len(query_results),
    "data": query_results
  }
  print(response["data"])
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

#  Venues - Read One
#  ----------------------------------------------------------------
@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):

  _venue_ = Venue.query.get(venue_id)
  
  print(_venue_.shows)
  venue = {}
  venue['id'] = _venue_.id
  venue['name'] = _venue_.name
  venue['genres'] = []

  for genre in _venue_.genre:
    venue['genres'].append(genre.genre)

  venue['address'] = _venue_.address
  venue['state'] = _venue_.state
  venue['city'] = _venue_.city
  venue['phone'] = _venue_.phone
  venue['website'] = _venue_.website
  venue['facebook_link'] = _venue_.facebook_url
  venue['seeking_talent'] = _venue_.seeking_talent
  venue['seeking_description'] = _venue_.seeking_description
  venue['image_link'] = _venue_.image_url
  venue['past_shows'] = []
  venue['upcoming_shows'] = []

  for item in _venue_.shows:
    now = datetime.utcnow()
    print(item.artist_id)
    _artist_ = Artist.query.filter_by(id = item.artist_id).all()[0]
    show = {}
    show['artist_id'] = item.artist_id
    show['start_time'] = item.start_time.strftime('%m/%d/%Y')
    print(item.start_time)
    show['artist_name'] = _artist_.name
    show['artist_image_link'] = _artist_.image_url
    if item.start_time < now:
      #print('PAST SHOW')
      venue['past_shows'].append(show)
    else:
      #print('UPCOMING SHOW')
      venue['upcoming_shows'].append(show)

  venue['past_shows_count'] = len(venue['past_shows'])
  venue['upcoming_shows_count'] = len(venue['upcoming_shows'])
  return render_template('pages/show_venue.html', venue=venue)

#  Venues - Create One - Render Form
#  ----------------------------------------------------------------
@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

#  Venues - Create One
#  ----------------------------------------------------------------
@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  
  error = False
  name=request.form.get('name', '')
  city=request.form.get('city', '')
  state=request.form.get('state', '')
  address=request.form.get('address', '')
  phone=request.form.get('phone', '')
  genres = request.form.getlist('genres')
  facebook_link = request.form.get('facebook_link', '')
  print(facebook_link2)

  try:

    new_venue = Venue(
      name=name,
      city=city,
      state=state,
      address=address,
      phone=phone,
      image_url='#',
      facebook_url=facebook_link
    )
    db.session.add(new_venue)
    db.session.flush()

    for genre in genres:
      new_venue_genre = Venue_Genre(
        venue_id=new_venue.id,
        genre=genre
      )
      db.session.add(new_venue_genre)

    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    flash('Venue ' + request.form['name'] + ' could not be listed!')
  else:
    flash('Venue ' + request.form['name'] + ' was successfully listed!')

  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

#  Venues - Delete One
#  ----------------------------------------------------------------
@app.route('/venues/<venue_id>/deleteplease', methods=['GET'])
def delete_venue(venue_id):
  
  error=False
  
  try:

    venue=Venue.query.get(venue_id)
    for genre in venue.genre:
      old_genre = Venue_Genre.query.get(genre.id)
      db.session.delete(old_genre)
    db.session.delete(venue)
    db.session.commit()

  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    flash('Venue could not be deleted!')
  else:
    flash('Venue was successfully deleted!')
  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return render_template('pages/home.html')

#  Artists - Read All
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  
  artists = Artist.query.all()
  data1 = []
  for artist in artists:
    _artist_ = {}
    _artist_['id'] = artist.id
    _artist_['name'] = artist.name
    data1.append(_artist_)
  print(data1)
  return render_template('pages/artists.html', artists=data1)

#  Artist - Search Route
#  ----------------------------------------------------------------
@app.route('/artists/search', methods=['POST'])
def search_artists():
  
  search_term = request.form.get('search_term', '')
  print(search_term)
  query_results = Artist.query.filter(Artist.name.ilike('%{}%'.format(search_term))).all()
  response={
    "count": len(query_results),
    "data": query_results
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

#  Artists - Read One
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):

  _artist_ = Artist.query.get(artist_id)
  _genres_ = Artist_Genre.query.filter_by(artist_id = artist_id).all()
  _shows_ = Show.query.filter_by(artist_id = artist_id).all()

  artist = {}
  artist['id'] = _artist_.id
  artist['name'] = _artist_.name
  artist['genres'] = []
  for item in _genres_:
    artist['genres'].append(item.genre)
  artist['state'] = _artist_.state
  artist['city'] = _artist_.city
  artist['phone'] = _artist_.phone
  artist['website'] = _artist_.website
  artist['facebook_link'] = _artist_.facebook_url
  artist['seeking_venue'] = _artist_.seeking_venue
  artist['seeking_description'] = _artist_.seeking_description
  artist['image_link'] = _artist_.image_url
  artist['past_shows'] = []
  artist['upcoming_shows'] = []
  for item in _shows_:
    now = datetime.utcnow()
    print(item.venue_id)
    _venue_ = Venue.query.filter_by(id = item.venue_id).all()[0]
    show = {}
    show['venue_id'] = item.venue_id
    show['start_time'] = item.start_time.strftime('%m/%d/%Y')
    print(item.start_time)
    show['venue_name'] = _venue_.name
    show['venue_image_link'] = _venue_.image_url
    if item.start_time < now:
      artist['past_shows'].append(show)
    else:
      artist['upcoming_shows'].append(show)
  artist['past_shows_count'] = len(artist['past_shows'])
  artist['upcoming_shows_count'] = len(artist['upcoming_shows'])
  return render_template('pages/show_artist.html', artist=artist)

#  Artists - Update One - Render Form
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist = Artist.query.get(artist_id)
  return render_template('forms/edit_artist.html', form=form, artist=artist)

#  Artists - Update One 
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  
  error = False
  name=request.form.get('name', '')
  city=request.form.get('city', '')
  state=request.form.get('state', '')
  phone=request.form.get('phone', '')
  genres = request.form.getlist('genres', '')
  facebook_link = request.form.get('facebook_link', '')

  try:

    artist = Artist.query.get(artist_id)
    old_genres = artist.genre

    for genre in old_genres:
     old_genre = Artist_Genre.query.get(genre.id)   
     db.session.delete(old_genre)

    artist.name=name
    artist.city=city
    artist.state=state
    artist.phone=phone
    artist.facebook_url = facebook_link

    for genre in genres:
      new_genre = Artist_Genre(
        artist_id=artist_id,
        genre=genre
      )
      db.session.add(new_genre)
    
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    flash('Artist ' + request.form.get('name') + ' could not be updated!')
  else:
    flash('Artist ' + request.form.get('name') + ' was successfully updated!')
  return redirect(url_for('show_artist', artist_id=artist_id))

#  Venues - Update One - Render Form
#  ----------------------------------------------------------------
@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue = Venue.query.get(venue_id)
  return render_template('forms/edit_venue.html', form=form, venue=venue)

#  Venues - Update One
#  ----------------------------------------------------------------
@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
 
  error = False
  name=request.form.get('name', '')
  address=request.form.get('address', '')
  city=request.form.get('city', '')
  state=request.form.get('state', '')
  phone=request.form.get('phone', '')
  genres = request.form.getlist('genres')
  facebook_link = request.form.get('facebook_link')

  try:

    venue = Venue.query.get(venue_id)
    old_genres = venue.genre

    for genre in old_genres:
     old_genre = Venue_Genre.query.get(genre.id) 
     db.session.delete(old_genre)
    
    venue.name=name
    venue.address=address
    venue.city=city
    venue.state=state
    venue.phone=phone
    venue.facebook_url = facebook_link

    for genre in genres:
      new_genre = Venue_Genre(
        venue_id=venue_id,
        genre=genre
      )
      db.session.add(new_genre)
    
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    flash('Venue ' + request.form.get('name', '') + ' could not be updated!')
  else:
    flash('Venue ' + request.form.get('name', '') + ' was successfully updated!')
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Artists - Create One - Render Form
#  ----------------------------------------------------------------
@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

#  Artist - Create One
#  ----------------------------------------------------------------
@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  
  error = False
  name=request.form.get('name', '')
  city=request.form.get('city', '')
  state=request.form.get('state', '')
  phone=request.form.get('phone', '')
  genres = request.form.getlist('genres')
  facebook_link = request.form.get('facebook_link', '')

  try:

    new_artist = Artist(
      name=name,
      city=city,
      state=state,
      phone=phone,
      image_url='#',
      facebook_url=request.form['facebook_link']
    )
    db.session.add(new_artist)
    db.session.flush()

    for genre in genres:
      new_artist_genre = Artist_Genre(
        artist_id=new_artist.id,
        genre=genre
      )
      db.session.add(new_artist_genre)

    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    flash('Artist ' + request.form.get('name', '') + ' could not be listed!')
  else:
    flash('Artist ' + request.form.get('name', '') + ' was successfully listed!')

  return render_template('pages/home.html')

#  Artist - Delete One
#  ----------------------------------------------------------------
@app.route('/artists/<artist_id>/deleteplease', methods=['GET'])
def delete_artist(artist_id):
 
  error=False
  try:

    artist=Atrist.query.get(artist_id)
    db.session.delete(artist)
    db.session.commit()

  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    flash('Artist could not be deleted!')
  else:
    flash('Artist was successfully deleted!')
  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return render_template('pages/home.html')

#  Shows - Read All
#  ----------------------------------------------------------------
@app.route('/shows')
def shows():
 
  _shows_ = Show.query.all()
  shows = []

  for item in _shows_:
    _artist_ = Artist.query.get(item.artist_id)
    _venue_ = Venue.query.get(item.venue_id)
    show = {}
    show['venue_id'] = item.venue_id
    show['venue_name'] = _venue_.name
    show['artist_id'] = item.artist_id
    show['artist_name'] = _artist_.name
    show['artist_image_link'] = _artist_.image_url
    show['start_time'] = item.start_time.strftime('%m/%d/%Y')
    shows.append(show)
  return render_template('pages/shows.html', shows=shows)

#  Shows - Create One - Render Form
#  ----------------------------------------------------------------
@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

#  Shows - Create One
#  ----------------------------------------------------------------
@app.route('/shows/create', methods=['POST'])
def create_show_submission():

  error = False
  artist_id=request.form.get('artist_id')
  venue_id=request.form.get('venue_id')
  start_time=request.form.get('start_time')

  try:

    new_show = Show(
      artist_id=artist_id,
      venue_id=venue_id,
      start_time=start_time
    )
    db.session.add(new_show)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    flash('Show could not be listed!')
  else:
    flash('Show was successfully listed!')
  return render_template('pages/home.html')

#  404 Error
#  ----------------------------------------------------------------
@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

#  500 Error
#  ----------------------------------------------------------------
@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
