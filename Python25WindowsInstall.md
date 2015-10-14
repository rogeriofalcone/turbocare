#Python 2.5 TurboCare Installation

# Introduction #

THERE ARE STILL PROBLEMS WITH AJSON OPERATIONS!!!!

Instructions for installing TurboCare on a system using Python version 2.5.  This document highlights the differences with the regular Python version 2.4 installation.  NOTE that while TurboGears now supports version 2.5 of Python, TurboCare has not been tested yet.  This document is a work in progress.

# Details #

## Install Python ##

  1. Go to http://www.python.org/
  1. Download the latest version of Python version 2.5
  1. Install Python in the default folder

## Install MySQL-Python module ##
  1. At the command line, execute `easy_install mysql-python`

## DO NOT Downgrade SQLObject to version 0.7.1dev ##

## DO NOT Downgrade TurboJSON ##

## Install ReportLab ##
  1. Download the Report lab DLLs from "http://www.reportlab.org/ftp/win32-dlls-py25.zip"
  1. Unzip the contents to "C:\Python25\DLLs"
  1. Download "http://www.reportlab.org/ftp/ReportLab_2_0.zip"
  1. Unzip the file and copy the the "reportlab" folder to "C:\Python25\Lib\site-packages" (Note: not the "reportlab\_2\_0" folder, the "reportlab" folder)

## Install PySQLite 2 ##
  1. At the command prompt, type `easy_install pysqlite`

## Scriptaculous ##
  1. Download "http://files.turbogears.org/eggs/Scriptaculous-1.6.2-py2.4.egg"
  1. Using a command prompt, change to the folder where the above file is downloaded to
  1. Type `easy_install Scriptaculous-1.6.2-py2.4.egg`

## Install TGPaginate ##
  1. At the command prompt, type: `easy_install tgpaginate`

## Source code updates ##
  1. Line 2 in "turbocare\turbocare\model\_inventory.py" needs to be commented out: `from __future__ import division`