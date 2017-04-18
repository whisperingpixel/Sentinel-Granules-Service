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

from io import IO
from io import DB
from io import Config

import cgi
import sys
import json
    
if __name__ == "__main__":
    
    io = IO()
    cfg = Config()
    db = DB()
    
    #
    # Read the configuration file
    #
    config = cfg.getConfig()
    
    #
    # Read the input data at first since there might be a lot of errors. Expensive
    # parts of the program (read configuration, database) can be avoided.
    #
    wkt_string = io.input(cgi.FieldStorage())

    #
    # Execute the database query with the wkt string
    #
    try:
        utm_tiles = db.executeQuery(wkt_string)
    except Exception as e:
        io.output("Something went wrong: " + str(e), "FAIL", True)
    
    #
    # return the utm tiles
    #
    io.output(utm_tiles, "OK", True)
