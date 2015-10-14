Installation instructions

THIS DOCUMENT IS CURRENTLY OUT OF DATE.  FOR USABLE INSTRUCTIONS REFER TO DeployUsingModPython guide.
# Introduction #

TurboCare is based on the Python web framework called TurboGears.  It uses MySQL for the back-end database.  Up until now, I've been working on Ubuntu, so I'll be using that distribution as the starting point for explaining on how to install the program and get it running.

TurboCare uses the the database schema from the Care2x project (www.care2x.org) hence the name "TurboCare".

# Ubuntu packages #

1. Python 2.4 (python2.4) and the development package (python2.4-dev)

2. SQLite version 3 (sqlite2)

3. Python ReportLab

4. Python Imaging Library (PIL)

5. Python MySQL library

6. MySQL version 5.0 (5.0.24 tested)

> - I also recommend getting the administrative packages.


7. Also, make sure that gcc libstdc++6-dev and other needed packages listed in the TurboGears documentation are installed.


# TurboGears #

TurboGears has good documentation on how to install it on a system.  After installing the above Python packages, it should be really simple.  There are only two steps to follow on the following page:

http://www.turbogears.org/download/

after which, you should be ready to use TurboGears.

# Database creation #

The database schema is the Care2x (www.care2x.org) database schema.  When examining Care2x for our project, I had a real hard time working with the PHP, but the schema seemed very well structured.  So I based my project on the schema of the Care2x project, and I've been trying to keep it somewhat compatible.

In addition to the care2x tables, I've added a number of inventory management tables.  These tables aren't really described anywhere at this point.

1. On Ubuntu, MySQL installs with a password-less root user.  You can change this (http://www.mysql.org/doc/refman/5.0/en/set-password.html).  Also, if you prefer not using the care2x schema with the root user, you can create a new user with administrative privileges to the database, and use this user instead of root.


2. After adjusting the user account settings, you'll need to create the care2x database schema (http://www.mysql.org/doc/refman/5.0/en/create-database.html).  For example: CREATE DATABASE care2x;

3. In the base directory I have a small database schema utility which I wrote for helping manage the MySQL schema (minor updates), so this can be used to help create the schema.  This python program is called 'mysql\_schema.py'.  In the same folder I have a python pickle file which contains the care2x and inventory tables.  The file is called "care2x\_schema.data".  To execute the program to create the schema (assuming you've called your database "care2x" and your password is abc123 and you're running the command where the files are located):

python mysql\_schema.py -d care2x -u root -p abc123 -o schema\_updt -f care2x\_schema.data

There is a sample-dev.cfg file in the main folder of the project.  Rename it to dev.cfg and modify the variables inside that to match your environment (database login, etc...).

# controllers.py #

My version of the program already has a number of database entries, and some of these entries are currently hard-coded into the program.  You'll need to disable these lines (by commenting them out) to proceed.  Lines such as:
> pharmacy\_main = controllers\_dispensing.Dispensing(2)

> pharmacy\_main = identity.SecureObject(pharmacy\_main, identity.has\_permission('pharmacy\_main\_view'))

or

> warehouse\_store = controllers\_store.Store(1, "warehouse\_store")

> warehouse\_store = identity.SecureObject(warehouse\_store,identity.has\_permission('warehouse\_store\_view'))

That is, anything using the controllers\_store or controllers\_dispensing modules.  In the future (who knows how far into it) I will add code to dynamically create these links.  Ahh... the future.


# Adding users with permissions #

I still use the same table for care2x users with TurboCare.  That is, the user name and password should be preserved.  The permissions on the other hand, are handled separately (using the TurboGears default system).

The users are stored in the "care\_users" table.

If you log into the care2x as an administrator through mysql, then you should be able to use a command such as:

INSERT INTO care\_users (name, login\_id, password) VALUES ('New Name', 'myid', PASSWORD('abc123'));

Then a user with name: New Name and a login id of 'myid' is created with an encrypted password of 'abc123'.

The file "base\_care2x\_permission.sql" contains the tables and permissions which you can use as an example.  The permissions have already been coded through much of the program already, so at least the permissions table should be used as is (until you change the permissions in the program code).


Shortcuts for Ubuntu

sudo apt-get install python-pysqlite2 python-mysqldb python-imaging  gcc libc6-dev python-dev python-setuptools build-essential mysql-server python-reportlab mysql-admin subversion

sudo easy\_install -Z TurboGears
sudo easy\_install -Z sqlobject

cd ~/

svn checkout http://turbocare.googlecode.com/svn/trunk/ turbocare

mysql -u root
> ->create database care2x;
ctrl-D

cd ~/turbocare
python mysql\_schema.py -d care2x -u root -o schema\_updt -f turbocare\_schema.data
python mysql\_schema.py -d care2x -u root -o restore -f turbocare\_backup.data
cp dev-sample.cfg dev.cfg
python start-turbocare.py
If this loads without errors you have installed turbocare.  Start working using 127.0.0.1:8080.

sudo apt-get install libapache-mod-python2.4 apache2