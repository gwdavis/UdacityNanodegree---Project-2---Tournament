-- Tournament v1.1
-- Table definitions for the tournament project.
-- Fork - allow tied games
-- a Udacity Nano-Degree Project for Full Stack Foundations
-- March 2015 by Gary Davis

-- Initialize a new database by first making sure we are not connected 
-- to existing database of the same name and dropping it if it exits

\c vagrant

drop database if exists tournament;

create database tournament;

-- Connect to the database and create the initial tables
-- for players and their matches.

-- Matches table handles tied matches by including results of the game for each player
-- indicated as win 1, loss -1 and tie 0 for each player for each match played

\c tournament

create table players(
	P_Id serial PRIMARY KEY,
	player_name varchar(50));


create table matches(
	M_Id serial PRIMARY KEY,
	P1 integer references players(P_Id),
	P2 integer references players(P_Id),
	P1_result integer,
	P2_result integer);

-- Create a view of match history for every player listing their opponent
-- and win as 1, zero as loss.  So for each match there will be two listings
-- in this view

create view matches_by_player as
	SELECT
		M_Id,
		P1 as player,
		P2 as opponent,
		P1_result as points
	FROM
		matches
	UNION
	SELECT
		M_Id,
		P2 as player,
		P1 as opponent,
		P2_result as points
	FROM
		matches
	ORDER BY
		M_Id;

-- Populate the players table with some dummy players
-- These can be delete with the provided methods/functions
-- or deleted or commented out for production use.

INSERT INTO players(player_name) VALUES ('Henry the VIII');
INSERT INTO players(player_name) VALUES ('Catherine the Great');
INSERT INTO players(player_name) VALUES ('Richard the Lion Hearted');
INSERT INTO players(player_name) VALUES ('Louis the XIV');
INSERT INTO players(player_name) VALUES ('Julius Ceasar');
INSERT INTO players(player_name) VALUES ('Aristotle');
INSERT INTO players(player_name) VALUES ('Odd Man Out');

-- Populate the matches table with some dummy matches

INSERT INTO matches(P1, P2, P1_result, P2_result) VALUES (1, 2,1,-1);
INSERT INTO matches(P1, P2, P1_result, P2_result) VALUES (3,4,1,-1);
INSERT INTO matches(P1, P2, P1_result, P2_result) VALUES (5,6,0,0);
INSERT INTO matches(P1, P2, P1_result, P2_result) VALUES (1, 3,1,-1);
INSERT INTO matches(P1, P2, P1_result, P2_result) VALUES (5,2,1,-1);
INSERT INTO matches(P1, P2, P1_result, P2_result) VALUES (4,6,0,0);


	


