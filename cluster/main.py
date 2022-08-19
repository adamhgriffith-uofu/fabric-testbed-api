import configparser
import os

from fabrictestbed_extensions.fablib.fablib import FablibManager
from logtools import CustomLogging

# Set up logging:
cluster_logger = CustomLogging('cluster').get_logger()

# Set up configuration:
fabric_config_dir = f"{os.path.dirname(os.path.realpath(__file__))}/../fabric_config"
cluster_logger.info(f'Applying config file: {fabric_config_dir}...')
config = configparser.ConfigParser()
try:
    config.read(f"{fabric_config_dir}/fabric.conf")
except Exception as ex:
    cluster_logger.error(f"Unable to read {fabric_config_dir}/fabric.conf!")
    raise ex

# Set up OS environmental variables for FABlib:
cluster_logger.info('Setting up OS environmental variables for FABlib...')
os.environ['FABRIC_CREDMGR_HOST'] = 'cm.fabric-testbed.net'
os.environ['FABRIC_ORCHESTRATOR_HOST'] = 'orchestrator.fabric-testbed.net'
os.environ['FABRIC_BASTION_HOST'] = 'bastion-1.fabric-testbed.net'
os.environ['FABRIC_PROJECT_ID'] = config['secrets']['fabric_project_id']
os.environ['FABRIC_BASTION_USERNAME'] = config['secrets']['fabric_bastion_username']
os.environ['FABRIC_BASTION_KEY_LOCATION'] = f"{fabric_config_dir}/fabric-bastion-key"
os.environ['FABRIC_SLICE_PRIVATE_KEY_FILE'] = f"{fabric_config_dir}/slice_key"
os.environ['FABRIC_SLICE_PUBLIC_KEY_FILE'] = f"{fabric_config_dir}/slice_key.pub"
os.environ['FABRIC_LOG_LEVEL'] = 'INFO'
os.environ['FABRIC_LOG_FILE'] = f"{fabric_config_dir}/fablib.log"
os.environ['FABRIC_TOKEN_LOCATION'] = f"{fabric_config_dir}/token.json"

# Import the FABlib API:
cluster_logger.info('Importing FABlib...')
# TODO: Fix handling the pile of "Exception ignored in"s when executing fablib_manager().
try:
    fablib = FablibManager()
    fablib.show_config()
except AttributeError:
    pass

# Set up the Slice
cluster_logger.info('Gathering Slice details...')
slice_name = config['slice']['name']
site = config['slice']['site']
image = config['node']['image']
network_name = config['network']['name']
network_type = config['network']['type']
node_names = config['node']['names'].split()

# Submit Slice request
try:
    # Create Slice:
    cluster_logger.info('Submitting Slice request...')
    fabric_slice = fablib.new_slice(slice_name)
    node_ifaces = []

    # Create nodes:
    for index, name in enumerate(node_names):
        node = fabric_slice.add_node(name=name, site=site, image=image)
        iface = node.add_component(model='NIC_Basic', name=f'NIC{index}').get_interfaces()[0]
        node_ifaces.append(iface)

    # Create network:
    fabric_slice.add_l3network(name=network_name, interfaces=node_ifaces, type=network_type)

    # Submit Slice request
    slice_id = fabric_slice.submit()
except Exception as ex:
    cluster_logger.error(f"Exception: {ex}")
    raise ex

# Display node attributes:
# actual_fabric_slice = fablib.get_slice(slice_id=slice_id)
# try:
#     network = actual_fabric_slice.get_network(name=network_name)
#     network_available_ips = network.get_available_ips()
#     cluster_logger.info(f"{network}")
# except Exception as ex:
#     cluster_logger.error(f"Exception: {ex}")
#     raise ex
#
# actual_nodes = actual_fabric_slice.get_nodes()
# for index, name in enumerate(actual_nodes):
#     node = actual_fabric_slice.get_node(name)
#     iface = node.get_interface(network_name=network_name)
#
#     node1_address = network_available_ips.pop(0)
#     node1_iface.ip_addr_add(addr=node1_address, subnet=network.get_subnet())
#
#     stdout, stderr = node1.execute(f'ip addr show {node1_iface.get_os_interface()}')
#     print (stdout)
#
#     stdout, stderr = node1.execute(f'ip route list')
#     print (stdout)