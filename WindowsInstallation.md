# Introduction #

How To Install TurboCare on Windows

# Details #

# Install the Software #

## Install MySQL ##

  1. Go to http://www.mysql.org/
  1. Download the latest version of MySQL version 5.0 or 5.1
  1. Install MySQL Server as a service

## Install Python ##

  1. Go to http://www.python.org/
  1. Download the latest version of Python version 2.4 (NOTE: version 2.5 is too new, it hasn't been tested)
  1. Install Python in the default folder

## Install TurboGears ##

  1. Go to http://docs.turbogears.org/1.0/InstallWindows
  1. Follow the above installation instructions in the "Installing TurboGears" section

## Install MySQL-Python module ##
  1. Go to "http://sourceforge.net/project/showfiles.php?group_id=22307"
  1. Download "MySQL-python.exe-1.2.1\_p2.win32-py2.4.exe" or newer
  1. Install the module

## Downgrade SQLObject to version 0.7.1dev ##
  1. Go to http://files.turbogears.org/eggs/
  1. Download "SQLObject-0.7.1dev\_r1860-py2.4.egg"
  1. In the same folder where you downloaded the file:
  1. execute `easy_install -fZ SQLObject-0.7.1dev_r1860-py2.4.egg`

## Downgrade TurboJSON ##
  1. Go to http://files.turbogears.org/eggs/
  1. Download "TurboJson-0.9.9-py2.4.egg"
  1. In the same folder where you downloaded the file:
  1. execute `easy_install -fZ TurboJson-0.9.9-py2.4.egg`

## Install the Python Imaging Library ##
  1. Open a command line window
  1. Type: `easy_install pil`

## Install ReportLab ##
  1. Download the Report lab DLLs from "http://www.reportlab.org/ftp/win32-dlls-py24.zip"
  1. Unzip the contents to "C:\Python24\DLLs"
  1. Download "http://www.reportlab.org/ftp/ReportLab_2_0.zip"
  1. Unzip the file and copy the the "reportlab" folder to "C:\Python24\Lib\site-packages" (Note: not the "reportlab\_2\_0" folder, the "reportlab" folder)

## Install PySQLite 2 ##
  1. Download "http://initd.org/pub/software/pysqlite/releases/2.3/2.3.3/pysqlite-2.3.3.win32-py2.4.exe"
  1. Install the program after downloading

## Additional TurboGears Widgets ##
Foreign Key look up widget
```
easy_install TGFKLookup
easy_install tgpaginate
```

## Install Subversion ##

  1. Go to: http://subversion.tigris.org/project_packages.html
  1. Look for the Windows download link (http://subversion.tigris.org/servlets/ProjectDocumentList?folderID=91)
  1. Download "svn-1.4.2-setup.exe" or newer
  1. Install Subversion

## Download TurboCare Source ##

  1. Create a folder on your computer where you want to install the source code for TurboCare
  1. Open a command line window, and change to the folder you created
  1. Follow the instructions at http://code.google.com/p/turbocare/source
  1. svn checkout http://turbocare.googlecode.com/svn/trunk/ turbocare

# Initial configuration #

## MySQL Database ##

  1. Make sure that the database is running (under services)
  1. From the Start Menu, select "Start \ All Programs \ MySQL \ MySQL Server 5.0 \ MySQL Command Line Client"
  1. `create database turbocare;`
  1. `exit;`
  1. In a command line window, change to the folder where you installed the TurboCare source
  1. Change to the "turbocare" sub-folder
  1. NOTE: make sure to put your root password in place of "password" in the two commands below
  1. `python mysql_schema.py -d turbocare -u root -p password -o schema_updt -f turbocare_schema.data`
  1. This next line will put in some sample data!!  Don't execute if you don't want sample data
  1. `python mysql_schema.py -d turbocare -u root -p password -o restore -f turbocare_backup.data`
  1. Open up the Query Browser window: "Start \ All Programs \ MySQL \ MySQL Query Browser"
  1. Make sure to use "turbocare" as the default schema, and "localhost" as the "Server Host"
  1. Select "File \ Open Script"
  1. Open the file called "care2x\_preload\_data.sql" located in the main TurboCare folder and execute it.
  1. In the same way, open and execute the "care2x\_preload\_data\_icd10\_en.sql"

## Custom Python Files ##
  1. Copy "dev-sample.cfg" to "dev.cfg"
  1. Edit the "dev.cfg" file and Check that all the variables are right. Particularly the sqlobject.dburi string.  `sqlobject.dburi="mysql://root:password@localhost:3306/turbocare"` and make password your root password.
  1. Copy "turbocare\ReportDefinition-Sample.py" to  "turbocare\ReportDefinition.py" (This file is used for defining custom formatting of reports).
  1. Copy "turbocare\printer\_list.py-example" to "turbocare\printer\_list.py"


## Test run ##
  1. Open a command line window and change to the TurboCare folder
  1. `python start-turbocare.py`
  1. When windows firewall will ask permission for this program to run. Say yes.