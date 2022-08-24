import configparser
import os


from fabrictestbed_extensions.fablib.fablib import FablibManager
from logtools import CustomLogging
from toolkit import create_slice, delete_slice, set_env_vars

# Set up logging:
logger = CustomLogging('cluster').get_logger()

# Set up configuration:
fabric_config_dir = f"{os.path.dirname(os.path.realpath(__file__))}/../fabric_config"
logger.info(f'Applying config file: {fabric_config_dir}.')
try:
    config = configparser.ConfigParser()
    config.read(f"{fabric_config_dir}/fabric.conf")
except Exception as ex:
    logger.error(f"Unable to read {fabric_config_dir}/fabric.conf!")
    raise ex

logger.info('Gathering Slice details.')
slice_name = config['slice']['name']
site = config['slice']['site']
image = config['node']['image']
network_name = config['network']['name']
network_type = config['network']['type']
node_names = config['node']['names'].split()

# Set up OS environmental variables for FABlib:
set_env_vars()

# Import the FABlib API:
# TODO: Fix handling the pile of "Exception ignored in"s when executing fablib_manager().
logger.info('Importing FABlib.')
try:
    fablib = FablibManager()
    fablib.show_config()
except AttributeError:
    pass

__all__ = [
    'delete_slice',
    'create_slice',
]
