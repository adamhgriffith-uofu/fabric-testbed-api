import datetime
import cluster
import os


def create_slice() -> str:
    """
    Create the Slice in Fabric.
    :return: The Slice ID
    """
    try:
        # Create Slice:
        cluster.logger.info(f'Submitting Slice request for "{cluster.slice_name}".')
        fabric_slice = cluster.fablib.new_slice(cluster.slice_name)
        node_ifaces = []

        # Create nodes:
        for index, name in enumerate(cluster.node_names):
            node = fabric_slice.add_node(name=name, site=cluster.site, image=cluster.image)
            iface = node.add_component(model='NIC_Basic', name=f'NIC{index}').get_interfaces()[0]
            node_ifaces.append(iface)

        # Create network:
        fabric_slice.add_l3network(name=cluster.network_name, interfaces=node_ifaces, type=cluster.network_type)

        # Submit Slice request:
        slice_id = fabric_slice.submit(wait=True)
        return slice_id
    except Exception as ex:
        cluster.logger.error(f"Exception: {ex}")
        raise ex


def delete_slice() -> None:
    """
    Delete the Slice in Fabric.
    :return: None
    """
    try:
        cluster.logger.info(f'Deleting Slice: {cluster.slice_name}.')
        fabric_slice = cluster.fablib.get_slice(name=cluster.slice_name)
        fabric_slice.delete()
    except Exception as ex:
        cluster.logger.error(f"Exception: {ex}")
        raise ex


def renew_slice(add_days: int) -> None:
    """
    Renew the Slice in Fabric by extending the lease end time.
    :param add_days: Number of days from now to add to Slice lease
    :return: None
    """
    cluster.logger.info(f'Renewing Slice: {cluster.slice_name}.')
    end_date = (datetime.datetime.utcnow() + datetime.timedelta(days=add_days)).strftime("%Y-%m-%d %H:%M:%S")
    cluster.logger.info(f'New lease end date will be: {end_date}.')
    try:
        fabric_slice = cluster.fablib.get_slice(name=cluster.slice_name)
        fabric_slice.renew(end_date)
    except Exception as ex:
        cluster.logger.error(f"Exception: {ex}")
        raise ex


def set_env_vars() -> None:
    """
    Set up OS environmental variables for FABlib:
    :return: None
    """

    cluster.logger.info('Setting up OS environmental variables for FABlib.')
    os.environ['FABRIC_CREDMGR_HOST'] = 'cm.fabric-testbed.net'
    os.environ['FABRIC_ORCHESTRATOR_HOST'] = 'orchestrator.fabric-testbed.net'
    os.environ['FABRIC_BASTION_HOST'] = 'bastion-2.fabric-testbed.net'
    os.environ['FABRIC_PROJECT_ID'] = cluster.config['secrets']['fabric_project_id']
    os.environ['FABRIC_BASTION_USERNAME'] = cluster.config['secrets']['fabric_bastion_username']
    os.environ['FABRIC_BASTION_KEY_LOCATION'] = f"{cluster.fabric_config_dir}/fabric-bastion-key"
    os.environ['FABRIC_SLICE_PRIVATE_KEY_FILE'] = f"{cluster.fabric_config_dir}/slice_key"
    os.environ['FABRIC_SLICE_PUBLIC_KEY_FILE'] = f"{cluster.fabric_config_dir}/slice_key.pub"
    os.environ['FABRIC_LOG_LEVEL'] = 'INFO'
    os.environ['FABRIC_LOG_FILE'] = f"{cluster.fabric_config_dir}/fablib.log"
    os.environ['FABRIC_TOKEN_LOCATION'] = f"{cluster.fabric_config_dir}/token.json"

def set_ssh_config() -> None:
    """
    Set up an SSH config file for Fabric access via a shell.
    :return: None
    """
    cluster.logger.info('Setting up SSH config file for Fabric access via a shell.')
