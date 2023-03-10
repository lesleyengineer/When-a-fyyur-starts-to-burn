# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, jsonify, abort, session
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
import sys
import datetime
from models import *

# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#

# app = Flask(__name__)
# moment = Moment(app)
# app.config.from_object('config')
# # db = SQLAlchemy(app)
# db.init_app(app)
# migrate = Migrate(app, db)

# TODO: connect to a local postgresql database - DONE


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

# # TODO: implement any missing fields, as a database migration using Flask-Migrate


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

#     # TODO: implement any missing fields, as a database migration using Flask-Migrate

# # TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.


# class Shows(db.Model):
#     __tablename__ = 'Shows'

#     id = db.Column(db.Integer, primary_key=True)
#     artist_id = db.Column(db.Integer, db.ForeignKey(
#         'Artists.id'), nullable=False)
#     venue_id = db.Column(db.Integer, db.ForeignKey(
#         'Venue.id'), nullable=False)
#     # start_time = db.Column(db.Datetime, nullable=False)


# ----------------------------------------------------------------------------#
# Filters.
# ----------------------------------------------------------------------------#


def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format, locale='en')


app.jinja_env.filters['datetime'] = format_datetime

# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#


@ app.route('/')
def index():
    return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@ app.route('/venues')
def venues():
    # TODO: replace with real venues data.
    #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
    data = []
    venues = Venue.query.all()
    for thisvenue in venues:
        area = {
            'city': thisvenue.city,
            'state': thisvenue.state,
            'venues': [{
                'id': thisvenue.id,
                'name': thisvenue.name
            }]
        }
        data.append(area)

    return render_template('pages/venues.html', areas=data)


@ app.route('/venues/search', methods=['POST'])
def search_venues():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"

    search_term = request.form.get('search_term', '')
    search_results = Venue.query.filter(
        Venue.name.ilike(f'%{search_term}%')).all()
    response = {
        'count': len(search_results),
        'data': []
    }
    for venue in search_results:
        response['data'].append({
            'id': venue.id,
            'name': venue.name
        })

    return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))


@ app.route('/venues/<int:venue_id>')
def show_venue(venue_id):

    venue = Venue.query.get(venue_id)

    current_time = datetime.now()

    upcoming_shows = db.session.query(Shows).join(Venue).filter(
        Shows.venue_id == venue_id).filter
    (Shows.start_time > datetime.now()).all()

    for show in upcoming_shows:
        if show.start_time > datetime.now():
            upcoming_shows.append({
                'artist_id': show.artists_id,
                'artist_name': Artist.query.filter_by(id=show.artist_id).first().name,
                'artist_image_link': Artist.query.filter_by(id=show.artist_id).first().image_link,
                'start_time': format_datetime(str(show.start_time))
            })
        return upcoming_shows

    past_shows = db.session.query(Shows).join(Venue).filter(
        Shows.venue_id == venue_id).filter
    (Shows.start_time > datetime.now()).all()

    for show in past_shows:
        if show.start_time < datetime.now():
            past_shows.append({
                'artist_id': show.artists_id,
                'artist_name': Artist.query.filter_by(id=show.artist_id).first().name,
                'artist_image_link': Artist.query.filter_by(id=show.artist_id).first().image_link,
                'start_time': format_datetime(str(show.start_time))
            })
        return past_shows

    # shows the venue page with the given venue_id
    # TODO: replace with real venue data from the venues table, using venue_id

    return render_template('pages/show_venue.html',
                           venue=venue)


#  Create Venue
#  ----------------------------------------------------------------


@ app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@ app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    error = False
    try:
        form = VenueForm(request.form)
        venue = Venue(
            name=form.name.data,
            city=form.city.data,
            state=form.state.data,
            address=form.address.data,
            phone=form.phone.data,
            genres=form.genres.data,
            facebook_link=form.facebook_link.data,
            image_link=form.image_link.data
        )
        db.session.add(venue)
        db.session.commit()
        flash('Venue: {0} created successfully'.format(venue.name))
    except Exception as error:
        flash('An error occurred creating the Venue: {0}. Error: {1}'.format(
            venue.name, error))
        db.session.rollback()
    finally:
        db.session.close()
    if error:
        flash('An error occurred. Venue ' +
              request.form['name'] + ' could not be listed.')
        abort(500)
    else:
        # flash('Venue ' + request.form['name'] + ' was successfully listed!')
        return render_template('pages/home.html')

#      # on successful db insert, flash success

#         # TODO: on unsuccessful db insert, flash an error instead.
#         # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/


@ app.route('/venues/<venue_id>/delete', methods=['DELETE'])
def delete_venue(venue_id):
    venue = Venue.query.get(venue_id)
    error = False
    try:
        db.session.delete(venue)
        db.session.commit()
        flash('Venue ' + Venue.name + 'has been deleted')
    except:
        db.session.rollback()
    finally:
        db.session.close()
    if error:
        flash('Error! Venue ' + request.form['name'] + 'has not been deleted')
        abort(500)
    else:
        return render_template('pages/home.html')

    # TODO: Complete this endpoint for taking a venue_id, and using
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage

#  Artists
#  ----------------------------------------------------------------


@ app.route('/artists')
def artists():
    # TODO: replace with real venues data.
    #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
    data = []
    artists = Artist.query.all()
    for thisartist in artists:
        area = {
            'id': thisartist.id,
            'name': thisartist.name
        }
        data.append(area)

    return render_template('pages/artists.html', artists=data)


@ app.route('/artists/search', methods=['POST'])
def search_artists():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".

    search_term = request.form.get('search_term', '')
    search_results = Artist.query.filter(
        Artist.name.ilike(f'%{search_term}%')).all()
    response = {
        'count': len(search_results),
        'data': []
    }
    for artist in search_results:
        response['data'].append({
            'id': artist.id,
            'name': artist.name
        })

    return render_template('pages/search_artists.html', results=response, search_term=search_term)


@ app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    # shows the artist page with the given artist_id
    # TODO: replace with real artist data from the artist table, using artist_id

    artist = Artist.query.get(artist_id)

    current_time = datetime.now()

    upcoming_shows = db.session.query(Shows).join(Artist).filter(
        Shows.artist_id == artist_id).filter
    (Shows.start_time > datetime.now()).all()

    for show in upcoming_shows:
        if show.start_time > datetime.now():
            upcoming_shows.append({
                'venue_id': show.venue_id,
                'venue_name': Venue.query.filter_by(id=show.venue_id).first().name,
                'venue_image_link': Artist.query.filter_by(id=show.venue_id).first().image_link,
                'start_time': format_datetime(str(show.start_time))
            })
        return upcoming_shows

    past_shows = db.session.query(Shows).join(Artist).filter(
        Shows.artist_id == artist_id).filter
    (Shows.start_time > datetime.now()).all()

    for show in past_shows:
        if show.start_time < datetime.now():
            past_shows.append({
                'venue_id': show.venue_id,
                'venue_name': Venue.query.filter_by(id=show.venue_id).first().name,
                'venue_image_link': Artist.query.filter_by(id=show.venue_id).first().image_link,
                'start_time': format_datetime(str(show.start_time))
            })
        return past_shows

    data = Artist.query.get(artist_id)
    return render_template('pages/show_artist.html', artist=data)


#  Update
#  ----------------------------------------------------------------


@ app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()
    artist = {
        "id": 4,
        "name": "Guns N Petals",
        "genres": ["Rock n Roll"],
        "city": "San Francisco",
        "state": "CA",
        "phone": "326-123-5000",
        "website": "https://www.gunsnpetalsband.com",
        "facebook_link": "https://www.facebook.com/GunsNPetals",
        "seeking_venue": True,
        "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
        "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
    }
    # TODO: populate form with fields from artist with ID <artist_id>
    return render_template('forms/edit_artist.html', form=form, artist=artist)


@ app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    # TODO: take values from the form submitted, and update existing
    # artist record with ID <artist_id> using the new attributes

    return redirect(url_for('show_artist', artist_id=artist_id))


@ app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()
    venue = {
        "id": 1,
        "name": "The Musical Hop",
        "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
        "address": "1015 Folsom Street",
        "city": "San Francisco",
        "state": "CA",
        "phone": "123-123-1234",
        "website": "https://www.themusicalhop.com",
        "facebook_link": "https://www.facebook.com/TheMusicalHop",
        "seeking_talent": True,
        "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
        "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
    }
    # TODO: populate form with values from venue with ID <venue_id>
    return render_template('forms/edit_venue.html', form=form, venue=venue)


@ app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    # TODO: take values from the form submitted, and update existing
    # venue record with ID <venue_id> using the new attributes
    return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------


@ app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@ app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    error = False
    try:
        artist = Artist(name=request.form['name'], genres=request.form['genres'], city=request.form['city'], state=request.form['state'], phone=request.form['phone'], image_link=request.form['image_link'],
                        website=request.form['website_link'], facebook_link=request.form['facebook_link'], seeking_venue=request.form['seeking_venue'], seeking_description=request.form['seeking_description'])
        db.session.add(artist)
        db.session.commit()
    except:
        db.session.rollback()
        error = True
    finally:
        db.session.close()
    if error:
        flash('An error occurred. Artist ' +
              request.form['name'] + ' could not be listed.')
        abort(500)
    else:
        flash('Artist ' + request.form['name'] + ' was successfully listed!')
        return render_template('pages/home.html')

    # on successful db insert, flash success

    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')


#  Shows
#  ----------------------------------------------------------------

@ app.route('/shows')
def shows():
    # displays list of shows at /shows
    # TODO: replace with real venues data.
    data = []  # YOU DELETED THE HARD CODED INFO FROM HERE
    return render_template('pages/shows.html', shows=data)


@ app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@ app.route('/shows/create', methods=['POST'])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing form
    # TODO: insert form data as a new Show record in the db, instead

    # on successful db insert, flash success
    flash('Show was successfully listed!')
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Show could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return render_template('pages/home.html')


@ app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@ app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

# ----------------------------------------------------------------------------#
# Launch.
# ----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()
