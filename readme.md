# Tournament - a Udacity Nano-Degree Project for Full Stack Foundations
March 2015 by Gary Davis

Tournament is small python backend that implements an SQL database using postgresql to store players and determine the winner for a Swiss-Style tournament.

Requirements:
* Python
* postgresql
* psql 9.3.6

For the class, we installed a virtual machine using VirtualBox and Vagrant and pulled the necessary setup from GIT

Installation (on a Mac OS)
* Open Terminal on the Mac (it is found in the utilities folder or use Spotlight to search for it)
* Change the directory from home to the vagrant directory installed on the Mac.  This can be done with:
```
> cd /fullstack/vagrant  
```
* Fire up the virtual machine:  
> vagrant up  
* SSH into the virtual machine, again form the Mac Terminal program:  
> vagrant SSH  
  You should now see the command line of the virtual machine


Running the program

* The command line of the virtual machine (see above) we will set up the SQL database by opening PSQL and running the database model:  
> psql  
* From within psql:  
> \i tournament.sql

	From here you will have database with a few players and matches already added for testing purposes.  
