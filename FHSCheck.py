#############################################################################
# File		: FHSCheck.py
# Package	: rpmlint
# Author	: Frederic Lepied
# Created on	: Fri Oct 15 17:40:32 1999
# Version	: $Id$
# Purpose	: check FHS conformity
#############################################################################

import AbstractCheck
import rpm
import re
import stat
import string

class FHSCheck(AbstractCheck.AbstractCheck):
    usr_regex=re.compile("^/usr/([^/]+)/")
    usr_subdir_regex=re.compile("X11R6|X386|bin|games|include|lib|local|sbin|share|src|spool|tmp")
    var_regex=re.compile("^/var/([^/]+)/")
    var_fsstnd_regex=re.compile("adm|catman|local|named|nis|preserve")
    var_subdir_regex=re.compile("account|lib|cache|crash|games|lock|log|opt|run|spool|state|tmp|yp")
    
    def __init__(self):
	AbstractCheck.AbstractCheck.__init__(self, "FHSCheck")

    def check(self, pkg, verbose):
	# Check only binary package
	if pkg.isSource():
	    return
	
	files=pkg.files()
	var_list=[]
	usr_list=[]
	
	for f in files.keys():
	    s=FHSCheck.usr_regex.search(f)
	    if s:
		dir=s.group(1)
		if not FHSCheck.usr_subdir_regex.search(dir):
		    if not dir in usr_list:
			print "W:", pkg.name, "non-standard-dir-in-usr", dir
			usr_list.append(dir)
	    else:
		s=FHSCheck.var_regex.search(f)
		if s:
		    dir=s.group(1)
		    if FHSCheck.var_fsstnd_regex.search(dir):
			if not dir in var_list:
			    print "W:", pkg.name, "FSSTND-dir-in-var", f
			    var_list.append(dir)
		    elif not FHSCheck.var_subdir_regex.search(dir):
			if not dir in var_list:
			    print "W:", pkg.name, "non-standard-dir-in-var", dir
			    var_list.append(dir)
			    
# Create an object to enable the auto registration of the test
check=FHSCheck()

# FHSCheck.py ends here