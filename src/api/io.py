#!/usr/bin/python

"""
    
    Author: Martin Sudmanns
    Institution: University of Salzburg, Department of Geoinformatics - Z_GIS
    Date: 18.4.2017
    
"""

########################################################################
# This file is part of Sentinel-Granules-Service.
# 
# Sentinel-Granules-Service is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# Sentinel-Granules-Service is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Sentinel-Granules-Service.  If not, see <http://www.gnu.org/licenses/>.
########################################################################

class Config:

    import sys 
    import ConfigParser

    def getConfig(self):
        
        

        #
        # This is where the config file is located
        #
        filename = "config/config.cfg"

        #
        # This is the dictionary where the config should be stored
        #
        configDict = {}

        #
        # Reade and pars the configuration file
        #
        config = self.ConfigParser.ConfigParser()
        config.read(filename)

        #
        # Extract the sections
        #
        sections = config.sections()

        #
        # Extract the options within the sections
        #
        for section in sections:

            #
            # Create a new section in the dictionary
            #
            configDict[section] = {}

            #
            # Extract the options of that section
            #
            options = config.options(section)

            #
            # Extract the option and perform error handling if something went wring
            #
            for option in options:
                try:
                    value = config.get(section, option)
                except:
                    logging.critical("Unable to read option " + str(option) + " in section " + str(section))
                    self.sys.exit()

                #
                # Write it to the dictionary
                #
                configDict[section][option] = value

        return configDict
    
class IO:
    import json
    import sys
    
    #
    # This is the array where the messages are stored.
    #
    msg = []

    def makeFailMessage(self):

        #
        # Collect all the messages and put them into the dictionary. Then
        # create a JSON out of it.
        #
        if len(self.msg) > 0:
            return self.json.dumps({"status": "FAIL", "messages": self.msg})
        else:
            return self.json.dumps({"status": "FAIL", "messages": ["Unknown error"]})


    def makeSuccessMessage(self, tiles):

        #
        # Create a JSON object with the data
        #
        return self.json.dumps({
            "tiles": tiles,
            "status": "OK"
        })

    def output(self, payload, status, stop):

        #
        # If the status is set to fail, collect the messages. It might be the case
        # that many messages should be sent to the server.
        #
        if status.upper() == "FAIL":
            self.msg.append(payload)

        #
        # If the program should stop, return either all errormessages or the data.
        # In either case, exit the program.
        # The data or the errormessages are encoded in JSON to allow easy handling in
        # the JavaScript client.
        #
        if stop == True:

            print "Content-Type: text/json"
            print

            if status.upper() == "FAIL":
                print self.makeFailMessage()
            if status.upper() == "OK":
                print self.makeSuccessMessage(payload)
            self.sys.exit()


    def checkInput(self, candidate):

        #
        # This variable holds the outcome of the checks
        #
        passed = []
        checks = 3
        
        #
        # The request key must be in the field storage
        #
        if "wkt" in candidate:
            passed.append(True)
        else:
            passed.append(False)
            self.output("Please specify the wkt request", "FAIL", False)

        #
        # Make sure that there is only the wkt request in the field storage
        #
        if len(candidate) == 1:
            passed.append(True)
        else:
            passed.append(False)
            self.output("invalid request(s): " + ", ".join(candidate), "FAIL", False)
        
        #
        # Check whether it is a valid WKT String. This can be only done if the first
        # check was already passed successfully 
        #
        if passed[0] == True:
            from wkt import WKT
            wkt = WKT()
            try:
                if wkt.checkWKT(str(candidate["wkt"].value)) == True:
                    passed.append(True)
                else:
                    passed.append(False)
                    self.output("Invalid WKT: " + str(candidate["wkt"].value), "FAIL", False)
            except:
				passed.append(False)
                self.output("Invalid regex pattern", "FAIL", False)
        
        #
        # Check whether the tests have been accomplished successfully
        #
        if passed.count(True) == checks:
            return True
        else:
            self.output("Something went wrong: " + str(passed.count(False)) + " of " + str(checks) + " checks failed.", "FAIL", True)
            return False
        
        
    def input(self, cgiinput):

        #
        # At first check whether it is valid. If yes, return the wkt
        #
        if self.checkInput(cgiinput) == True:
            
            return cgiinput["wkt"].value

class DB:
    from io import Config
    import psycopg2
    
    def getDatabaseConnection(self):
        
        #
        # Read the config file
        #
        cfg = self.Config()
        parameter = cfg.getConfig()["database"]
        
        #
        # Extract the parameter
        #
        databasename = parameter["database"]
        username = parameter["username"]
        host = parameter["host"]
        password = parameter["password"]

        #
        # Return the database connection
        #
        return self.psycopg2.connect("dbname='"+databasename+"' user='"+username+"' host='"+host+"' password='"+password+"'")
        
    def executeQuery(self, wkt):
        
        #
        # Open the database connection
        #
        dbconn = self.getDatabaseConnection()
        
        #
        # This is the SQL query
        #
        sql = "SELECT name FROM sentinel2_utm_granules WHERE ST_Intersects(geom, ST_Geomfromtext(%s ,4326))"
        
        #
        # Cursor
        #
        cur = dbconn.cursor()
        
        #
        # Executing the SQL command
        #
        cur.execute(sql, (wkt,))
        granules = cur.fetchall()
        
        #
        # Close database connection
        #
        dbconn.close()
        
        #
        # return granules.
        # If it is empty, return an empty list. If it is not empty,
        # reformat it into a un-nested array.
        #
        if len(granules) == 0:
            return []
        else:
            granule_list = []
            
            for g in granules:
                granule_list.append(g[0])
            
            return granule_list
