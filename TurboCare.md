TurboCare project - Hospital Information Systems based on the Care2x schema and using the TurboGears framework.

# The name #

Well, this is kind of boring.  The "Turbo" part is there because of the TurboGears framework and the "Care" comes from Care2x, where we have the schema from (for much of the hospital operations except for inventory, billing and dispensing).


# Summary, history and excuses #

CIHSR is a hospital located in the North East of India, in the state of Nagaland.  I was asked to help with the computer infrastructure portion of the project.  As a Computer Systems Analyst, this is the first time that I've worked with Hospital IT systems, but I had some assistance in becoming familiar with what some of the needs are.

There are many parts to Hospital IT and one of them is Hospital Information Systems Software.  In this case, Hospital Information Systems tracks most of, but not all of the Hospital data.  This data includes: Patient information, Inventory and some accounting.

I have only been exposed to Hospital operations in India (as a systems analyst), so I don't know how other hospitals operate in other countries in this respect.  The hospitals in India which I've been exposed to are charitable hospitals (i.e. low budget), and are often located in remote locations.  My guess is that most hospitals that do similar work have similar needs from a computer system and I guess that if there were one all encompassing system that covered everything a hospital needed, it could be used in every hospital, that is, if every hospital worked in the same way.

It seems to me that while hospitals have similar needs, they have different ways of going about their work.  This affects which parts of a system are desired first and are required before going live with a system.  As a programmer, it affects what kind of software I choose.

## Care2x ##

Care2x (www.care2x.org) is a great project providing Hospital Information Systems software at a great price... free!  It uses open source software in all it's parts: PHP, MySQL or PostgreSQL (and more).  It has some really nice cool features.  But it was missing some key features which we wanted to work in a particular fashion, so I couldn't just use it the way it was, which is ok because it's opensource.

So I downloaded and started to hack away at the PHP.  My PHP skills aren't very good, and they weren't getting better really quick.  I was starting to struggle with some of the coding and after a month of not making much progress on the changes I was hoping to make, I thought I'd take a different approach.

## TurboGears ##

After some months of research, it was decided that we (since there was more than just me working on the IT aspects of the project at this time) to attempt coding a custom inventory system (slightly limited in ability) and link it to Patient information so that we could track everything a patient consumes from hospital inventory, including services.

After some more time of research, we chose TurboGears as our frame work because