"""
mqpsoapbox - Fetch soapbox comments from the MOQP database and 
             make a web page from them.
Update History:
* Sat Apr 27 2024 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.0.1 - First interation

* Fri Apr 17 2026 Mike Heitmann, N0SO <n0so@arrl.net>
- V1.0.0 - Fix for Issue #1 (bad path module importing)
-          The original code used a 'view' in the database. That's
           OK, but most views are tied to a year. The view query was
           put in the string and made to take the year for the databse
           name from the moqpdbconfig.py module. This will make the
           query track the defined configuration.
"""
VERSION = '1.0.0' 

