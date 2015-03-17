-- Table definitions for the tournament project.
--

-- Initialize a new database by first making sure we are not connected to existing database of the same
-- name and dropping it if it exits

\c vagrant

drop database if exists tournament;

create database tournament;

-- Connect to the database and create the initial tables

\c tournament

create table players(
	P_Id serial PRIMARY KEY,
	player_name varchar(50));

create table matches(
	M_Id serial PRIMARY KEY,
	P1 integer references players(P_Id),
	P2 integer references players(P_Id),
	winner integer references players(P_Id));

-- Create a view of match history for every player listing opponent
-- and win as 1, zero as loss

create view long_match_list as
	SELECT
		M_Id,
		P1 as player,
		P2 as opponent,
		(case when winner=P1 then 1 else 0 end) as wins
	FROM
		matches
	UNION
	SELECT
		M_Id,
		P2 as player,
		P1 as opponent,
		(case when winner=P2 then 1 else 0 end) as wins
	FROM
		matches
	ORDER BY
		M_Id;

-- Populate the players table with some dummy players

INSERT INTO players(player_name) VALUES ('Henry the VIII');
INSERT INTO players(player_name) VALUES ('Catherine the Great');
INSERT INTO players(player_name) VALUES ('Richard the Lion Hearted');
INSERT INTO players(player_name) VALUES ('Louis the XIV');
INSERT INTO players(player_name) VALUES ('Julius Ceasar');
INSERT INTO players(player_name) VALUES ('Aristotle');
INSERT INTO players(player_name) VALUES ('Odd Man Out');

-- Populate some matches

INSERT INTO matches(P1, P2, winner) VALUES (1, 2,1);
INSERT INTO matches(P1, P2, winner) VALUES (3,4,3);
INSERT INTO matches(P1, P2, winner) VALUES (5,6,5);
INSERT INTO matches(P1, P2, winner) VALUES (1, 3,1);
INSERT INTO matches(P1, P2, winner) VALUES (5,2,5);
INSERT INTO matches(P1, P2, winner) VALUES (4,6,4);


	


