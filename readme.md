# Tournament - a Udacity Nano-Degree Project for Full Stack Foundations
March 2015 by Gary Davis

Tournament is small python backend that implements an SQL database using postgresql to store players and determine the winner for a Swiss-Style tournament (see: http://en.wikipedia.org/wiki/Swiss-system_tournament).

Requirements:
* Python
* postgresql
* psql 9.3.6

For the class, we installed a virtual machine using VirtualBox and Vagrant and pulled the necessary setup from GIT (see: https://www.udacity.com/wiki/ud197/install-vagrant)

Files:
* tournament.sql - the postresql model of the database
* tournament.py - the program containing the methods or functions that can be called from python
* tournament_test.py - the unit-test file provided by Udacity

Installation (on a Mac OS)
* Open Terminal on the Mac (it is found in the utilities folder or use Spotlight to search for it)
* Change the directory from home to the vagrant directory installed on the Mac.  This can be done with:
```
> cd [path to get to:]fullstack/vagrant  
```
* Fire up the virtual machine: 
``` 
> vagrant up
```  
* SSH into the virtual machine, again form the Mac Terminal program: 
``` 
> vagrant SSH  
```
  You should now see the command line of the virtual machine


Running the program

* From the command line of the virtual machine, change directory to that of the tournament files:
```
> cd /vagrant/tournament
```
* The command line of the virtual machine (see above) we will set up the SQL database by opening PSQL and running the database model:  
```
> psql  
```
* From within psql:
``` 
> .\i tournament.sql
```

From here you will have database with a few players and matches already added to the database for testing purposes. 
The test routines were provided by Udacity and can be run from the vagrant terminal prompt:
```
> ./tournament_test.py
```
or from within python:
```
> python tournament_test.py
```
Methods/Functions included in tournament.py:
*connect()
* deleteMatches() - delete all matches from the database
* deletePlayers() - delete all players from teh database
* countPlayers() - provides a count of the players
* registerPlayer(name) - register a players name
* playerStandings() - lists the current standing of the players including player ids
* reportMatch(winner, loser) - report match results using player ids
* swissPairings() - provides the pairs for the next round of matches

To use the functions from python, run the python interpreter and import the necessary modules:
```
> python
>>> import psycopg2
>>> from tournament import *
```
The methods/functions can be called individually e.g.:
```
>>> playerStandings()
```




