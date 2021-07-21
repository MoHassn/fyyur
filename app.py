#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment

import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from past import *
from flask_migrate import Migrate
import sys
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
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  data = []
  cities = set()
  for venue in Venue.query.all():
    cities.add((venue.city, venue.state))
  for city in cities:
    venues = Venue.query.filter(Venue.city == city[0]).filter(Venue.state == city[1]).all()
    venues_data = []
    for venue in venues:
      shows = db.session.query(Shows).join(Venue).filter(Shows.venue_id == venue.id).all()
      upcoming_shows = 0
      for show in shows:
        if not past(show.start_time):
          upcoming_shows += 1
      venues_data.append({
        "id": venue.id,
        "name": venue.name,
        "num_upcoming_shows": upcoming_shows,
      })
    data.append({
    "city": city[0],
    "state": city[1],
    "venues": venues_data
    })

  return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  search_term = request.form.get("search_term")
  result = Venue.query.filter(Venue.name.ilike("%" + search_term + "%"))
  response_data = []
  for venue in result:
    shows = db.session.query(Shows).join(Venue).filter(Shows.venue_id == venue.id).all()
    upcoming_shows = 0
    for show in shows:
      if not past(show.start_time):
        upcoming_shows += 1
    response_data.append({
      "id": venue.id,
      "name": venue.name,
      "num_upcoming_shows": upcoming_shows
    })
  response = {
    "count": len(response_data),
    "data": response_data
  }

  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  venue = Venue.query.get(venue_id)
  shows = db.session.query(Shows).join(Venue).filter(Shows.venue_id == venue_id).all()
  data = {key:venue.__dict__[key] for key in["id", "name", "address", "city", "state", "phone", "website", "facebook_link", "seeking_talent", "seeking_description", "image_link"]}
  data["genres"] = json.loads(venue.__dict__['genres'])
  past_shows = []
  upcoming_shows = []
  for show in shows:
    if past(show.start_time):
      past_shows.append({
        "artist_id": show.artist.id,
        "artist_name": show.artist.name,
        "artist_image_link": show.artist.image_link,
        "start_time": show.start_time
      })
    else:
      upcoming_shows.append({
        "artist_id": show.artist.id,
        "artist_name": show.artist.name,
        "artist_image_link": show.artist.image_link,
        "start_time": show.start_time
      })
  data['past_shows'] = past_shows
  data['upcoming_shows'] = upcoming_shows
  data['past_shows_count'] = len(past_shows)
  data['upcoming_shows_count'] = len(upcoming_shows)

  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  form = VenueForm(request.form, meta={"csrf": False})
  if form.validate_on_submit():
    try:
      venue = Venue(
        name=form.name.data ,
        city=form.city.data ,
        state=form.state.data ,
        address=form.address.data ,
        phone=form.phone.data ,
        image_link=form.image_link.data ,
        genres=json.dumps(form.genres.data) ,
        facebook_link=form.facebook_link.data ,
        website=form.website_link.data ,
        seeking_talent=form.seeking_talent.data ,
        seeking_description=form.seeking_description.data ,
      )

      db.session.add(venue)
      db.session.commit()

      flash('Venue ' + request.form['name'] + ' was successfully listed!')
    except:
      print(sys.exc_info())
      db.session.rollback()

      flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
    finally:
      db.session.close()
      return render_template('pages/home.html')
  else:
    flash(form.errors)
    return render_template('forms/new_venue.html', form=form)

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  try:
    venue = Venue.query.get(venue_id)
    shows = db.session.query(Shows).join(Venue).filter(Shows.venue_id == venue_id).all()

    # first deleted the shows associated to this venue
    for show in show:
      db.session.delete(show)

    # delete the venue
    db.session.delete(venue)
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()
    return None

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  data = []
  for artist in Artist.query.all():
    data.append({
      "id": artist.id,
      "name": artist.name
    })

  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  search_term = request.form.get("search_term")
  result = Artist.query.filter(Artist.name.ilike("%" + search_term + "%"))
  response_data = []
  for artist in result:
    shows = db.session.query(Shows).join(Artist).filter(Shows.artist_id == artist.id).all()
    upcoming_shows = 0
    for show in shows:
      if not past(show.start_time):
        upcoming_shows += 1
    response_data.append({
      "id": artist.id,
      "name": artist.name,
      "num_upcoming_shows": upcoming_shows,
    })
  response = {
    "count": len(response_data),
    "data": response_data
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  artist = Artist.query.get(artist_id)
  shows = db.session.query(Shows).join(Artist).filter(Shows.artist_id == artist_id).all()
  data = {key:artist.__dict__[key] for key in ["id","name","city","state","phone","website","facebook_link","seeking_venue","seeking_description","image_link"]}
  data["genres"] = json.loads(artist.__dict__['genres'])
  past_shows = []
  upcoming_shows = []
  for show in shows:
    if past(show.start_time):
      past_shows.append({
        "venue_id": show.venue.id,
        "venue_name": show.venue.name,
        "venue_image_link": show.venue.image_link,
        "start_time": show.start_time
      })
    else:
      upcoming_shows.append({
        "venue_id": show.venue.id,
        "venue_name": show.venue.name,
        "venue_image_link": show.venue.image_link,
        "start_time": show.start_time
      })
  data['past_shows'] = past_shows
  data['upcoming_shows'] = upcoming_shows
  data['past_shows_count'] = len(past_shows)
  data['upcoming_shows_count'] = len(upcoming_shows)

  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  artist = Artist.query.get(artist_id)
  form = ArtistForm(
    name=artist.name,
    city=artist.city,
    state=artist.state,
    phone=artist.phone,
    image_link=artist.image_link,
    genres=json.loads(artist.genres),
    facebook_link=artist.facebook_link,
    website_link=artist.website,
    seeking_venue=artist.seeking_venue,
    seeking_description=artist.seeking_description,
  )

  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  try:
    form = ArtistForm()
    artist = Artist.query.get(artist_id)
    artist.name = form.name.data
    artist.city = form.city.data
    artist.state = form.state.data
    artist.phone = form.phone.data
    artist.image_link = form.image_link.data
    artist.genres = json.dumps(form.genres.data)
    artist.facebook_link = form.facebook_link.data
    artist.website = form.website_link.data
    artist.seeking_venue = form.seeking_venue.data
    artist.seeking_description = form.seeking_description.data

    db.session.add(artist)
    db.session.commit()
  except:
    print(sys.exc_info())
    db.session.rollback()
  finally:
    db.session.close()
    return redirect(url_for('show_artist', artist_id=artist_id))




@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  venue = Venue.query.get(venue_id)
  form = VenueForm(
    name= venue.name,
    city= venue.city,
    state= venue.state,
    address= venue.address,
    phone= venue.phone,
    image_link= venue.image_link,
    genres= json.loads(venue.genres),
    facebook_link= venue.facebook_link,
    website_link= venue.website,
    seeking_talent= venue.seeking_talent,
    seeking_description= venue.seeking_description,
  )

  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  try:
    form = VenueForm()
    venue = Venue.query.get(venue_id)

    venue.name = form.name.data
    venue.city = form.city.data
    venue.state = form.state.data
    venue.address = form.address.data
    venue.phone = form.phone.data
    venue.image_link = form.image_link.data
    venue.genres = json.dumps(form.genres.data)
    venue.facebook_link = form.facebook_link.data
    venue.website = form.website_link.data
    venue.seeking_talent = form.seeking_talent.data
    venue.seeking_description = form.seeking_description.data

    db.session.add(venue)
    db.session.commit()
  except:
    print(sys.exc_info())
    db.session.rollback()
  finally:
    db.session.close()
    return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  form = ArtistForm(request.form, meta={"csrf": False})
  if form.validate_on_submit():
    try:
      artist = Artist(
        name=form.name.data,
        city=form.city.data,
        state=form.state.data,
        phone=form.phone.data,
        image_link=form.image_link.data,
        genres=json.dumps(form.genres.data),
        facebook_link=form.facebook_link.data,
        website=form.website_link.data,
        seeking_venue=form.seeking_venue.data,
        seeking_description=form.seeking_description.data,
      )
      db.session.add(artist)
      db.session.commit()
      flash('Artist ' + request.form['name'] + ' was successfully listed!')
    except:
      print(sys.exc_info())
      db.session.rollback()
      flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')

    finally:
      db.session.close()
      return render_template('pages/home.html')
  else:
    flash(form.errors)
    return render_template('forms/new_artist.html', form=form)


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  data = []
  for show in Shows.query.all():
    data.append({
      "venue_id" : show.venue_id,
      "venue_name" : show.venue.name,
      "artist_id" : show.artist_id,
      "artist_name" : show.artist.name,
      "artist_image_link" : show.artist.image_link,
      "start_time" : show.start_time
    })

  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  form = ShowForm(request.form, meta={"csrf": False})
  if form.validate_on_submit():
    try:
      show = Shows(
        venue_id=form.venue_id.data,
        artist_id=form.artist_id.data,
        start_time=form.start_time.data,
      )
      db.session.add(show)
      db.session.commit()

      flash('Show was successfully listed!')
    except:
      print(sys.exc_info())
      db.session.rollback()
      flash('An error occurred. Show could not be listed.')
    finally:
      db.session.close()
      return render_template('pages/home.html')
  else:
    flash(form.errors)
    return render_template('forms/new_show.html', form=form)

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

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
