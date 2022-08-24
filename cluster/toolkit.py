import cluster
import os


def create_slice() -> str:
    """
    Create the Slice in Fabric.
    :return: The Slice ID
    """
    try:
        # Create Slice:
        cluster.logger.info('Submitting Slice request.')
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


def delete_slice():
    """
    Delete the Slice in Fabric.
    :return:
    """
    try:
        cluster.logger.info(f'Deleting Slice: {cluster.slice_name}.')
        fabric_slice = cluster.fablib.get_slice(name=cluster.slice_name)
        result = fabric_slice.delete()
        return result
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
    os.environ['FABRIC_BASTION_HOST'] = 'bastion-1.fabric-testbed.net'
    os.environ['FABRIC_PROJECT_ID'] = cluster.config['secrets']['fabric_project_id']
    os.environ['FABRIC_BASTION_USERNAME'] = cluster.config['secrets']['fabric_bastion_username']
    os.environ['FABRIC_BASTION_KEY_LOCATION'] = f"{cluster.fabric_config_dir}/fabric-bastion-key"
    os.environ['FABRIC_SLICE_PRIVATE_KEY_FILE'] = f"{cluster.fabric_config_dir}/slice_key"
    os.environ['FABRIC_SLICE_PUBLIC_KEY_FILE'] = f"{cluster.fabric_config_dir}/slice_key.pub"
    os.environ['FABRIC_LOG_LEVEL'] = 'INFO'
    os.environ['FABRIC_LOG_FILE'] = f"{cluster.fabric_config_dir}/fablib.log"
    os.environ['FABRIC_TOKEN_LOCATION'] = f"{cluster.fabric_config_dir}/token.json"
