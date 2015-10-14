# Introduction #

Some versions have important notes.  Read below for important information regarding updating to a specific version.

# [Revision 290](https://code.google.com/p/turbocare/source/detail?r=290) #

  1. Removed "tgpaginate" requirement

# [Revision 289](https://code.google.com/p/turbocare/source/detail?r=289) and earlier (I missed a few entries) #

Run the following commands:
  1. `easy_install TGFKLookup`
  1. `easy_install tgpaginate`

# [Revision 216](https://code.google.com/p/turbocare/source/detail?r=216) #

  1. In the turbocare installation folder run: `python mysql_schema.py -o schema_updt -d turbocare -p 123 -f turbocare_schema.data`
  1. This fixes an issue with the care\_ward table.