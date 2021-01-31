import os, json


class CloudInventory(object):

    def __init__(self, name):
        self.user = name
        self.vms_list = "vms_list.json"
        self.data = None

    def checkout_a_vm(self):
        self.data = self._load_data()
        free_vm = None
        if self._get_vm_assigned_to_me():
            print("only one VM can be assigned to a user, you have already one VM assigned!")
            return
        for vm_name, attrs in self.data.items():
            if attrs["vm_state"] == "available":
                free_vm = {vm_name: attrs}
                print("Following Virtual machine is assigned to you:\n")
                for vm_name in free_vm.keys():
                    print("Name: {0}".format(vm_name))
                    for attr, val in free_vm[vm_name].items():
                        print("{0}: {1}".format(attr, val))
                self.data[vm_name]["vm_state"] = "un-available"
                self.data[vm_name]["assigned_to"] = self.user
                break
        # if free_vm:
        #     print("Following Virtual machine is assigned to you:\n")
        #     for vm_name in free_vm.keys():
        #         print("Name: {0}".format(vm_name))
        #         for attr, val in free_vm[vm_name].items():
        #             print("{0}: {1}".format(attr, val))
        if not free_vm:
            print("No VMs available at the minute, please try after sometime!")
        self._dump_data()

    def checkin_a_vm(self):
        """
        method to check in a vm back to inventory
        :return: None
        """
        self.data = self._load_data()
        vm = self._get_vm_assigned_to_me()
        if vm:
            self._cleanup(vm)
            self.data[vm]["vm_state"] = "available"
            self.data[vm]["assigned_to"] = None
            self._dump_data()
            print("VM {0} checked in successfully!".format(vm))
        else:
            print("No Vm is assigned to you at the moment!")

    def display_all_inventory_vms(self):
        self.data = self._load_data()
        print("Available VMs: ")
        for vm_name in self.data:
            print("VM {0} assigned to {1}".format(vm_name, self.data[vm_name]["assigned_to"]))

    def _cleanup(self, vm):
        # host = self.data[vm]["ip"]
        # port = 22
        # username = "demo"
        # password = "password"
        # command = "rmdir -r /tmp"
        # ssh = paramiko.SSHClient()
        # ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # ssh.connect(host, port, username, password)
        # stdin, stdout, stderr = ssh.exec_command(command)
        # lines = stdout.readlines()
        print("VM: {} cleaned up".format(vm))


    def _load_data(self):
        with open(self.vms_list) as json_file:
            data = json.load(json_file)
        return data

    def _dump_data(self):
        with open(self.vms_list, 'w') as json_file:
            json.dump(self.data, json_file)


    def _get_vm_assigned_to_me(self):
        for vm_name in self.data:
            if self.user == self.data[vm_name]["assigned_to"]:
                return vm_name


if __name__ == "__main__":
    name = input("Enter your name: ")
    user = CloudInventory(name)
    user_input = True
    while user_input:
        user_input = input("""Welcome to VM inventory:
                           Type a for checking out a VM
                           Type b for checking in a VM
                           Type c for getting list of inventory VMs
                           Type anything else to exit: """)
        if user_input == "a":
            user.checkout_a_vm()
        elif user_input == "b":
            user.checkin_a_vm()
        elif user_input == "c":
            user.display_all_inventory_vms()
        else:
            user_input = False
