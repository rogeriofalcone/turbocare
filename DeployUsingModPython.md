## Introduction ##

This is a quick guide to installing turbocare using mod\_python on Ubuntu.  Using Apache to serve the static content makes things nice and fast.  This is very much designed as a step by step documenting one way of setting things up.  There are other ways to do most things in here.

Commands are indented
```
like this.
```

## Procedure ##
### Install mysql, turbocare, python, and apache2 packages. ###

```
sudo vi /etc/apt/sources.list
```
Remove "#" on deb http://in.archive.ubuntu.com/ubuntu/ dapper universe
and on  deb-src http://in.archive.ubuntu.com/ubuntu/ dapper universe lines.

```

sudo apt-get update

sudo apt-get install gcc libc6-dev  build-essential

sudo apt-get install mysql-server python-reportlab subversion

sudo apt-get install python-pysqlite2 python-mysqldb python-imaging  python-dev python-setuptools

sudo apt-get install apache2 libapache2-mod-python2.4

```

### Install turbogears ###

```
sudo easy_install -UZ  setuptools

wget http://files.turbogears.org/eggs/TurboJson-0.9.9-py2.4.egg

sudo easy_install -fZ TurboJson-0.9.9-py2.4.egg

sudo easy_install -Z  TurboGears

wget http://files.turbogears.org/eggs/SQLObject-0.7.1dev_r1860-py2.4.egg

sudo easy_install -fZ SQLObject-0.7.1dev_r1860-py2.4.egg
```

Note the manual installation of TurboJson and SQLObject is to overcome a conflict with turbocare and the later versions of these modules.  In the future it is hoped to correct this problem.

Note when using easy\_install we need to specify the install as unziped eggs as this stops apache from trying to extract the eggs into its own home directory.

### Additional TurboGears Widgets ###
Foreign Key look up widget
```
sudo easy_install TGFKLookup
```

### Install turbocare ###

```
cd  ~/

svn checkout http://turbocare.googlecode.com/svn/trunk/  turbocare
```

### Setup database ###
We should add a password to MySQL's root user but I will add that later.
```
mysql -u root -p
```
just press enter if you have no password yet.

at the prompt type:

```
create database turbocare;
```
press enter and then ctrl-D to exit.


```

cd ~/turbocare

python mysql_schema.py -d turbocare -u root -o schema_updt -f turbocare_schema.data

python mysql_schema.py -d turbocare -u root -o restore -f turbocare_backup.data

```
### Check standalone turbocare ###
```
cp dev-sample.cfg dev.cfg

vi dev.cfg

```
Check that all the variables are right. Particularly the sqlobject.dburi string.

```
cp turbocare/ReportDefinition-Sample.py turbocare/ReportDefinition.py
```
This file is used for defining custom formatting of reports.

```
cp turbocare/printer_list.py-example turbocare/printer_list.py
```
This file is used to setup printers.
```
python start-turbocare.py
```

If this loads without errors you have installed turbocare.

Check it's really working by visiting http://localhost:8080/.

If it is congratulations your half way to having turbocare and mod\_python installed.

Maybe you should grab a coffee now.

## Modpython time ##

Now to get mod\_python working

### Setup Turbocare for production ###

```
cd ~/turbocare

cp prod-sample.cfg prod.cfg

vi prod.cfg
```

This is the production configuration file.

Make sure the database variable is right.

sqlobject.dburi="mysql://root@localhost:3306/turbocare"

Make sure turbocare.basedir="/home/USERNAME/turbocare" points to where turbocare username is installed.

You can also change the log file locations if you want to.
```
cp turbocare/turbocare_modpython-sample.py turbocare/turbocare_modpython.py

vi turbocare/turbocare_modpython.py
```

Update the configuration file location in this file to where you have installed turbocare.  It should be on a line like this
turbogears.update\_config(configfile="/home/david/turbocare/prod.cfg")


```
sudo python setup.py install
```


We need to install the files for apache to be able to find them.

Note after every update you need to run this command.

```
sudo cp modpython_gateway.py /usr/lib/python2.4/site-packages/
```
Copy Modpython Gateway to pythons sitepackages.  This lets us use TurboGears with mod\_python.


### Apache Configuration ###

```
sudo cp apache-turbocare.conf /etc/apache2/sites-available/turbocare

sudo cp apache-ssl-turbocare.conf /etc/apache2/sites-available/turbocare-ssl

```
Copy Apache def files
```
sudo vi /etc/apache2/sites-available/turbocare
```

Change any references to /home/david to the home/USER where user is the user in which you have done the installation with.

```
sudo vi /etc/apache2/sites-available/turbocare-ssl
```
Change any references to /home/david to the home/USER where user is the user in which you have done the installation with.
```
sudo vi /etc/apache2/ports.conf
```

Add a new line with _Listen 443_ on it.

```
sudo apache2-ssl-certificate -days 365

sudo mkdir /var/www/.egg
```
Setup temp egg directory.

```
sudo chown -R www-data /var/www/.egg
```


Install ssl certificate.



### Enable sites and modules ###
```
sudo a2enmod mod_python
```

Enable mod\_python for apache2

```
sudo a2enmod  ssl
```

Enable ssl for apache2

```
sudo a2dissite default
```

Disable the default site as we want turbocare to be new default.

```
sudo a2ensite turbocare
```

Enable turbocare site

```
sudo a2ensite turbocare-ssl
```

Enable ssl version of turbocare.


### Reports ###

Now we need to change some permissions to make sure Apache's user can write reports.

```
cd ~/turbocare

sudo chown  www-data turbocare/static/reports

sudo chown  www-data turbocare/static/user_reports
```

### Report Writer ###
There is a file that is used when constructing custom reports.  By default, there is a sample of this file.  It is necessary to rename the file for the application to run.

```
cp turbocare/ReportDefinition-Sample.py turbocare/ReportDefinition.py
```

This file can be customized for your installation.

### Finishing off ###
```
sudo /etc/init.d/apache2 restart
```

Restart Apache2 to get it to load changes.


Go to http://ipaddressofmachine and https://ipaddressofmachine in a Web Browser.

Both should display first page of turbocare.


## Upgrades ##
To upgrade turbocare
```
cd ~/turbocare

svn update

sudo python setup.py install

sudo /etc/init.d/apache2 restart
```

## Ubuntu Dapper and SQLite ##

At the time of writing there were incompatiblities with the current version of turbocare and the version of sqlite which comes with Dapper.  To fix this follow these steps

```

sudo apt-get remove python2.4-pysqlite2

sudo apt-get install libsqlite3-dev

sudo easy_install -Z pysqlite

```
# References #
My instructions are based on the following websites.  However I was able to simplify as we removed some of the work for mod\_python by including necessary files in our svn version of turbocare.

http://trac.turbogears.org/wiki/ModPythonIntegration09

http://www.linode.com/wiki/index.php/Apache2_SSL_in_Ubuntu