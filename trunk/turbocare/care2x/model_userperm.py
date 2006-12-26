from datetime import datetime
from sqlobject import *
from turbogears import identity 
from turbogears.database import PackageHub
from model_inventory import cur_date_time

hub = PackageHub("care2x")
__connection__ = hub


class Users_Group(SQLObject):
    """
    An ultra-simple group definition.
    """
    
    # names like "Group", "Order" and "User" are reserved words in SQL
    # so we set the name to something safe for SQL
    class sqlmeta:
        table="tg_group"
    
    group_name = UnicodeCol( length=35, alternateID=True,
                            alternateMethodName="by_group_name" )
    display_name = UnicodeCol( length=255 )
    created = DateTimeCol( default=cur_date_time() )

    # collection of all users belonging to this group
    users = RelatedJoin( "Users_User", intermediateTable="user_group",
                        joinColumn="group_id", otherColumn="id" )

    # collection of all permissions for this group
    permissions = RelatedJoin( "Users_Permission", joinColumn="group_id", 
                              intermediateTable="group_permission",
                              otherColumn="permission_id" )


class Users_User(SQLObject):
    """
    Reasonably basic User definition. Probably would lbwant additional attributes.
    """
    import md5 #Because care2x uses md5
    # names like "Group", "Order" and "User" are reserved words in SQL
    # so we set the name to something safe for SQL
    class sqlmeta:
        table="care_users"
        idName='id'

    user_name = UnicodeCol( length=35, alternateID=True,
                           alternateMethodName="by_user_name", dbName='login_id' )
    email_address = UnicodeCol( length=255, alternateID=True, dbName='history',
                               alternateMethodName="by_email_address" )
    display_name = UnicodeCol( length=60, dbName='name' )
    password = UnicodeCol( length=255, dbName='password' )
    created = DateTimeCol( default=cur_date_time(), dbName = 'create_time' )

    # groups this user belongs to
    #modified from original
    groups = RelatedJoin( "Users_Group", intermediateTable="user_group",
                         joinColumn="id", otherColumn="group_id" )

    def _get_permissions( self ):
        perms = set()
        for g in self.groups:
            perms = perms | set(g.permissions)
        return perms
        
    def _set_password( self, cleartext_password ):
        "Runs cleartext_password through the hash algorithm before saving."
        hash = identity.encrypt_password(cleartext_password)
        self._SO_set_password(hash)
        
    def set_password_raw( self, password ):
        "Saves the password as-is to the database."
        self._SO_set_password(password)



class Users_Permission(SQLObject):
    class sqlmeta:
        table="tg_permissions"

    permission_name = UnicodeCol( length=35, alternateID=True,
                                 alternateMethodName="by_permission_name" )
    description = UnicodeCol( length=255 )
    
    groups = RelatedJoin( "Users_Group",
                        intermediateTable="group_permission",
                         joinColumn="permission_id", 
                         otherColumn="group_id" )
