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
from models import *

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db.init_app(app)
migrate = Migrate(app, db)

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
  #get venue data
  query_results = Venue.query.all()
  cities = []
  data = []

  for result in query_results:
    #add location to sort list
    location = (result.city, result.state)
    #create custom venue dict
    venue = {
      'id': result.id,
      'name': result.name
    }
    #create upcoming show list
    upcoming_shows = [
      show for show in result.shows if show.start_time > datetime.utcnow()
      ]
    
    #create and set venue upcoming shows
    venue['num_upcoming_shows'] = len(upcoming_shows)
    
    if location not in cities:
      #if the location does not exist in data object then add it
      cities.append(location)
      #instantiate new area dict
      area = {
        'city': result.city,
        'state': result.state,
        'venues': [venue]
      }
      #add new area to data list
      data.append(area)
    else:
      #area already in list -- just append venue to area
      city_index = cities.index(location)
      data[city_index]['venues'].append(venue)

  #sort each venue with in each area based on the number of shows
  for area in data:
    area['venues'] = sorted(area['venues'], key=lambda k: k['num_upcoming_shows'], reverse=True)
  # sort all the areas by the area with the top venue with the most shows
  sorted_areas = sorted(data, key=lambda k: k['venues'][0]['num_upcoming_shows'], reverse=True)
  return render_template('pages/venues.html', areas=data)

#  Venues - Search Route
#  ----------------------------------------------------------------
@app.route('/venues/search', methods=['POST'])
def search_venues():

  #get search term from search form
  search_term = request.form.get('search_term', '')
  #get data from database
  query_results = Venue.query.filter(Venue.name.ilike('%{}%'.format(search_term))).all()
  #instantiate response dict
  response={
    "count": len(query_results),
    "data": query_results
  }
  
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

#  Venues - Read One
#  ----------------------------------------------------------------
@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):

  #get venue data
  query_result = Venue.query.get(venue_id)
  shows = []
  for item in query_result.shows:
    now = datetime.utcnow()
    #get artist info
    artist = Artist.query.get(item.artist_id)
    #instantiate a new show instance
    show = {
      'artist_id': item.artist_id,
      'start_time': item.start_time.strftime('%m/%d/%Y'),
      'artist_name': artist.name,
      'artist_image_link': artist.image_url
    }
    #sort sort based on past or upcoming
    if item.start_time < now:
      #add to past shows if data was before now
      venue['past_shows'].append(show)
    else:
      #add to upcoming shows if data was after now
      venue['upcoming_shows'].append(show)
  
  #convert query from class to dict for manipulation
  venue = {
    'id': query_result.id,
    'name': query_result.name,
    'genres': [
      genre.genre for genre in query_result.genre
      ],
    'address': query_result.address,
    'state': query_result.state,
    'city': query_result.city,
    'phone': query_result.phone,
    'website': query_result.website,
    'facebook_link': query_result.facebook_url,
    'seeking_talent': query_result.seeking_talent,
    'seeking_description': query_result.seeking_description,
    'image_link': query_result.image_url,
    'past_shows':  [],
    'upcoming_shows': []
  }
  
  #create shows list
  
  #create and define past shows count property
  venue['past_shows_count'] = len(venue['past_shows'])
  #create and define upcoming shows count property
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
  #set error state
  error = False
  
  try:
    #instantiate new venue instance
    new_venue = Venue(
      name=request.form.get('name', ''),
      city=request.form.get('city', ''),
      state=request.form.get('state', ''),
      address=request.form.get('address', ''),
      phone=request.form.get('phone', ''),
      image_url='#',
      facebook_url=request.form.get('facebook_link', '')
    )
    # add instance to database
    db.session.add(new_venue)
    #flush session to get id of newly created artist
    db.session.flush()
    #get list of genres from form submission
    genres = request.form.getlist('genres')
    #create art genre instance
    for genre in genres:
      #create art genre instance
      new_venue_genre = Venue_Genre(
        venue_id=new_venue.id,
        genre=genre
      )
      #add each genre to the association table
      db.session.add(new_venue_genre)

    db.session.commit()
  except:
    #error occured set error to true
    error = True
    #roll back session
    db.session.rollback()
    #print error
    print(sys.exc_info())
  
  finally:
    #close the session 
    db.session.close()

  #on submit flash the user a status of the submission request 
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
  #set error state
  error=False
  
  try:
    #get venue to delete
    query_result=Venue.query.get(venue_id)

    for genre in query_result.genre:
      #get old genre instances
      old_genre = Venue_Genre.query.get(genre.id)
      #delete old genre instances
      db.session.delete(old_genre)
    # delete venue
    db.session.delete(venue)
    db.session.commit()

  except:
    #error occured set error to true
    error = True
    #roll back session
    db.session.rollback()
    #print error
    print(sys.exc_info())
  
  finally:
    #close the session 
    db.session.close()

  #on submit flash the user a status of the submission request 
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
  
  # get artist information
  query_results = Artist.query.all()
  #create data list
  data = []

  for result in query_results:
    # format each result into an artist instance for later manipulation
    artist = {
       'id': result.id,
       'name': result.name
    }
    #append artist to data list 
    data.append(artist)
  
  return render_template('pages/artists.html', artists=data)

#  Artist - Search Route
#  ----------------------------------------------------------------
@app.route('/artists/search', methods=['POST'])
def search_artists():
  # get search term value from form submission
  search_term = request.form.get('search_term', '')
  # query the database using search query
  query_results = Artist.query.filter(Artist.name.ilike('%{}%'.format(search_term))).all()
  #format result dict
  response={
    "count": len(query_results),
    "data": query_results
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

#  Artists - Read One
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):

  # get artist info
  query_result = Artist.query.get(artist_id)
  #create artist dict
  artist = {
    'id': query_result.id,
    'name': query_result.name,
    'genres': [],
    'state': query_result.state,
    'city': query_result.city,
    'phone': query_result.phone,
    'website': query_result.website,
    'facebook_link': query_result.facebook_url,
    'seeking_venue': query_result.seeking_venue,
    'seeking_description': query_result.seeking_description,
    'image_link': query_result.image_url,
    'past_shows': [],
    'upcoming_shows': []
  }
  #add genres to artist dict
  for genre in query_result.genre:
    artist['genres'].append(genre.genre)
  #add and sort shows to artist dict
  for item in query_result.shows:
    now = datetime.utcnow()
    # get venue data
    venue = Venue.query.get(item.venue_id)
    # create show inastance
    show = {
      'venue_id': item.venue_id,
      'start_time': item.start_time.strftime('%m/%d/%Y'),
      'venue_name': venue.name,
      'venue_image_link': venue.image_url
    }
    
    #sort shows into upcoming or past
    if item.start_time < now:
      #add to past shows
      artist['past_shows'].append(show)
    else:
      #add to upcoming shows
      artist['upcoming_shows'].append(show)

  #create and set past shows count property    
  artist['past_shows_count'] = len(artist['past_shows'])
  #create and set upcoming shows count property  
  artist['upcoming_shows_count'] = len(artist['upcoming_shows'])
  return render_template('pages/show_artist.html', artist=artist)

#  Artists - Update One - Render Form
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  #get venue data
  query_result = Artist.query.get(artist_id)
  return render_template('forms/edit_artist.html', form=form, artist=query_result)

#  Artists - Update One 
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  
  #set error state
  error = False
  
  try:
    #get the queried artist data
    artist = Artist.query.get(artist_id)
    #get the old genres to be deleted
    old_genres = artist.genre
    for genre in old_genres:
     #get old genre instance
     old_genre = Artist_Genre.query.get(genre.id)
     #delete old genre instance   
     db.session.delete(old_genre)
    #update properties on artist instance in database
    artist.name=request.form.get('name', '')
    artist.city=request.form.get('city', '')
    artist.state=request.form.get('state', '')
    artist.phone=request.form.get('phone', '')
    artist.facebook_url = request.form.get('facebook_link', '')

    #get new genres from form submission
    genres = request.form.getlist('genres', '')
    for genre in genres:
      #instantiate artist genre
      new_genre = Artist_Genre(
        artist_id=artist_id,
        genre=genre
      )
      #add each relation to table
      db.session.add(new_genre)
    
    db.session.commit()
  except:
    #error occured set error to true
    error = True
    #roll back session
    db.session.rollback()
    #print error
    print(sys.exc_info())
  
  finally:
    #close the session 
    db.session.close()

  #on submit flash the user a status of the submission request 
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
  #get venue data
  query_result = Venue.query.get(venue_id)
  return render_template('forms/edit_venue.html', form=form, venue=query_result)

#  Venues - Update One
#  ----------------------------------------------------------------
@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
 
  #set error state
  error = False
  
  try:
    #get the queried venue data
    venue = Venue.query.get(venue_id)
    #get the old genres to be deleted
    old_genres = venue.genre
    for genre in old_genres:
     #get old genre instance
     old_genre = Venue_Genre.query.get(genre.id) 
     #delete old genre instance
     db.session.delete(old_genre)
    
    #update properties on venue instance in database
    venue.name=request.form.get('name', '')
    venue.address=request.form.get('address', '')
    venue.city=request.form.get('city', '')
    venue.state=request.form.get('state', '')
    venue.phone=request.form.get('phone', '')
    venue.facebook_url = request.form.get('facebook_link')

    #get new genres from form submission
    genres = request.form.getlist('genres')
    for genre in genres:
      #instantiate venue genre
      new_genre = Venue_Genre(
        venue_id=venue_id,
        genre=genre
      )
      #add each relation to table
      db.session.add(new_genre)
    
    db.session.commit()
  except:
    #error occured set error to true
    error = True
    #roll back session
    db.session.rollback()
    #print error
    print(sys.exc_info())
  
  finally:
    #close the session 
    db.session.close()

  #on submit flash the user a status of the submission request 
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
  
  #set error state
  error = False

  try:
    #instantiate new artist instance
    new_artist = Artist(
      name=request.form.get('name', ''),
      city=request.form.get('city', ''),
      state=request.form.get('state', ''),
      phone=request.form.get('phone', ''),
      image_url='#',
      facebook_url=request.form.get('facebook_link', '')
    )
    # add instance to database
    db.session.add(new_artist)
    #flush session to get id of newly created artist
    db.session.flush()
    #get list of genres from form submission
    genres = request.form.getlist('genres')
    for genre in genres:
      #create art genre instance
      new_artist_genre = Artist_Genre(
        artist_id=new_artist.id,
        genre=genre
      )
      #add each genre to the association table
      db.session.add(new_artist_genre)

    db.session.commit()
  except:
    #error occured set error to true
    error = True
    #roll back session
    db.session.rollback()
    #print error
    print(sys.exc_info())
  
  finally:
    #close the session 
    db.session.close()

  #on submit flash the user a status of the submission request 
  if error:
    flash('Artist ' + request.form.get('name', '') + ' could not be listed!')
  else:
    flash('Artist ' + request.form.get('name', '') + ' was successfully listed!')

  return render_template('pages/home.html')

#  Artist - Delete One
#  ----------------------------------------------------------------
@app.route('/artists/<artist_id>/deleteplease', methods=['GET'])
def delete_artist(artist_id):
 
  #set error state
  error=False

  try:
    #get artist info
    artist=Atrist.query.get(artist_id)
    #delete artist instance
    db.session.delete(artist)
    db.session.commit()

  except:
    #error occured set error to true
    error = True
    #roll back session
    db.session.rollback()
    #print error
    print(sys.exc_info())
  
  finally:
    #close the session 
    db.session.close()

  #on submit flash the user a status of the submission request 
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
  # get shows data from database
  _shows_ = Show.query.all()
  #instantiate shows list
  shows = []
  
  #process each result
  for result in _shows_:
    #get artist info
    _artist_ = Artist.query.get(result.artist_id)
    #get venue info
    _venue_ = Venue.query.get(result.venue_id)
    #create custom show dict
    show = {
      'venue_id' : result.venue_id,
      'venue_name' : _venue_.name,
      'artist_id' : result.artist_id,
      'artist_name' : _artist_.name,
      'artist_image_link': _artist_.image_url,
      'start_time': result.start_time.strftime('%m/%d/%Y')
    }
    #append show to list
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

  #set error state
  error = False

  try:
    #instantiate new show object 
    new_show = Show(
      artist_id=request.form.get('artist_id'),
      venue_id=request.form.get('venue_id'),
      start_time=request.form.get('start_time')
    )
    #add object to data base
    db.session.add(new_show)
    db.session.commit()
  except:
    #error occured set error to true
    error = True
    #roll back session
    db.session.rollback()
    #print error
    print(sys.exc_info())
  finally:
    #close the session 
    db.session.close()

  #on submit flash the user a status of the submission request  
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
