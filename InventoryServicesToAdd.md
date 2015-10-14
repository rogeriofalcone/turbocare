# Introduction #

When the Registering a new patient, the program has to pick an inventory service to charge the patient/customer.  This page lists what entries you should enter and edit for inventory services needed for hospital operation.


# Details #

Add the following items to the Item Master:
  1. Registration
  1. Booklet printing
  1. Consultation Common
  1. Consultation Common+Private
  1. Consultation Private
  1. Consultation Very Private
  1. Nursing Common
  1. Nursing Common+Private
  1. Nursing Private
  1. Nursing Very Private
  1. Room Common
  1. Room Common+Private
  1. Room Private
  1. Room Very Private

All these items should be marked as: Service, For Sale, Selectable, Dispensable.  Note: Registration and Booklet printing should NOT have Dispensable checked.

After adding these items to the Item Master, then go to the "Stock Editor".  Add stock quantities for these services.  The quantity that you should add should be the estimate for the yearly use.  It isn't important if your estimate is wrong.  When creating new stock quantities of these services, remember to link it to the Item Master entry.  You do not need a purchase order for these entries.

NOTE: Be careful which deparment (location) you create these Stock Services in.  I would create a department called MRD (Medical Records Department), and then store these services in this department.  Of course, items of this stock type can still be moved to another department using stock transfers.  This is helpful for doing reports.

# Locations #

There are also some locations/departments you should add:
  1. MRD - Medical Records Department: mark it as a store, can sell.
  1. Customer - Where items get transferred to when purchased or used by patients/customers.  This is necessary for the program to operate.  When creating this location, make sure "Is Consumed" is marked