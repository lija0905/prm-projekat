from ncclient import manager;
import sys                                                                                                                                                                                                                                                            
from ncclient.operations import RPCError                                                                                                                                                                                                                              
import xmltodict
import xml.dom.minidom
import os

class NETCONF:
    def __init__(self, host, port, username, password):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.session = None

    def connect_to_device(self):
        try:
            self.session = manager.connect(
                host = self.host,
                port = self.port,
                username = self.username,
                password = self.password,
                hostkey_verify = False,
                allow_agent =False,
                look_for_keys=False # Explicitly disable looking for keys     
            )

            print(f"Connected to the {self.host}")
        except Exception as e:
            print(f"Failed to connect to {self.host}: {e}")

    def show_available_interfaces(self):
        netconf_filter = NETCONF.load_netconf_filter(os.path.join('project\\filters', 'get-interfaces-filter.xml'), {})
        try:
            netconf_reply = self.session.get_config(source = 'running', filter = netconf_filter)
            print(xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml())

        except Exception as e:
            print(f"Error Getting Available Interfaces: {e}")

    def show_interface(self, interface_name):
        available_interfaces = NETCONF.return_available_interfaces()
        if ((interface_name not in available_interfaces)):
            print(f"No such interface on router")
            return

        netconf_filter = NETCONF.load_netconf_filter(
                            os.path.join('project\\filters', 'get-interface-filter.xml'),  { "interface_name": interface_name })
        try:
            netconf_reply = self.session.get_config(source = 'running', filter = netconf_filter)
            print(xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml())

        except Exception as e:
            print(f"Error Getting Available Interfaces: {e}")

    def edit_interface_configuration(self, interface_name, description, ip_address, subnet_mask):
        available_interfaces = NETCONF.return_available_interfaces()
        if ((interface_name not in available_interfaces)):
            print(f"No such interface on router")
            return
        
        netconf_filter = NETCONF.load_netconf_filter(
                            os.path.join('project\\filters', 'edit-interface-config.xml'),
                            { "interface_name": interface_name,
                              "description": description,
                              "ip_address" : ip_address,
                              "subnet_mask": subnet_mask
                            }
                            )
        try:
            netconf_reply = self.session.edit_config(target = 'running', config = netconf_filter)

            # result = self.session.copy_config(source="running", target="startup-config")
            print(xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml())

        except Exception as e:
            print(f"Error Getting Available Interfaces: {e}")

    def add_new_interface(self, interface_name, description, ip_address, subnet_mask): 

        netconf_filter = NETCONF.load_netconf_filter(
                            os.path.join('project\\filters', 'create-interface-config.xml'),
                            { "interface_name": interface_name,
                              "description" : description,
                              "ip_address" : ip_address,
                              "subnet_mask": subnet_mask
                            }
                            )
        try:
            netconf_reply = self.session.edit_config(target = 'running', config = netconf_filter)

            # result = self.session.copy_config(source="running", target="startup-config")
            print(xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml())

        except Exception as e:
            print(f"Error Creating New Interface: {e}")

    def configure_ipsec(self, remote_ip, key, policy_number, set, map, match_address):
        netconf_filter = NETCONF.load_netconf_filter(
                            os.path.join('project\\filters', 'configure-ipsec.xml'),
                            {
                              "remote_ip": remote_ip,
                              "key" : key,
                              "policy_number": policy_number,
                              "set" : set,
                              "map": map,
                              "match_address": match_address,
                            }
                            )
        
        try: 
            netconf_reply = self.session.edit_config(target = 'running', config = netconf_filter)
            print(xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml())

        except Exception as e:
            print(f"Error Configuring IPSec: {e}")

        # result = self.session.copy_config(source="running", target="startup-config")
        # print(xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml())

    def configure_interface_ipsec(self, map):
        netconf_filter = NETCONF.load_netconf_filter(
                            os.path.join('project\\filters', 'configure-interface-ipsec.xml'),
                            {
                              "map": map
                            }
                            )
        
        try: 
            netconf_reply = self.session.edit_config(target = 'running', config = netconf_filter)
            print(xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml()) # maybe check if ok and write some message?
            
        except Exception as e:
            print(f"Error Creating New Interface: {e}")

        # result = self.session.copy_config(source="running", target="startup-config")
        # print(xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml())
    
    def load_netconf_filter(file_path, params):
        with open(file_path, 'r') as file:
            xml_content = file.read()
        for key, value in params.items():
            placeholder = f'{{{key}}}'
            xml_content = xml_content.replace(placeholder, value)
        return xml_content
    
    def return_available_interfaces():
        return {
            "GigabitEthernet1",
            "GigabitEthernet2",
            "GigabitEthernet3",
            "GigabitEthernet4"
        }

    
