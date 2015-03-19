# Tournament v1.2- a Udacity Nano-Degree Project for Full Stack Foundations
###v1.2 adds: Distingquish ties in standings
March 2015 by Gary Davis

Tournament is small python backend that implements an SQL database using postgresql to store players and determine the winner for a Swiss-Style tournament (see: http://en.wikipedia.org/wiki/Swiss-system_tournament).  Methods/functions are provided that can clear the database, add players, record matches, display results and show matchings for the next round.  If there are an odd number of players, a bye will be included in the players matchings.  Matches can be won or tied.  Points are awarded to players as win:1, loss: -1, tie: 0. Standings are based on 
total points for each player and in the case of a tie, the sum of the total points for each of their opponents, or Opponent Match Points ("OMP")

###Requirements:
* Python
* postgresql
* psql 9.3.6

For the Udacity Nano-Degree class, we installed a virtual machine using VirtualBox and Vagrant and pulled the necessary setup from GIT (see: https://www.udacity.com/wiki/ud197/install-vagrant)

###Files:
* tournament.sql - the postresql model of the database
* tournament.py - the program containing the methods or functions that can be called from python
* tournament_test.py - the unit-test file provided by Udacity

###Installation (on a Mac OS)
* Open Terminal on the Mac (it is found in the utilities folder or use Spotlight to search for it)
* Change the directory from home to the vagrant directory installed on the Mac.  This can be done with:
```ShellSession
> cd [path to get to:]fullstack/vagrant  
```
* Fire up the virtual machine: 
```ShellSession 
> vagrant up
```  
* SSH into the virtual machine, again form the Mac Terminal program: 
```ShellSession 
> vagrant SSH  
```
  You should now see the command line of the virtual machine


###Running the program

* From the command line of the virtual machine, change directory to that of the tournament files:
```ShellSession
> cd /vagrant/tournament
```
* From the command line of the virtual machine (see above) we will set up the SQL database by opening PSQL
and running the database model.  This only needs to be done once. NOTE however that it will delete all existing 
data in a database called 'tournament'. 
```ShellSession
> psql  
```
* From within psql:
``` 
> .\i tournament.sql
```
To exit PSQL:
```
> \q
```
The test routines were provided by Udacity and can be run from the vagrant terminal prompt. Be sure
that you are in the directory /vagrant/tournament per the direction at the start of this section:
```ShellSession
> ./tournament_test.py
```
or:
```ShellSession
> python tournament_test.py
```
####Methods (i.e. Functions) included in tournament.py:
* deleteMatches() - delete all matches from the database
* deletePlayers() - delete all players from teh database
* countPlayers() - provides a count of the players
* registerPlayer(name) - register a players name
* playerStandings() - lists the current standing of the players including player ids, points, number 
						of matches played and the sum of the points of their opponents
* reportMatch(player1, player2, point1, points2) - report match results using player ids and points for each
				player as win: 1, loss: -1 and tie: 0. 
* swissPairings() - provides the pairs for the next round of matches

To use the functions from python, run the python interpreter (or iPython) and import the necessary modules:
```ShellSession
> python
>>> import psycopg2
>>> from tournament import *
```
The methods/functions can then be called individually e.g.:
```python
>>> playerStandings()
[(1, 'Henry the VIII', 2L, 2L, Decimal('-2')), (5, 'Julius Ceasar', 1L, 2L, Decimal('-2')), (3, 'Richard the Lion Hearted', 0L, 2L, Decimal('1')), (6, 'Aristotle', 0L, 2L, Decimal('0')), (4, 'Louis the XIV', -1L, 2L, Decimal('0')), (2, 'Catherine the Great', -2L, 2L, Decimal('3'))]

```
The first number in each tuple is the player id follwed by play name, points, number of matches played and the sum of the points of their opponents which is used to decide on ties in the rankings.  The 'L' after the numbers shows the formatting used for the number (i.e. long).  The Decimal('1') format for opponent points snuck in there and I have no idea why but it works for sorting.

A description of each of the functions can be obtain from the python interpreter by entering "print function_name.__doc__":
```python
>>> print playerstandings.__doc__
```



