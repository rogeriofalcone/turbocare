# Introduction #

Before using the patient registration screen, you'll need to have some data enetered into the database.


# Details #

To initialize your data with care2x data:
  1. Open a Shell window
  1. Change to your TurboCare installation (the main folder)
  1. Make sure the files "care2x\_preload\_data.sql" and "care2x\_preload\_data\_icd10\_en.sql" are in the current folder (you need to have [revision 193](https://code.google.com/p/turbocare/source/detail?r=193) at least).
  1. run the following two commands, but REPLACE "--password=123" with your mysql root password.  If you have no password, then don't include the option.  Replace "turbocare" with your database name.

`mysql --user=root --password=123 turbocare < care2x_preload_data.sql`

`mysql --user=root --password=123 turbocare < care2x_preload_data_icd10_en.sql`

if you don't use a password:

`mysql --user=root turbocare < care2x_preload_data.sql`

`mysql --user=root turbocare < care2x_preload_data_icd10_en.sql`