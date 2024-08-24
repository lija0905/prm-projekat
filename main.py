import sys                                                                                                                                                                                                                                                            
from project.netconf import NETCONF

def configure():
        
        netconf = NETCONF(
            host="192.168.100.2",
            port=830,
            username="admin",
            password="vasilija"
        )

        available_capabilities = [
                "1. Show All Interfaces",
                "2. Get Interface Information",
                "3. Configure Interface",
                "4. Add New Loopback Interface",
                "5. Configure IPSec"
        ]

        print("Choose operation: ");
        for capability in available_capabilities:
            print(capability);
        
        choice = int(input());
        netconf.connect_to_device();

        if choice == 1:
            netconf.show_available_interfaces();
        if choice == 2:
            interface_name = input("Enter interface name: ")
            netconf.show_interface(interface_name)
        if choice == 3: 
            interface_name = input("Enter Interface Name: ")
            description = input("Enter Interface Description: ")
            ip_address = input("Enter Interface IP Address: ")
            subnet_mask = input("Enter Netmask: ")
            netconf.edit_interface_configuration(interface_name, description, ip_address, subnet_mask)
        if choice == 4:
            interface_name = input("Enter Interface Name: ")
            description = input("Enter Interface Description: ")
            ip_address = input("Enter Interface IP Address: ")
            subnet_mask = input("Enter Netmask: ")
            netconf.add_new_interface(interface_name, description, ip_address, subnet_mask)
        if choice == 5:
            remote_ip = input("Enter Remote IP Address: ")
            policy_number = input("Enter ISAKMP Policy Number: ")
            key = input("Enter The Pre-Share Key: ")
            set = input("Enter The Tag of IPSec Transform Set: ")
            map = input("Enter The Tag Of Crypto Map: ")
            match_address = input("Enter Match Address of ACL: ") # set needs to be different and map needs to be the same always
            netconf.configure_ipsec(remote_ip, key, policy_number, set, map, match_address)
            netconf.configure_interface_ipsec(map)
        else: print("The Choosen option doesn't exist. ")

def start():   
     
    try:
        configure()

        choice = input("Do you wish to continue with configurations? Y(es)")

        if choice == "Y" or choice == "Yes":
            configure()
        else: print(f"Goodbye!")

    except Exception as e:
            print(f"Error Creating New Interface: {e}")


start()

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        