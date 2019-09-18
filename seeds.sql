/*
* The following seeds file will set up a fresh database instance with dummy data
* Just copy and paste into your database client
*/

DROP DATABASE IF EXISTS fyyur;

CREATE DATABASE fyyur;

CREATE TABLE venues (
    venue_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    venue_name VARCHAR,
    --genres VARCHAR,
    venue_city VARCHAR,
    venue_state VARCHAR,
    venue_address VARCHAR,
    venue_phone VARCHAR,
    image_link VARCHAR,
    facebook_url VARCHAR,
    website VARCHAR,
    seeking_talent BOOLEAN,
    seeking_description VARCHAR,
    --past_shows INT,
    --upcoming_shows INT,
    past_shows_count INT,
    upcoming_shows_count INT

);

INSERT INTO venues (
    venue_name,
    --genres,
    venue_city,
    venue_state,
    venue_address,
    venue_phone,
    image_link,
    facebook_url,
    website,
    seeking_talent,
    seeking_description,
    --past_shows,
    --upcoming_shows,
    past_shows_count,
    upcoming_shows_count
    )

VALUES (
    'The Musical Hop',
    --'genres',
    'San Francisco',
    'CA',
    '1015 Folsom Street',
    '123-123-1234',
    'https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60',
    'https://www.facebook.com/TheMusicalHop',
    'https://www.themusicalhop.com',
    TRUE,
    'We are on the lookout for a local artist to play every two weeks. Please call us.',
    --'past shows',
    --'upcoming shows',
    5,
    10
    );

INSERT INTO venues (
    venue_name,
    --genres,
    venue_city,
    venue_state,
    venue_address,
    venue_phone,
    image_link,
    facebook_url,
    website,
    seeking_talent,
    seeking_description,
    --past_shows,
    --upcoming_shows,
    past_shows_count,
    upcoming_shows_count
    )

VALUES (
    'The Dueling Pianos Bar',
    --'genres',
    'New York',
    'NY',
    '335 Delancey Street',
    '914-003-1132',
    'https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80',
    'https://www.facebook.com/theduelingpianos',
    'https://www.theduelingpianos.com',
    FALSE,
    NULL,
    'past shows',
    'upcoming shows',
    15,
    20
    );

INSERT INTO venues (
    venue_name,
    --genres,
    venue_city,
    venue_state,
    venue_address,
    venue_phone,
    image_link,
    facebook_url,
    website,
    seeking_talent,
    seeking_description,
    --past_shows,
    --upcoming_shows,
    past_shows_count,
    upcoming_shows_count
    )

VALUES (
    'Park Square Live Music & Coffee',
    --'genres',
    'San Francisco',
    'CA',
    '34 Whiskey Moore Ave',
    '415-000-1234',
    'https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80',
    'https://www.facebook.com/ParkSquareLiveMusicAndCoffee',
    'https://www.parksquarelivemusicandcoffee.com',
    FALSE,
    NULL,
    --'past shows',
    --'upcoming shows',
    25,
    30
    );

-- INSERT INTO venues (
--     venue_name,
--     --genres,
--     venue_city,
--     venue_state,
--     venue_address,
--     venue_phone,
--     image_link,
--     facebook_url,
--     website,
--     seeking_talent,
--     seeking_description,
--     --past_shows,
--     --upcoming_shows,
--     past_shows_count,
--     upcoming_shows_count
-- )
-- VALUES (
--     '',
--     '',
--     '',
--     '',
--     '',
--     '',
--     '',
--     '',
--     '',
--     '',
--     '',
--     '',
--     '',
--     '',
--     ''
--     );

CREATE TABLE artists (
    artist_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    artist_name VARCHAR,
    --genres VARCHAR,
    artist_city VARCHAR,
    artist_state VARCHAR,
    artist_phone VARCHAR,
    image_link VARCHAR,
    facebook_link VARCHAR,
    website VARCHAR,
    seeking_venue BOOLEAN TRUE,
    seeking_description VARCHAR,
    --past_shows INT,
    --upcoming_shows INT,
    past_shows_count INT,
    upcoming_shows_count INT
);

INSERT INTO artists (
    artist_name,
    --genres
    artist_city,
    artist_state,
    artist_phone,
    image_link,
    facebook_url,
    website,
    seeking_venue,
    seeking_description,
    --past_shows
    --upcoming_shows
    past_shows_count,
    upcoming_shows_count
    )
VALUES (
    'Guns N Petals',
    --['Rock n Roll'],
    'San Francisco',
    'CA',
    '326-123-5000',
    'https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80',
    'https://www.facebook.com/GunsNPetals',
    'https://www.gunsnpetalsband.com',
    TRUE,
    'Looking for shows to perform at in the San Francisco Bay Area!',
    --'past shows'
    --'upcoming shows',
    0,
    0
);

INSERT INTO artists (
    artist_name,
    --genres
    artist_city,
    artist_state,
    artist_phone,
    image_link,
    facebook_url,
    website,
    seeking_venue,
    seeking_description,
    --past_shows
    --upcoming_shows
    past_shows_count,
    upcoming_shows_count
)
VALUES (
    'Matt Quevedo',
    --['Jazz'],
    'New York',
    'NY',
    '300-400-5000',
    'https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80',
    'https://www.facebook.com/mattquevedo923251523',
    NULL,
    FALSE,
    NULL,
    --'past shows',
    --'upcoming shows',
    25,
    20
);

INSERT INTO artists (
    artist_name,
    --genres
    artist_city,
    artist_state,
    artist_phone,
    image_link,
    facebook_url,
    website,
    seeking_venue,
    seeking_description,
    --past_shows
    --upcoming_shows
    past_shows_count,
    upcoming_shows_count
)
VALUES (
    'The Wild Sax Band',
    --['Jazz', 'Classical'],
    'San Francisco',
    'CA',
    '432-325-5432',
    'https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80',
    NULL,
    NULL,
    FALSE,
    NULL,
    --'past shows',
    --'upcoming shows',
    15,
    10

);

-- INSERT INTO artists (
--     artist_name,
--     --genres
--     artist_city,
--     artist_state,
--     artist_phone,
--     image_link,
--     facebook_url,
--     website,
--     seeking_venue,
--     seeking_description,
--     --past_shows
--     --upcoming_shows
--     past_shows_count,
--     upcoming_shows_count
-- )
-- VALUES (
--     '',
--     '',
--     '',
--     '',
--     '',
--     '',
--     '',
--     '',
--     '',
--     '',
--     '',
--     '',
--     '',
--     ''
-- );