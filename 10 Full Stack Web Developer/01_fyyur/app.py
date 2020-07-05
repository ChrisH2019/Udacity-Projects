#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, jsonify
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
from datetime import datetime
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

Show = db.Table('Show',
    db.Column('venue_id', db.Integer, db.ForeignKey('Venue.id'), primary_key=True),
    db.Column('artist_id', db.Integer, db.ForeignKey('Artist.id'), primary_key=True),
    db.Column('start_time', db.DateTime)
)

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String))
    facebook_link = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    website = db.Column(db.String)
    seeking_talent = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String)
    artists = db.relationship('Artist', secondary=Show, backref=db.backref('Venue', lazy=True))

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String))
    facebook_link = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    website = db.Column(db.String)
    seeking_venue = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String)

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

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # Retrieve all venues
  venues = db.session.query(Venue).all()

  # Retrieve distinct city and state pair in venues
  locations = set()
  for venue in venues:
    locations.add((venue.city, venue.state))

  # Append each location to data list
  data = []
  for loc in locations:
    data.append({
      'city': loc[0],
      'state': loc[1],
      'venues': []
    })

  # Append venue information to each loation's venue field
  for venue in venues:
    num_upcoming_shows = 0
    shows = db.session.query(Show).filter_by(venue_id=venue.id).all()

    # Count upcoming shows
    for show in shows:
      if show.start_time > datetime.now():
        num_upcoming_shows += 1

    # Add the number of upcoming shows in each location
    for item in data:
      if venue.city == item['city'] and venue.state == item['state']:
        item['venues'].append({
          'id': venue.id,
          'name': venue.name,
          'num_upcoming_shows': num_upcoming_shows
        })

  return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # implement search on artists with partial string search. Ensure it is case-insensitive.
  # Retrieve the search term
  search_term = request.form.get('search_term', '')

  # Retrieve records like search term
  venues = Venue.query.filter(Venue.name.ilike(f'%{search_term}%')).all()

  # Populate the data field in response
  data = []
  for venue in venues:
    num_upcoming_shows = 0
    shows = db.session.query(Show).filter_by(venue_id=venue.id).all()

    for show in shows:
      if show.start_time > datetime.now():
        num_upcoming_shows += 1
      
      data.append({
        'id': venue.id,
        'name': venue.name,
        'num_upcoming_shows': num_upcoming_shows
      })
  # Response to search term
  response = {
    'count': len(venues),
    'data': data
  }

  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # Retrieve the venue given vaue id
  venue = db.session.query(Venue).filter_by(id=venue_id).first()

  # Retrieve the shows given value id
  shows = db.session.query(Show).filter_by(venue_id=venue_id).all()

  # Retrieve upcoming & past shows
  upcoming_shows, past_shows = [], []
  for show in shows:
    artist = {
        'artist_id': show.artist_id,
        'artist_name': Artist.query.filter_by(id=show.artist_id).first().name,
        'artist_image_link': Artist.query.filter_by(id=show.artist_id).first().image_link,
        'start_time': format_datetime(str(show.start_time))
    }
    if show.start_time > datetime.now():
      upcoming_shows.append(artist)
    else:
      past_shows.append(artist)

  # Data to be shown for given venue id
  data = {
    'name': venue.name,
    'id': venue.id,
    'genres': ''.join(venue.genres[1:-1]).split(','),
    'city': venue.city,
    'state': venue.state,
    'address': venue.address,
    'phone': venue.phone,
    'website': venue.website,
    'facebook_link': venue.facebook_link,
    'seeking_talent': venue.seeking_talent,
    'seeking_description': venue.seeking_description,
    'upcoming_shows_count': len(upcoming_shows),
    'upcoming_shows': upcoming_shows,
    'past_shows_count': len(past_shows),
    'past_shows': past_shows,
    'image_link': venue.image_link
  }

  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # Insert form data as a new Venue record in the db
  try:
    new_venue = Venue(
      name = request.form['name'],
      city = request.form['city'],
      state = request.form['state'],
      address = request.form['address'],
      phone = request.form['phone'],
      genres = request.form.getlist('genres'),
      facebook_link = request.form['facebook_link'],
      image_link = request.form['image_link'],
      website = request.form['website'],
      seeking_talent = True if request.form['seeking_talent'] == 'Yes' else False,
      seeking_description = request.form['seeking_description']
    )
    db.session.add(new_venue)
    db.session.commit()
    # on successful db insert, flash success
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
  except:
    db.session.rollback()
    # On unsuccessful db insert, flash an error instead.
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
  finally:
    db.session.close()

  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  # Retrieve the venue to be deleted
  try:
    venue = db.session.query(Venue).filter_by(id=venue_id).first()
    venue_name = venue.name
    db.session.delete(venue)
    db.session.commit()
    flash('Venue ' + venue_name + ' was successfully deleted.')
  except:
    db.session.rollback()
    flash('An error occurred. Venue ' + venue_name + ' could not be deleted')
  finally:
    db.session.close()

  return jsonify({'success':True})

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # Retreive all artists
  artists = db.session.query(Artist).all()

  # Append the artist id and name
  data = []
  for artist in artists:
    data.append({
      'id': artist.id,
      'name': artist.name
    })

  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # implement search on artists with partial string search. Ensure it is case-insensitive.
  # Retrieve the search term
  search_term = request.form.get('search_term', '')

  # Retrieve artist record like search term
  artists = Artist.query.filter(Artist.name.ilike(f'%{search_term}%')).all()

  # Populate the data field in response
  data = []
  for artist in artists:
    num_upcoming_shows = 0
    shows = db.session.query(Show).filter_by(artist_id=artist.id).all()

    for show in shows:
      if show.start_time > datetime.now():
        num_upcoming_shows += 1
      
      data.append({
        'id': artist.id,
        'name': artist.name,
        'num_upcoming_shows': num_upcoming_shows
      })

  # Response to search term
  response = {
    'count': len(artists),
    'data': data
  }

  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # Retrieve the artist given artist id
  artist = db.session.query(Artist).filter_by(id=artist_id).first()

  # Retrieve the shows given value id
  shows = db.session.query(Show).filter_by(artist_id=artist_id).all()

  # Retrieve upcoming & past shows
  upcoming_shows, past_shows = [], []
  for show in shows:
    venue = {
      'venue_id': show.venue_id,
      'venue_name': Venue.query.filter_by(id=show.venue_id).first().name,
      'venue_image_link': Venue.query.filter_by(id=show.venue_id).first().image_link,
      'start_time': format_datetime(str(show.start_time))
    }
    if show.start_time > datetime.now():
      upcoming_shows.append(venue)
    else:
      past_shows.append(venue)

  # An artist entry to be shown
  data = {
    'name': artist.name,
    'id': artist.id,
    'genres': ''.join(artist.genres[1:-1]).replace('"', '').split(','),
    'city': artist.city,
    'state': artist.state,
    'phone': artist.phone,
    'website': artist.website,
    'facebook_link': artist.facebook_link,
    'seeking_venue': artist.seeking_venue,
    'seeking_description': artist.seeking_description,
    'upcoming_shows_count': len(upcoming_shows),
    'upcoming_shows': upcoming_shows,
    'past_shows_count': len(past_shows),
    'past_shows': past_shows,
    'image_link': artist.image_link
  }
  
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist = db.session.query(Artist).filter_by(id=artist_id).first()
  form['name'].data = artist.name
  form['city'].data = artist.city
  form['state'].data = artist.state
  form['phone'].data = artist.phone
  form['genres'].data = artist.genres
  form['facebook_link'].data = artist.facebook_link
  form['image_link'].data = artist.image_link
  form['website'].data = artist.website
  form['seeking_venue'].data = artist.seeking_venue
  form['seeking_description'].data = artist.seeking_description 

  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  # Retrieve the artist to be edited given value id
  artist = db.session.query(Artist).filter_by(id=artist_id).first()
  
  # Update the venue fields
  try:
    artist.name = request.form['name']
    artist.city = request.form['city']
    artist.state = request.form['state']
    artist.phone = request.form['phone']
    if request.form.getlist('genres'):
      artist.genres = request.form.getlist('genres')
    artist.facebook_link = request.form['facebook_link']
    artist.image_link = request.form['image_link']
    artist.website = request.form['website']
    artist.seeking_venue = True if request.form['seeking_venue'] == 'Yes' else False
    artist.seeking_description = request.form['seeking_description']

    db.session.commit()
    flash('Venue ' + request.form['name'] + ' was successfully updated.')
  except:
    db.session.rollback()
    flash('An error occurred. ' + request.form['name'] + ' Venue could not be updated.')
  finally:
    db.session.close()

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  # Retrieve the venue given venue id
  form = VenueForm()
  venue = db.session.query(Venue).filter_by(id=venue_id).first()
  form['name'].data = venue.name
  form['city'].data = venue.city
  form['state'].data = venue.state
  form['address'].data = venue.address
  form['phone'].data = venue.phone
  form['genres'].data = venue.genres
  form['facebook_link'].data = venue.facebook_link
  form['image_link'].data = venue.image_link
  form['website'].data = venue.website
  form['seeking_talent'].data = venue.seeking_talent
  form['seeking_description'].data = venue.seeking_description  

  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  # Retrieve the venue to be edited given value id
  venue = db.session.query(Venue).filter_by(id=venue_id).first()
  
  # Update the venue fields
  try:
    venue.name = request.form['name']
    venue.city = request.form['city']
    venue.state = request.form['state']
    venue.address = request.form['address']
    venue.phone = request.form['phone']
    if request.form.getlist('genres'):
      venue.genres = request.form.getlist('genres')
    venue.facebook_link = request.form['facebook_link']
    venue.image_link = request.form['image_link']
    venue.website = request.form['website']
    venue.seeking_talent = True if request.form['seeking_talent'] == 'Yes' else False
    venue.seeking_description = request.form['seeking_description']

    db.session.commit()
    flash('Venue ' + request.form['name'] + ' was successfully updated.')
  except:
    db.session.rollback()
    flash('An error occurred. ' + request.form['name'] + ' Venue could not be updated.')
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
  # called upon submitting the new artist listing form
  try:
    new_artist = Artist(
      name = request.form['name'],
      city = request.form['city'],
      state = request.form['state'],
      phone = request.form['phone'],
      genres = request.form.getlist('genres'),
      facebook_link = request.form['facebook_link'],
      image_link = request.form['image_link'],
      website = request.form['website'],
      seeking_venue = True if request.form['seeking_venue'] == 'Yes' else False,
      seeking_description = request.form['seeking_description']
    )
    db.session.add(new_artist)
    db.session.commit()
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
  except:
    db.session.rollback()
    flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
  finally:
    db.session.close()

  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # Retreive all shows
  shows = db.session.query(Show).all()

  # Append artist, venue & show
  data = []
  for show in shows:
    data.append({
      'venue_id': show.venue_id,
      'venue_name': db.session.query(Venue).filter_by(id=show.venue_id).first().name,
      'artist_id': show.artist_id,
      'artist_name': db.session.query(Artist).filter_by(id=show.artist_id).first().name,
      'artist_image_link': db.session.query(Artist).filter_by(id=show.artist_id).first().image_link,
      'start_time': format_datetime(str(show.start_time))
    })
  
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  try:
    new_show = Show.insert().values(
      artist_id = request.form['artist_id'],
      venue_id = request.form['venue_id'],
      start_time = request.form['start_time']
    )
    db.session.execute(new_show)
    db.session.commit()
    flash('Show was successfully listed!')
  except:
    db.session.rollback()
    flash('An error occurred. Show could not be listed.')
  finally:
    db.session.close()

  return render_template('pages/home.html')

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
