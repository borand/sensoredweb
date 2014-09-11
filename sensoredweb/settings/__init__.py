from .base import *

try:        
    from .local import *
    # print "Loaded local settings"
except ImportError:
    # print "Import error while attempting to load local.py module"
    pass
