#!/usr/bin/env python3
"""
Fetch soapbox comments from the MOQP database and make a web page 
from them.

Update History is in file __init__.py
"""


from soapbox.__init__ import VERSION
from moqputils.moqpdbutils import *
from moqputils.configs.moqpdbconfig import *
from datetime import datetime
from htmlutils.htmldoc import *


class Station():
    def __init__(self, call = None,
                       ops = None,
                       lid = None,
                       soapbox=None,
                       dbDat=None):
                               
        
        self.call = call
        self.ops = ops
        self.logID = lid
        self.soapbox = soapbox
        if dbDat:
            self._parseDB_data(dbDat)

    def csvLine(self, omitID=False):
        if omitID:
            return ('{}\t{}\t{}'.format(\
                  self.call,
                  self.ops,
                  self.soapbox))
        else:
            return ('{}\t{}\t{}\t{}'.format(\
                  self.call,
                  self.ops,
                  self.soapbox, 
                  self.logID))
                  
    def _parseDB_data(self, d):
        """ Fill values with 1 line from DB LOGHEADER table. """
        self.call = d['CALLSIGN']
        self.ops = d['OPERATORS']
        self.soapbox = d['SOAPBOX']
        self.logID = d['ID']

class SoapBox():
    def __init__(self):
        self.stationList = dict()
        self.valid = False

        self.fetchComments()
            
    def fetchComments(self):
        mydb = MOQPDBUtils(HOSTNAME, USER, PW, DBNAME)
        mydb.setCursorDict()

        dbData = mydb.read_query("""SELECT * FROM SOAPBOX_VIEW
                                    WHERE 1""")
        if len(dbData) >=1 :
            for d in dbData:
                station = Station(dbDat=d)
                if station.ops == station.call:
                    station.ops = ''
                if station.soapbox.startswith('CONTACT WITH BONUS '):
                    pass
                else:
                    self.stationList[station.call] = station
                #print(station.csvLine())
        
        self.valid = True
        #print(self.stationList)
        return self.valid

class csvSoapBox(SoapBox):
    
    def getCSV(self):
        csvData = ['CALLSIGN\tOPERATORS\tSOAPBOX COMMENTS\tLOGID']
        comment_keys = self.stationList.keys()
        for cs in comment_keys:
            csvData.append(self.stationList[cs].csvLine())
        return csvData

    def showRpt(self, csvd = None):
        if csvd == None:
            csvd = self.getCSV()
        for line in csvd:
            print(line)

class htmlSoapBox(csvSoapBox):
    def showRpt(self,csvd=None):
        csvd = self.getCSV()
        
        htmd = self.makeHTML(csvd)
        #print (htmd)
        self.getHTML(htmd)
        
    def makeHTML(self, csvd):
        htmd = []
        for crow in csvd:
            hrow = crow.split('\t')
            htmd.append(hrow)
        #print(htmd)
        return htmd
    
    def getHTML(self, htmld = None ):
       d = htmlDoc()
       d.openHead(\
           '{} Missouri QSO Party Soapbox Comments'\
               .format(YEAR),'./styles.css')
       d.closeHead()
       d.openBody()
       d.addTimeTag(prefix='Report Generated On ', 
                    tagType='comment') 
                         
       d.add_unformated_text(\
           """<h2 align='center'>{} Missouri QSO Party Soapbox Comments</h2>\n""".format(YEAR))

       d.addTable(htmld, header=True)
       d.closeBody()
       d.closeDoc()

       d.showDoc()
       #d.saveAndView('test.html')
       
    def getCSV(self):
        csvData = ['CALLSIGN\tOPERATORS\tSOAPBOX COMMENTS']
        comment_keys = self.stationList.keys()
        for cs in comment_keys:
            csvData.append(self.stationList[cs].csvLine(omitID=True))
        return csvData
