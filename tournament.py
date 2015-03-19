#!/usr/bin/env python
#
# tournament.py v1.2 -- implementation of a Swiss-system tournament
# distinguish player ties
# a Udacity Nano-Degree Project for Full Stack Foundations
# March 2015 by Gary Davis
#

import psycopg2

def connect():
    """Connect to the PostgreSQL database for tournament.py.
    Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    c = conn.cursor()
    # Delete all rows
    c.execute("DELETE from matches")
    conn.commit()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    c = conn.cursor()
    # Delete all rows
    c.execute("DELETE from players")
    conn.commit()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    c = conn.cursor()
    # Count the players
    c.execute("SELECT count(*) from players;")
    count = c.fetchone()
    conn.close()
    # return the count which is the first entry in the tuple
    return count[0]


def registerPlayer(name):
    """Adds a player to the tournament database with a unique serial id

    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    c = conn.cursor()
    # Unique ID is added automatically as a serial variable
    # Insert parameter into database
    c.execute("INSERT INTO players(player_name) VALUES(%s)", (name,))
    conn.commit()
    conn.close()


def playerStandings():
    """Returns a list of the players and their points records, number of
    matches played, and the sum of thier opponent's points
    (Opponent Match Points or OMP)in order to settle tied results.
    The list is sorted by total points and OMP.

    Returns:
      A list of tuples, each of which contains (id, name, points, matches, OMP):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        points: the sum of wins, losses and ties for the player
        matches: the number of matches the player has played
        OMP: Opponent Match Points is the sum of the points earned in all
            reported matches in order to decide ties.
        """

    conn = connect()
    c = conn.cursor()
    c.execute(
        """SELECT
                p.id,
                p.name,
                p.points,
                p.matches,
                o.OMP
            FROM playerPoints p
            LEFT JOIN cumPoints o
            ON p.id = o.id
            ORDER BY p.points desc, o.OMP desc
            """)
    result = c.fetchall()
    # BUG_ALERT - the OMP output type in result is Decimal('n') where n is
    # the number of points.  It sorts correctly but is odd.
    conn.close
    return result


def reportMatch(player1, player2, player1Result, player2Result):
    """Records the outcome of a single match between two players.

    Args:
      player1:  the id number of a player
      player2:  the id number of a player
      player1Result: either a 1,-1 or 0
      player2Result: either a 1,-1 or 0
    """

    # Check to make sure a win, loss or tie was entered correctly
    # by checking that the sum of the two results is zero
    if player1Result + player2Result != 0:
        raise ValueError("""Oops!  sum of results did not equal zero, enter
              1, -1 or 0...""")
    else:

        conn = connect()
        c = conn.cursor()
        # Insert a new record into the Matches table using
        # the player id for each player, a 1 for a win, -1 for a loss
        # and 0 for a tie.
        c.execute(
            """INSERT INTO matches(P1,P2,P1_result,P2_result)
            VALUES(%s, %s, %s, %s)""",
            (player1, player2, player1Result, player2Result))
        conn.commit()
        conn.close()

# Following can be used to test reportMatch()
# deleteMatches()
# reportMatch(1, 2, 1, -1)
# reportMatch(3, 4, 1, -1)
# reportMatch(5, 6, 0, 0)
# reportMatch(1, 3, 1, -1)
# reportMatch(5, 2, 1, -1)
# reportMatch(4, 6, 0, 0)
# print playerStandings()


def previousMatch(player1, opponent1):
    """Determines if two players have previously played a match

    Args:   player id
            opponent id

    Returns TRUE or FALSE"""

    conn = connect()
    c = conn.cursor()
    # Simply count the number of matches between players using the
    # matches_by_player_view that lists all matches for each player in the 
    # first column (i.e. there will be two entries for each match in
    # in the matches_by_player)
    c.execute(
        """SELECT count(case when opponent = %s then 1 end)
        from matches_by_player
        where player = %s""", (opponent1, player1))
    result = c.fetchone()
    conn.close()
    if result[0] > 0:
        return True
    return False


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1:    the first player's unique id
        name1:  the first player's name
        id2:    the second player's unique id
        name2:  the second player's name
    """
    # Count the number of participants and add a partipant: "Bye"
    # At this point in the development of the application the organizer
    # will need to manually enter the results of the Bye match.

    if countPlayers() % 2 != 0:
        # If Bye is already registered, delete player bye
        conn = connect()
        c = conn.cursor()
        c.execute("SELECT count(P_Id) FROM players where player_name = 'Bye'")
        byeExists = c.fetchone()[0]

        # If There are odd players add "Bye"
        if byeExists > 0:
            c.execute("DELETE FROM players where player_name = 'Bye'")
            conn.commit()
            conn.close()

        else:
            registerPlayer("Bye")

    # Retrieve the standings from the database and initialize a variable
    standings = playerStandings()
    pairings = []

    # Go through standings list to finding pairings and reducing the size
    # of the list until all pairings are found.
    while True:
        for i in range(1, len(standings)):
            # remove the players from the standings list using pop and
            # record the player Ids and name which are the first two
            # entries in the tuples

            if previousMatch(standings[0][0], standings[i][0]) is False:
                pairings.append((standings[i][0], standings.pop(i)[1],
                                 standings[0][0], standings.pop(0)[1]))
                break
            else:
                continue
        # If the standings list is empty then return
        if len(standings) <= 0:
            break
    return pairings


def dummyDatabase():
    """Populates the tables with some dummy players and matches
    These can be delete with the provided methods/functions"""

    conn = connect()
    c = conn.cursor()
    c.execute("""
        -- Populates the players table with some dummy players

        INSERT INTO players(player_name) VALUES ('Henry the VIII');
        INSERT INTO players(player_name) VALUES ('Catherine the Great');
        INSERT INTO players(player_name) VALUES ('Richard the Lion Hearted');
        INSERT INTO players(player_name) VALUES ('Louis the XIV');
        INSERT INTO players(player_name) VALUES ('Julius Ceasar');
        INSERT INTO players(player_name) VALUES ('Aristotle');

        -- Populate the matches table with some dummy matches

        INSERT INTO matches(P1, P2, P1_result, P2_result) VALUES (1, 2,1,-1);
        INSERT INTO matches(P1, P2, P1_result, P2_result) VALUES (3,4,1,-1);
        INSERT INTO matches(P1, P2, P1_result, P2_result) VALUES (5,6,0,0);
        INSERT INTO matches(P1, P2, P1_result, P2_result) VALUES (1, 3,1,-1);
        INSERT INTO matches(P1, P2, P1_result, P2_result) VALUES (5,2,1,-1);
        INSERT INTO matches(P1, P2, P1_result, P2_result) VALUES (4,6,0,0);
        """)
    conn.commit()
    conn.close()


""" EXTRA CREDIT COMMENTS:
    =====================
To Handle Odd Players -     Done above but does not automatically enter a
    result for the bye match.  This must be entered manually as with all
    other results.
To Handle Ties -            Done
To Handle Ties in Ranking - Done
To Handle Multiple Tournaments (preliminary thoughts) - 
                            Not done
    - New Table - Tournaments
    - Add Tournaments method
    - Add registered Player to a tournament method
    - Add Delete player method removes a player from a tournament
    - Add Match results will add the tournament identifyier
    - Add tournament parameter to all applicable methods.  Alternatively
      consider creating an "active tournament" value in the tournament table
      so that only one tournament can be active.  Another alternative is 
      to have an active tournament for the session as a global variable.
"""






""" NOTA BENE
Following functions were used to develop ideas but are not used by the 
application"""


def playerStandings_old():
    """Returns a list of the players and their points records and number of
    matches played, sorted by total points.

    Returns:
      A list of tuples, each of which contains (id, name, points, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        points: the sum of wins, losses and ties for the player
        matches: the number of matches the player has played
    """
    conn = connect()
    c = conn.cursor()
    # Join the players table and a view of the matches table.
    # The view of the matches table (matches_by_player) lists each player
    # in column one and his opponent and results (i.e. there will be two
    # enteries for each match).  Select the id, name and a sum of the
    # points for each player.
    # Sort by the wins .
    c.execute(
        # Summing the points column gives the total number of points
        # Sounting the points column gives the total number of matches
        # players table provides the name
        # long_match_view table provides the points column as a 1, -1 or 0
        """SELECT
            P_Id as id,
            player_name as name,
            COALESCE(SUM(points), 0) as points,
            count(points) as matches
        FROM players
        LEFT JOIN matches_by_player ON P_Id = player
        GROUP BY P_Id
        ORDER BY points desc;""")
    result = c.fetchall()
    conn.close()
    return result


# Create a method that returns the number of points earned for
# a particular player and in this use case we will call him an
# opponent as we want to get the summ of opponets points.
def playerPoints(opponentID):
    """Sum the total points for a player and return an integer

    Args: opponent id"""

    conn = connect()
    c = conn.cursor()
    c.execute(
        """SELECT SUM(points)
        FROM matches_by_player
        WHERE player = %s""", (opponentID,))
    result = str(c.fetchone()[0])
    conn.close
    return result


# Create a method that returns a list of opponents
def opponentList(playerid):
    """Output a list of opponents, at the moment,
    this list is a list of tuples with one opponent ID
    in each tuple.

    Args: player ID"""

    conn = connect()
    c = conn.cursor()
    c.execute("""SELECT opponent
        FROM matches_by_player
        WHERE player = %s""", (playerid,))
    temp_result = c.fetchall()
    conn.close
    # convert list of single element tuples to a list
    # from  http://stackoverflow.com/a/716761/4671044
    result = [j for i in temp_result for j in i]
    return result


# Create a method that returns the points earned by opponents of
# a given player
def opponentPoints(playerid):
    """Output the sum of points earned by the opponents of a given player

    Args: player id"""
    conn = connect()
    c = conn.cursor()
    c.execute("""SELECT SUM(points)
        FROM matches_by_player
        WHERE player IN
            (SELECT opponent
            FROM matches_by_player as LML2
            WHERE LML2.player = %s)""", (playerid,))
    result = str(c.fetchone()[0])
    conn.close
    return result

