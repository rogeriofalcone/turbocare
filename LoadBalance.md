Use ldirectord-2

sudo apt-get install ldirectord-2


Steps:
Configure ldirectord to loadbalance between two servers:

```
# Global Directives
checktimeout=3
checkinterval=1
fallback=127.0.0.1:80

autoreload=yes
#logfile="/var/log/ldirectord.log"
#logfile="local0"
quiescent=yes


# LDirectord HTTP
virtual=192.168.1.20:80
        real=192.168.1.3:80 gate
        real=192.168.1.4:80 gate
        fallback=127.0.0.1:80 gate
        service=http
        request="/login"
        receive="Login"
        virtualhost=his.dmp.cihsr.org
        scheduler=rr
        #persistent=600
        #netmask=255.255.255.255
        protocol=tcp

# LDirectord HTTPS
virtual=192.168.1.20:443
       real=192.168.1.3:443 masq
       real=192.168.1.4:443 masq
       fallback=127.0.0.1:443
       service=https
       virtualhost=some.domain.com.au
       #request="index.html"
       #receive="Test Page"
       scheduler=rr
       #persistent=600
       #netmask=255.255.255.255
       protocol=tcp
```



Use hearbeat for

ldirectord

SAMBA

DHCP


```
#!/bin/bash
#---------------mini-rc.lvs_dr-director------------------------
#set ip_forward OFF for lvs-dr director (1 on, 0 off)
#(there is no forwarding in the conventional sense for LVS-DR)
cat       /proc/sys/net/ipv4/ip_forward
echo "0" >/proc/sys/net/ipv4/ip_forward

#director is not gw for realservers: leave icmp redirects on
echo 'setting icmp redirects (1 on, 0 off) '
echo "1" >/proc/sys/net/ipv4/conf/all/send_redirects
cat       /proc/sys/net/ipv4/conf/all/send_redirects
echo "1" >/proc/sys/net/ipv4/conf/default/send_redirects
cat       /proc/sys/net/ipv4/conf/default/send_redirects
echo "1" >/proc/sys/net/ipv4/conf/eth0/send_redirects
cat       /proc/sys/net/ipv4/conf/eth0/send_redirects

#add ethernet device and routing for VIP 192.168.1.20
/sbin/ifconfig eth0:110 192.168.1210 broadcast 192.168.1.20 netmask 255.255.255.255
/sbin/route add -host 192.168.1.20 dev eth0:10
#listing ifconfig info for VIP 192.168.2.10
/sbin/ifconfig eth0:20

#check VIP 192.168.1.20 is reachable from self (director)
/bin/ping -c 1 192.168.1.20
#listing routing info for VIP 192.168.1.20
/bin/netstat -rn

#setup_ipvsadm_table
#clear ipvsadm table
/sbin/ipvsadm -C
#installing LVS services with ipvsadm
#add http to VIP with round robin scheduling
/sbin/ipvsadm -A -t 192.168.1.20:http -s rr

#forward telnet to realserver using direct routing with weight 1
/sbin/ipvsadm -a -t 192.168.1.20:http -r 192.168.1.3 -g -w 1
#check realserver reachable from director
ping -c 1 192.168.1.3

#forward telnet to realserver using direct routing with weight 1
/sbin/ipvsadm -a -t 192.168.1.110:telnet -r 192.168.1.4 -g -w 1
#check realserver reachable from director
ping -c 1 192.168.1.4

#displaying ipvsadm settings
/sbin/ipvsadm

#not installing a default gw for LVS_TYPE vs-dr
#---------------mini-rc.lvs_dr-director------------------------



#!/bin/bash
#----------mini-rc.lvs_dr-realserver------------------
#installing default gw 192.168.1.254 for vs-dr
/sbin/route add default gw 192.168.1.254
#showing routing table
/bin/netstat -rn
#checking if DEFAULT_GW 192.168.1.254 is reachable
ping -c 1 192.168.1.254

#set_realserver_ip_forwarding to OFF (1 on, 0 off).
echo "0" >/proc/sys/net/ipv4/ip_forward
cat       /proc/sys/net/ipv4/ip_forward

#looking for DIP 192.168.1.1
ping -c 1 192.168.1.1

#looking for VIP (will be on director)
ping -c 1 192.168.1.20

#install_realserver_vip
/sbin/ifconfig lo:20 192.168.1.20 broadcast 192.168.1.20 netmask 0xffffffff up
#ifconfig output
/sbin/ifconfig lo:20
#installing route for VIP 192.168.1.20 on device lo:20
/sbin/route add -host 192.168.1.20 dev lo:20
#listing routing info for VIP 192.168.1.20
/bin/netstat -rn

#hiding interface lo:20, will not arp
echo "1" >/proc/sys/net/ipv4/conf/all/hidden
cat       /proc/sys/net/ipv4/conf/all/hidden
echo "1" >/proc/sys/net/ipv4/conf/lo/hidden
cat       /proc/sys/net/ipv4/conf/lo/hidden

#----------mini-rc.lvs_dr-realserver------------------
```