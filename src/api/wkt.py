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


class WKT:
    
    from io import Config
    import json
    
    def checkWKT(self, candidate):
        import re
        
        #
        # Get the regex
        #
        cfg = self.Config()
        regex = cfg.getConfig()["checks"]["regex"]
        regex = regex.split(" ")
        
        #
        # As the regex check is so expensive, we can skip the regex check when the array is empty.
        #
        if len(regex) == 0:
            return True

        #
        # These are the pattern against which we want to check the candidate
        #
        patterns = []
        for r in regex:
            patterns.append(re.compile(r))
        
        #
        # Replace leading or trailing quotes from the request
        #
        candidate = re.sub(r'^("|\')|("|\')$', '', candidate)        
        
        #
        # Check the candidate. If there is a match, return True as the
        # test was successfully.
        #
        for pattern in patterns:
            if pattern.match(candidate) is not None:
                return True
        
        #
        # If none of the patterns fit, return false
        #
        return False
            
        
