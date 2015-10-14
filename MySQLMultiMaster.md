# Introduction #

For our production system at CIHSR we are using 3 MySQL 5 Servers.

# **HIS1** - A Master MySQL server with turbocare running through Apache

# **HIS2** - A Master MySQL server with turbocare running through Apache

# **BKP1** - A Slave MySQL server which has the backup software running on it.


## Required Background Reading ##
It is strongly recommended if you are not familiar with MySQL Database Replication that you read the following page http://www.onlamp.com/pub/a/onlamp/2005/06/16/MySQLian.html in addition to the section on the topic in the MySQL manual

## Assumptions ##
This guide assumes that you already have the HIS DB setup and working on HIS1 and HIS2.

It assumes MySql 5.0 or later is installed on the three servers.

It also assumes that an ssh server is installed and active on the three servers.

The best way to do this HowTo is to open up an ssh session to each server and leave it open for the duration of the HowTo.

# Steps #

### Setup Mysql Network Interfaces and hosts files ###

MySQL Replication Network:

Change IP's to

HIS 1: 10.0.0.3

HIS 2: 10.0.0.4

BKP1: 10.0.0.2

Subnet: 255.255.255.0

### Grant Replication Rights ###

On HIS1

```
mysql -u root -p
```
Enter in your mysql root password you set in step 2.
```
GRANT REPLICATION SLAVE, REPLICATION CLIENT
    ON *.*
    TO 'HIS2'@'10.0.0.4'
    IDENTIFIED BY 'HIS2 PASSWORD';

GRANT REPLICATION SLAVE, REPLICATION CLIENT
    ON *.*
    TO 'BKP1'@'10.0.0.2'
    IDENTIFIED BY 'BKP1 PASSWORD';
```
Note replace HIS2 PASSWORD and BKP1 PASSWORD with a real password.  Keep this password as we will need it later on.
```
exit;
```
ON HIS2

```
mysql -u root -p
```

Enter in your mysql root password you set in step 2.

```
GRANT REPLICATION SLAVE, REPLICATION CLIENT
    ON *.*
    TO 'HIS1'@'10.0.0.3'
    IDENTIFIED BY 'HIS1 PASSWORD';
exit;
```

Note replace HIS1 PASSWORD with a real password.  Keep this password as we will need it later on.

### Update configuration files ###
Download sample config files from http://turbocare.googlecode.com/files/mysql-config-Jan07.tar

Extract file
`tar -xvf mysql-config-Jan07.tar'

Copy etc/mysql/my.cnf-his1 to HIS1 from the extracted archive
```
mv my.cnf-his1 my.cnf
sudo cp my.cnf /etc/mysql/my.cnf
sudo /etc/init.d/mysql restart
```


Copy etc/mysql/my.cnf-his2 to HIS2 from the extracted archive
```
mv my.cnf-his2 my.cnf
sudo cp my.cnf /etc/mysql/my.cnf
sudo /etc/init.d/mysql restart
```


Copy etc/mysql/my.cnf-bckp to BKP1 from the extracted archive
```
mv my.cnf-bckp my.cnf
sudo cp my.cnf /etc/mysql/my.cnf
sudo /etc/init.d/mysql restart
```

The main differences between the files is that we set up different autoincrement offsets and server to enable multi-master operation of the system.

### Sync DB Files ###
On HIS1

```
mysqldump --user=root -p --extended-insert --master-data turbocare > /tmp/backup.sql

scp /tmp/backup.sql user@10.0.0.4:/tmp/
```

Where user is the local username you use to login on HIS2.

```
scp /tmp/backup.sql user@10.0.0.2:/tmp/
```

Where user is the local username you use to login on BKP1.

On HIS2
```
mysql -u root -p turbocare < /tmp/backup.sql
```
On BKP1

```
mysql -u root -p
create database turbocare;
exit;
mysql -u root -p turbocare < /tmp/backup.sql
```

Watch for any errors here.

### Start Slave Processors ###
On HIS2

```
mysql -u root -p
CHANGE MASTER TO MASTER_HOST='10.0.0.3', MASTER_PORT=3306, MASTER_USER='HIS2', MASTER_PASSWORD='HIS2 PASSWORD';
```
Note HIS2 PASSWORD is the Password you set in the GRANT section of the Howto.
```
start slave;
```

Wait 20 seconds

```
show slave status\G;

mysql> show slave status\G;
*************************** 1. row ***************************
             Slave_IO_State: Waiting for master to send event
                Master_Host: 10.211.55.6
                Master_User: slave_user
                Master_Port: 3306
              Connect_Retry: 60
            Master_Log_File: mysql-bin.000056
        Read_Master_Log_Pos: 98
             Relay_Log_File: LindaHottie-relay-bin.000049
              Relay_Log_Pos: 239
      Relay_Master_Log_File: mysql-bin.000056
           Slave_IO_Running: Yes
          Slave_SQL_Running: Yes
            Replicate_Do_DB: 
        Replicate_Ignore_DB: 
         Replicate_Do_Table: 
     Replicate_Ignore_Table: 
    Replicate_Wild_Do_Table: 
Replicate_Wild_Ignore_Table: 
                 Last_Errno: 0
                 Last_Error: 
               Skip_Counter: 0
        Exec_Master_Log_Pos: 98
            Relay_Log_Space: 22343
            Until_Condition: None
             Until_Log_File: 
              Until_Log_Pos: 0
         Master_SSL_Allowed: No
         Master_SSL_CA_File: 
         Master_SSL_CA_Path: 
            Master_SSL_Cert: 
          Master_SSL_Cipher: 
             Master_SSL_Key: 
      Seconds_Behind_Master: 0
1 row in set (0.00 sec)

ERROR: 
No query specified
```

Sample output of the command.

The most important lines that are Slave\_IO\_Running: YES and Slave\_SQL\_Running: YES.

If these do not say yes then you'll need to do some troubleshooting before going any further.


On BKP1

```
mysql -u root -p

CHANGE MASTER TO MASTER_HOST='10.0.0.3', MASTER_PORT=3306,
    MASTER_USER='BKP1', MASTER_PASSWORD='BKP1 PASSWORD';
```

Note BKP1 PASSWORD is the Password you set in the GRANT section of the Howto.

```
start slave;

show slave status\G;
```


The most important lines that are Slave\_IO\_Running: YES and Slave\_SQL\_Running: YES.

If these do not say yes then you'll need to do some troubleshooting before going any further.

On HIS1
```
mysql -u root -p

CHANGE MASTER TO MASTER_HOST='10.0.0.4', MASTER_PORT=3306,
    MASTER_USER='HIS1', MASTER_PASSWORD='HIS1 PASSWORD';

```

Note HIS2 PASSWORD is the Password you set in the GRANT section of the Howto.

```
start slave;

show slave status\G;
```


The most important lines that are Slave\_IO\_Running: YES and Slave\_SQL\_Running: YES.

If these do not say yes then you'll need to do some troubleshooting before going any further.


# Testing #

Load Turbocare on HIS1 and HIS2.

Add a new patient on HIS1 server and see if that patient appears on HIS2.

Then add a new patient on HIS2 and see if it appears on HIS1.

There is lots of fun to be had testing out that replication works fully.

The rest of the testing though is an exercise left to the reader, as I am in need of a cup of tea.


# Backups #
Zmanda's MySQL backup software looks pretty nice.  I will put up a howto soon here for that.
http://mysqlbackup.zmanda.com/
[Zmanda MySQL Backup Guide](http://www.zmanda.com/quick-mysql-backup.html)


# Troubleshooting #
Please give me feedback on any errors you have and I will update this section with common problems and their solutions.

# If Replication has failed #
NOTE THIS WILL ERASE DB ON HIS2.

## Resync HIS1 and HIS2 ##

On HIS1

```
mysqldump --user=root -p --extended-insert --master-data turbocare > /tmp/backup.sql

scp /tmp/backup.sql user@10.0.0.4:/tmp/
```

Where user is the local username you use to login on HIS2.

```
scp /tmp/backup.sql user@10.0.0.2:/tmp/
```

Where user is the local username you use to login on BKP1.

On HIS2
```
mysql -u root -p turbocare < /tmp/backup.sql
```
On BKP1

```
mysql -u root -p
create database turbocare;
exit;
mysql -u root -p turbocare < /tmp/backup.sql
```

Watch for any errors here.

### Start Slave Processors ###
On HIS2

```
mysql -u root -p
CHANGE MASTER TO MASTER_HOST='10.0.0.3', MASTER_PORT=3306, MASTER_USER='HIS2', MASTER_PASSWORD='HIS2 PASSWORD';
```
Note HIS2 PASSWORD is the Password you set in the GRANT section of the Howto.
```
start slave;
```

Wait 20 seconds

```
show slave status\G;

mysql> show slave status\G;
*************************** 1. row ***************************
             Slave_IO_State: Waiting for master to send event
                Master_Host: 10.211.55.6
                Master_User: slave_user
                Master_Port: 3306
              Connect_Retry: 60
            Master_Log_File: mysql-bin.000056
        Read_Master_Log_Pos: 98
             Relay_Log_File: LindaHottie-relay-bin.000049
              Relay_Log_Pos: 239
      Relay_Master_Log_File: mysql-bin.000056
           Slave_IO_Running: Yes
          Slave_SQL_Running: Yes
            Replicate_Do_DB: 
        Replicate_Ignore_DB: 
         Replicate_Do_Table: 
     Replicate_Ignore_Table: 
    Replicate_Wild_Do_Table: 
Replicate_Wild_Ignore_Table: 
                 Last_Errno: 0
                 Last_Error: 
               Skip_Counter: 0
        Exec_Master_Log_Pos: 98
            Relay_Log_Space: 22343
            Until_Condition: None
             Until_Log_File: 
              Until_Log_Pos: 0
         Master_SSL_Allowed: No
         Master_SSL_CA_File: 
         Master_SSL_CA_Path: 
            Master_SSL_Cert: 
          Master_SSL_Cipher: 
             Master_SSL_Key: 
      Seconds_Behind_Master: 0
1 row in set (0.00 sec)

ERROR: 
No query specified
```

Sample output of the command.

The most important lines that are Slave\_IO\_Running: YES and Slave\_SQL\_Running: YES.

If these do not say yes then you'll need to do some troubleshooting before going any further.


On BKP1

```
mysql -u root -p

CHANGE MASTER TO MASTER_HOST='10.0.0.3', MASTER_PORT=3306,
    MASTER_USER='BKP1', MASTER_PASSWORD='BKP1 PASSWORD';
```

Note BKP1 PASSWORD is the Password you set in the GRANT section of the Howto.

```
start slave;

show slave status\G;
```


The most important lines that are Slave\_IO\_Running: YES and Slave\_SQL\_Running: YES.

If these do not say yes then you'll need to do some troubleshooting before going any further.

On HIS1
```
mysql -u root -p

CHANGE MASTER TO MASTER_HOST='10.0.0.4', MASTER_PORT=3306,
    MASTER_USER='HIS1', MASTER_PASSWORD='HIS1 PASSWORD';

```

Note HIS2 PASSWORD is the Password you set in the GRANT section of the Howto.

```
start slave;

show slave status\G;
```


The most important lines that are Slave\_IO\_Running: YES and Slave\_SQL\_Running: YES.

If these do not say yes then you'll need to do some troubleshooting before going any further.


# Testing #

Load Turbocare on HIS1 and HIS2.

Add a new patient on HIS1 server and see if that patient appears on HIS2.

Then add a new patient on HIS2 and see if it appears on HIS1.

There is lots of fun to be had testing out that replication works fully.

The rest of the testing though is an exercise left to the reader, as I am in need of a cup of tea.


# References #


[An introduction to MySQL Replication](http://www.onlamp.com/pub/a/onlamp/2005/06/16/MySQLian.html)

[A good reference on multi-master replication](http://www.onlamp.com/pub/a/onlamp/2006/04/20/advanced-mysql-replication.html)

[Some useful MySQL Projects](http://kjalleda.googlepages.com/mysqlprojects)
[Straight from the people who wrote it](http://dev.mysql.com/doc/refman/5.0/en/replication-howto.html)