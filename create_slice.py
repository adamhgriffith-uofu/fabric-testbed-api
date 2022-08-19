"""
Script to create an arbitrary slice on Fabric
"""

import logtools
import os

from fabric_config import fabric_rc
from fabrictestbed_extensions.fablib.fablib import FablibManager as fablib_manager

# Load the environmental variables:
os.environ['DEFAULT_FABRIC_CONFIG_LOCATION'] = f"{os.path.dirname(os.path.realpath(__file__))}/fabric_config"
fabric_rc.initialize()

# Import the FABlib API:
fablib = fablib_manager()
fablib.show_config()

# Create a slice:
