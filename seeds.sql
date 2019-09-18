/*
* The following seeds file will set up a fresh database instance with dummy data
* Just copy and paste into your database client
*/

DROP DATABASE IF EXISTS fyyur;

CREATE DATABASE fyyur;

CREATE TABLE venues (
    venue_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    venue_name VARCHAR,
    venue_city VARCHAR,
    venue_state VARCHAR,
    venue_address VARCHAR,
    venue_phone VARCHAR,
    image_link VARCHAR,
    facebook_url VARCHAR


);

INSERT INTO venues (venue_name, venue_city, venue_address, venue_phone, image_link, facebook_url)
VALUES (
    'The Musical Hop',
    'San Francisco',
    '1015 Folsom Street',
    '123-123-1234',
    'https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60',
    'https://www.facebook.com/TheMusicalHop');

INSERT INTO venues (venue_name, venue_city, venue_address, venue_phone, image_link, facebook_url)
VALUES (
    'The Dueling Pianos Bar',
    'New York',
    '335 Delancey Street',
    '914-003-1132',
    'https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80',
    'https://www.facebook.com/theduelingpianos'
    );

INSERT INTO venues (venue_name, venue_city, venue_address, venue_phone, image_link, facebook_url)
VALUES (
    'Park Square Live Music & Coffee',
    'San Francisco',
    '34 Whiskey Moore Ave',
    '415-000-1234',
    'https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80',
    'https://www.facebook.com/ParkSquareLiveMusicAndCoffee');

-- INSERT INTO venues (venue_name, venue_city, venue_address, venue_phone, image_link, facebook_url)
-- VALUES (
--     '',
--     '',
--     '',
--     '',
--     '',
--     '');

CREATE TABLE artists (
    artist_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    artist_name VARCHAR,
    artist_hometown VARCHAR,
    artist_phone VARCHAR,
    genres VARCHAR,
    image_link VARCHAR,
    facebook_link VARCHAR
);

INSERT INTO artists (artist_name, artist_hometown, artist_phone, genres, image_link, facebook_url)
VALUES (
    'Guns N Petals',
    'San Francisco',
    '326-123-5000',
    ['Rock n Roll'],
    'https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80',
    'https://www.facebook.com/GunsNPetals'
);

INSERT INTO artists (artist_name, artist_hometown, artist_phone, genres, image_link, facebook_url)
VALUES (
    'Matt Quevedo',
    'New York',
    '300-400-5000',
    ['Jazz'],
    'https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80',
    'https://www.facebook.com/mattquevedo923251523'
);

INSERT INTO artists (artist_name, artist_hometown, artist_phone, genres, image_link, facebook_url)
VALUES (
    'The Wild Sax Band',
    'San Francisco',
    '432-325-5432',
    ['Jazz', 'Classical'],
    'https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80',
    '#'
);

-- INSERT INTO artists (artist_name, artist_hometown, artist_phone, genres, image_link, facebook_url)
-- VALUES (
--     '',
--     '',
--     '',
--     '',
--     '',
--     ''
-- );