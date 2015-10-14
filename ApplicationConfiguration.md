#After installation, program configuration

# Introduction #

After installation, these instructions will help you get started with your TurboCare application, what data needs to be entered before you can start using the program productively.


## Creating an Administrative account ##
[Revision 263](https://code.google.com/p/turbocare/source/detail?r=263) has a new function documented here:

  1. Go to the project folder in a command line window
  1. type:
```
tg-admin shell
```
  1. In the TurboGears python shell, type (Substitute "Admin" for the user name you want, and "Password" for the new password you want)
```
import utils
utils.InitAdmin('Admin','Password')
```
  1. NOTE: some warning messages will scroll past during the command
  1. Exit the shell window (Linux/Unix 

&lt;Ctrl&gt;

+d, windows 

&lt;Ctrl&gt;

+z ??)
  1. When it asks to commit the transactions, choose "yes"
  1. Restart the server, you should be able to log-in with administrative rights using the new login

## Default Wards ##
([Revision 273](https://code.google.com/p/turbocare/source/detail?r=273))
For patient registration for inpatients, the program uses a default ward configuration option to assist the data entry.  When the program is started, TurboCare looks at the "app.cfg" file (located in the "turbocare/config" folder) for default ward mappings.

If there are no default ward mappings in the configuration file, TurboCare will find the first available ward and use that as the default.  If there are no wards, the program will warn the user and in-patient registrations will fail with an error.

Here is a sample configuration.  Replace the numbers with the id numbers for your installation's ward ids.  The following lines will need to be added to the "global" section of the configuration file like I've done below:
```
[global]
# Hospital Vairables
hospital.Ward_default_referral = 12
hospital.Ward_default_emergency = 11
hospital.Ward_default_birthdelivery = 7
hospital.Ward_default_walkin = 12	
hospital.Ward_default_accident = 11
```