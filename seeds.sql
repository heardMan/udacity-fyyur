/*
* The following seeds file will set up a fresh database instance with dummy data
* Just copy and paste into your database client
*/

-- CREATE TABLE "Venue" (
--     id SERIAL PRIMARY KEY,
--     name VARCHAR,
--     city VARCHAR,
--     state VARCHAR,
--     address VARCHAR,
--     phone VARCHAR,
--     image_url VARCHAR,
--     facebook_url VARCHAR,
--     website VARCHAR,
--     seeking_talent BOOLEAN,
--     seeking_description VARCHAR,
-- );

INSERT INTO "Venue" (
    name,
    city,
    state,
    address,
    phone,
    image_url,
    facebook_url,
    website,
    seeking_talent,
    seeking_description
    )

VALUES (
    'The Musical Hop',
    'San Francisco',
    'CA',
    '1015 Folsom Street',
    '123-123-1234',
    'https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60',
    'https://www.facebook.com/TheMusicalHop',
    'https://www.themusicalhop.com',
    TRUE,
    'We are on the lookout for a local artist to play every two weeks. Please call us.'
    );

INSERT INTO "Venue" (
    name,
    city,
    state,
    address,
    phone,
    image_url,
    facebook_url,
    website,
    seeking_talent,
    seeking_description
    )

VALUES (
    'The Dueling Pianos Bar',
    'New York',
    'NY',
    '335 Delancey Street',
    '914-003-1132',
    'https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80',
    'https://www.facebook.com/theduelingpianos',
    'https://www.theduelingpianos.com',
    FALSE,
    'n/a'
    );

INSERT INTO "Venue" (
    name,
    city,
    state,
    address,
    phone,
    image_url,
    facebook_url,
    website,
    seeking_talent,
    seeking_description
    )

VALUES (
    'Park Square Live Music & Coffee',
    'San Francisco',
    'CA',
    '34 Whiskey Moore Ave',
    '415-000-1234',
    'https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80',
    'https://www.facebook.com/ParkSquareLiveMusicAndCoffee',
    'https://www.parksquarelivemusicandcoffee.com',
    FALSE,
    'n/a'
    );

-- CREATE TABLE "Artist" (
--     id SERIAL PRIMARY KEY,
--     name VARCHAR,
--     city VARCHAR,
--     state VARCHAR,
--     phone VARCHAR,
--     image_url VARCHAR,
--     facebook_url VARCHAR,
--     website VARCHAR,
--     seeking_venue BOOLEAN,
--     seeking_description VARCHAR
-- );

INSERT INTO "Artist" (
    name,
    city,
    state,
    phone,
    image_url,
    facebook_url,
    website,
    seeking_venue,
    seeking_description
    )
VALUES (
    'Guns N Petals',
    'San Francisco',
    'CA',
    '326-123-5000',
    'https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80',
    'https://www.facebook.com/GunsNPetals',
    'https://www.gunsnpetalsband.com',
    TRUE,
    'Looking for shows to perform at in the San Francisco Bay Area!'
);

INSERT INTO "Artist" (
    name,
    city,
    state,
    phone,
    image_url,
    facebook_url,
    website,
    seeking_venue,
    seeking_description
    )
VALUES (
    'Matt Quevedo',
    'New York',
    'NY',
    '300-400-5000',
    'https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80',
    'https://www.facebook.com/mattquevedo923251523',
    'n/a',
    FALSE,
    'n/a'
);

INSERT INTO "Artist" (
    name,
    city,
    state,
    phone,
    image_url,
    facebook_url,
    website,
    seeking_venue,
    seeking_description
    )
VALUES (
    'The Wild Sax Band',
    'San Francisco',
    'CA',
    '432-325-5432',
    'https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80',
    'n/a',
    'n/a',
    FALSE,
    'n/a'

);

-- CREATE TABLE "Show" (
--     id SERIAL PRIMARY KEY,
--     artist_id INT REFERENCES artists(id), 
--     venue_id INT REFERENCES venues(id),
--     start_time TIMESTAMP
-- );

INSERT INTO "Show" ( artist_id, venue_id, start_time ) 
VALUES ( 1, 1, '2019-05-21T21:30:00.000Z' );

INSERT INTO "Show" ( artist_id, venue_id, start_time ) 
VALUES ( 2, 3, '2019-06-15T23:00:00.000Z');

INSERT INTO "Show" ( artist_id, venue_id, start_time ) 
VALUES ( 3, 3, '2035-04-01T20:00:00.000Z');

INSERT INTO "Show" ( artist_id, venue_id, start_time ) 
VALUES ( 3, 3, '2035-04-08T20:00:00.000Z');

INSERT INTO "Show" ( artist_id, venue_id, start_time ) 
VALUES ( 3, 3, '2035-04-15T20:00:00.000Z');

-- CREATE TABLE "Artist_Genre" (
--     id SERIAL PRIMARY KEY,
--     artist_id INT REFERENCES artists(id), 
--     genre VARCHAR
-- );

INSERT INTO "Artist_Genre" (artist_id, genre)
VALUES(1, 'Rock n Roll');

INSERT INTO "Artist_Genre" (artist_id, genre)
VALUES(2, 'Jazz');

INSERT INTO "Artist_Genre" (artist_id, genre)
VALUES(3, 'Jazz');

INSERT INTO "Artist_Genre" (artist_id, genre)
VALUES(3, 'Classical');

-- CREATE TABLE "Venue_Genre" (
--     id SERIAL PRIMARY KEY,
--     venue_id INT REFERENCES venues(id), 
--     genre VARCHAR
-- );

INSERT INTO "Venue_Genre" (venue_id, genre)
VALUES(1, 'Jazz');

INSERT INTO "Venue_Genre" (venue_id, genre)
VALUES(1, 'Reggae');

INSERT INTO "Venue_Genre" (venue_id, genre)
VALUES(1, 'Swing');

INSERT INTO "Venue_Genre" (venue_id, genre)
VALUES(1, 'Classical');

INSERT INTO "Venue_Genre" (venue_id, genre)
VALUES(1, 'Folk');

INSERT INTO "Venue_Genre" (venue_id, genre)
VALUES(2, 'Classical');

INSERT INTO "Venue_Genre" (venue_id, genre)
VALUES(2, 'R&B');

INSERT INTO "Venue_Genre" (venue_id, genre)
VALUES(2, 'Hip-Hop');

INSERT INTO "Venue_Genre" (venue_id, genre)
VALUES(3, 'Rock n Roll');

INSERT INTO "Venue_Genre" (venue_id, genre)
VALUES(3, 'Jazz');

INSERT INTO "Venue_Genre" (venue_id, genre)
VALUES(3, 'Classical');

INSERT INTO "Venue_Genre" (venue_id, genre)
VALUES(3, 'Folk');
