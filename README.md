LanCie Point-of-Sale website
============================

Website to handle drinks at LanCie events

Requirements
============
To run the website at least the following things are needed:
Python 3.2+
Pyro4
Django 1.6

This readme assumes that Python is run with the command "python3".

Running the site
================
Because part of the website (namely the routing app) needs to alter iptables rules it is necessary to have superuser priveledges. There are several layers of security to make sure that no commands can be accidentally run by the superuser. The code to do this is stored in routing/access.py so it is only needed to run this file with superuser priveledges. To run this it is only necessary to run "sudo python3 routing/access.py" and the website will take care of the rest. Communication is done through Pyro4 so it is also necessary to run the Pyro4 nameserver, this can be done with simply executing the command "python3 -m Pyro4.naming".

