# Introduction #

The configuration controller allows system administrators to edit:

  1. Addresses
  1. Ethnic Origins (Tribes)
  1. Departments/Locations
  1. Wards/Rooms/Beds
  1. Doctors
  1. Patient Types
  1. Insurance Options
  1. Packaging Types
  1. Groupings for Item Master, Locations, Customers, Vendors, Packaging, Compounds (groupings are useful for reporting).

# Details #

## Permissions ##

To access this controller, you'll need to go to the User Manager and add the "admin\_controllers\_configuration" and then add this permission to the groups with the users that you want to edit the TurboCare configuration.

The menu at the top of the program displays this option as "Configuration Admin".

## Address Table ##

### Summary ###
Addresses are used both for patients and vendors.  The structure of the database has addresses stored in two separate but identical tables (which was probably not the best idea, but hey, it makes it easier to separate out the inventory part of the program if needed).

### Fields ###
  * City Name - The name of the city
  * Block/Locality - Often used in cities
  * PIN Code - Numeric code used for mail
  * District - Area within a state
  * State - The state within the country
  * Country Code - A 3 letter code for the country
  * Un ECE Modifier [optional](optional.md) - Not sure - Not necessary at this point
  * Un ECE LO Code [optional](optional.md) - Not sure - Not necessary at this point
  * Un ECE LO Code Type - Not sure - Not necessary at this point
  * Un ECE Coordinate - Not sure - Not necessary at this point

## Tribes Table (Ethnic Origin) ##

### Summary ###
Used in Patient Registration.  In tradition Care2x, this is Ethnic origin configuration.  For Tribes to work, you'll need to create a "tribe" entry in the "Ethnic Origins Classification" table (the top part), and then you can create tribes (like "Ao", "Lotha", etc...) in the bottom section.

### Editing ###
There are two parts to editing this information.  First is the classification.  The Registration screen currently only shows entries with a classification of "tribe".  To add a the "tribe" entry:
  1. In the top section, press the "New" button
  1. Enter "tribe" in the "Selected Classification (Edit Mode)" edit box
  1. Press the Save button

Next, add some tribes.  To add the "Ao" tribe, do the following:
  1. In the top section, make sure that "tribe" is selected
  1. In the bottom half (the Types editor), press the "New" button
  1. In the "Selected Type (New Entry)" edit box, enter "Ao"
  1. Press the Save button

Now when you go to registration, you should see "Ao" in the list of tribe options.

## Departments\Locations ##

### Summary ###
Departments and locations (different names for essentially the same thing).  They are used in both the Hospital portion (Care2x) and Inventory section.  For the hospital operations, Departments are also used by Wards and Rooms.  For Inventory, they are used to store stock and do stock transfers.

Two tables store this data.  The Care2x table contains information regarding departments while the inventory module contains additional information which are properties for inventory (can the department sell items, receive items etc...).

### Field Notes ###
  * Has on call Doc - If the department has an "On call Doctor" then check this box.
  * Admit inpatient - If the department has patient admission for inpatients, then check this box (a department with wards would be one)
  * Admit out patient - If the department has out-patients (like the outpatient department) then check this box.
  * Has on call Nurse - If the department has an On call nurse, then check this box
  * Does Surgery - If the department does surgery, then check this box.
  * This Institution - If the department belongs to the hospital, then check this box (this is almost always checked)
  * Department Type - Choose what type of department it is.  Example, Computer department is Non medical.

## Wards ##

### Summary ###
Wards are used in the Hospital module only.  Wards are linked to Departments (which you edit separately).  Wards are used at the end of registration if the patient is being registered as an in-patient.  Rooms and Beds links to the Wards table, and you have the option of editing the Rooms table directly from this edit screen.

### Editing ###
When creating or editing a Ward, you have the option of Editing the rooms directly from here.  If you change the "Room Nr. Start" field or the "Room Nr. End" then the program will go and change the Rooms table (removing or adding rooms).  If you want to edit the table without changing the Rooms table, then use the "Save (No Room Updates)" button instead of the "Save" button

When making a room prefix, I'm not sure what we should do, but I was thinking of using the prefix to help the program classify the rooms, using COMM for common rooms, CMPR for semi-private and PRIV for private.

### Field Notes ###
  * Room Prefix - As mentioned above, the room prefix should indicate it's financial classification.  If rooms in the Ward are private, then mark the Ward "Room Prefix" as PRIV.  If it's common, then mark it "COMM", if it's common/private, then mark it "CMPR".
  * Closing Date - The date when the Ward is closed (not using it anymore).
  * Is Temp Closed - If the Ward is temporarily closed, then check this box.  Uncheck it when the ward re-opens.

## Rooms/Beds ##

### Summary ###
You can add rooms on their own, but normally rooms are created automatically from the Wards editing screen.  Rooms and Beds are used in patient registration if a patient is registered as an in-patient.

### Editing ###
You can either link a Room to a department or a Ward.  If you choose a ward, then the department is automatically selected as the department for the ward.  For the beds, you only have the option of choosing the number of beds, and they are automatically numbered sequentially.  Once beds are added to a room, you have the option for closing specific beds.

You can also see a listing of beds currently in use.

To close a bed, un-check it when editing the room.

## Doctors ##

### Summary ###
Doctors are used in patient registration if a patient is seeing a specific Doctor.  Later on, this will also be available for Medical records department to assign patients to doctors in the waiting room.

Eventually, this part will become part of a larger HR module (part of Care2x).

### Editing ###
Editing doctors is very much the same as registering a patient.  If a new doctor had visited the hospital in the past (as a customer or patient) then that information can be directly linked to the Employee/Doctor record.  If the doctor doesn't exist in the system, then adding a new doctor will create the "Person" record in the database.

## Patient Types ##

### Summary ###
(need [revision 208](https://code.google.com/p/turbocare/source/detail?r=208))
Patient types are classifications like "Self Pay", "Hospital Insurance", "Private Insurance".  This information is entered in during patient registration and can change from visit to visit.  For billing purposes, it is important to have certain values entered into the database (described below).  When a patient is marked as something other than "self\_pay" the billing module will require that a patient have an Insurance number of some kind (either a private insurance number, or a hospital insurance number).

### Mandatory Entries ###
Billing requires the following entries:
  1. Short name = "self\_pay", Name = "Self Pay"
  1. Short name = "private", Name = "Private Insurance"
  1. Short name = "hospital", Name = "Hospital Insurance"

The short name must be as above, but the Name can be modified (since it is used mostly for display purposes).

## Insurance Options ##

### Summary ###
Insurance options are used on patient registration.  If a patient is covered by insurance and has the required identification, then you can assign them the correct insurance company.  Billing sees this, and never asks for cash from the patient, assuming that the insurance company will cover 100% of the payment.

## Packaging Types ##

### Summary ###
Packaging types are used in Item Master editing in the Inventory module.  Packaging types describe how inventory items are contained, such as 100ml Bottles, 10x10x10cm boxes, etc...

## Item Master Groups ##

### Summary ###
If you want to Group your Item Master entries for reporting and program searching purposes.  Currently, the program doesn't filter on any of these, but in the future, there might be some Item Master (Catalog Item) groups which might become essential for program operation.

Item Master grouping is probably a very important grouping.

## Location Groups ##

### Summary ###
Group Inventory Locations (Departments) for reporting purposes.

## Customer Groups ##

### Summary ###
Group Customers into groups for reporting purposes.

## Vendor Groups ##

### Summary ###
Group Vendors for reporting purposes.

## Packaging Groups ##

### Summary ###
Group packaging types for reporting purposes.

## Compound Groups ##

### Summary ###
Group Compounds for reporting purposes.