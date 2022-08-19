"""
Script to create an arbitrary slice on Fabric

Known Issues

* ``fablib = fablib_manager()`` is known to spit out ``AttributeError``s. We have submitted `Pip fabrictestbed-extensions 1.2.4 – “Exception ignored in” <https://learn.fabric-testbed.net/forums/topic/pip-fabrictestbed-extensions-1-2-4-exception-ignored-in/#post-2656>`_ to the Fabric team.

"""

import os

from fabric_config import fabric_rc
from fabrictestbed_extensions.fablib.fablib import FablibManager as fablib_manager

# Load the environmental variables:
os.environ['DEFAULT_FABRIC_CONFIG_LOCATION'] = f"{os.path.dirname(os.path.realpath(__file__))}/fabric_config"
fabric_rc.initialize()

# TODO: Handle the pile of "Exception ignored in"s when executing fablib_manager().
# Import the FABlib API:
try:
    fablib = fablib_manager()
    fablib.show_config()
except AttributeError:
    pass

# Create a slice:
slice_name = 'MySlice'
site = fablib.get_random_site()
print(f"Site: {site}")
node1_name = 'Node1'
node2_name = 'Node2'
image = 'default_ubuntu_20'
node1_nic_name = 'NIC1'
node2_nic_name = 'NIC2'
network_name = 'NET1'