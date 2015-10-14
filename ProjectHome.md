TurboCare is a web based Hospital information system(HIS) written in [Python](http://www.python.org) using the [TurboGears](http://www.turbogears.org) framework.  Currently it can handle:
  1. Registration
    * New patients
    * Returning patients
  1. Inventory
    * Vendor Quotes
    * Purchase Orders
    * Stock transfers
  1. Billing
    * Creating and Editing bills for patients
  1. Dispensing
  1. Reporting
    * Custom reports using a query building interface

Future features:
  1. Waiting room
    * Assign patients to doctors
    * List patients which have not had their consultation
  1. Patient management
    * Edit details of patient
  1. Lab result data entry

It is based on the [Care2x](http://www.care2x.org) DB Schema using a MySQL back end.

## Getting Started ##
  1. Checkout the Installation instructions for [Linux with mod\_python](DeployUsingModPython.md) or [Windows](WindowsInstallation.md)
  1. Data initialization [instructions](InitializingData.md)

### Appreciation ###
It's amazing how a small project like this can be made with so little expense.  All the work thus far uses open source products, including: MySQL (the backend database engine), Care2x (the database schema), TurboGears (the Python based web development framework which brings together other great open source projects).

Looking for tools to develop in Python, try [Wing IDE](http://www.wingware.com/wingide), which I use for work on this project.
