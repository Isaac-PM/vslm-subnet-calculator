import sys
import os


def print_networks(network_list: list[tuple] = []) -> None:
    for network in network_list:
        print("Network number", network_list.index(network) + 1, end=", ")
        if network[0] == "1":
            print("LAN", end=", ")
        elif network[0] == "2":
            print("WAN", end=", ")
        else:
            print("Unknown network type", end=", ")
        print(f"hosts: {network[1]}")


def check_ip(ip: str = "") -> bool:
    if len(ip.split(".")) != 4:
        return False
    for octet in ip.split("."):
        if not octet.isdigit():
            return False
        if int(octet) < 0 or int(octet) > 255:
            return False
    return True


def get_power_of_two(number: int = 0) -> int:
    power: int = 0
    while 2 ** power < number:
        power += 1
    return power


def from_subnet_to_ip(subnet: int = 0) -> str:
    if subnet < 0 or subnet > 32:
        return ""
    mask: str = ""
    for i in range(32):
        if i < subnet:
            mask += "1"
        else:
            mask += "0"
    return f"{int(mask[0:8], 2)}.{int(mask[8:16], 2)}.{int(mask[16:24], 2)}.{int(mask[24:32], 2)}"


print("\nWelcome to a VSLM subnetting calculator simulator!")
print("\nThis program will help you to calculate the number of subnets and hosts in a VSLM network.")
print("\nCreated by: Isaac-PM @ https://github.com/Isaac-PM using the method described by the professor M. Sc. Majid Bayani Abbasy.")

main_ip: str = input(
    "\nType the IP address to process (preferably ending in 0, v.g. 192.168.1.0): ")

if not check_ip(main_ip):
    print("Invalid IP address.")
    os.system("pause")
    sys.exit(1)
print("Valid IP address, continuing...")

finished: bool = False
network_list: list[tuple] = []

while not finished:
    print("\nSelect the network type: ")
    print("1. LAN")
    print("2. WAN (connection between two LANs)")
    network_type: str = input("Type the number of the network type: ")
    hosts: int = 2
    if network_type == "1":
        hosts: int = int(input("Type the number of desired hosts: "))
    network_list.append((network_type, hosts))
    finished = input("Do you want to add another network? (y/n): ") == "n"

print("\nThe following networks will be created: ")
print_networks(network_list)
network_list.sort(key=lambda x: x[1], reverse=True)

print("\nPress enter to continue...")
input()

os.system("cls" if os.name == "nt" else "clear")

print("\nCalculating the number of subnets and hosts...")
print("\nSuccess!")
last_ip: str = main_ip
for network in network_list:
    power: int = get_power_of_two(network[1] + 2)
    network_hosts: int = 2 ** power
    print(f"\nNetwork number {network_list.index(network) + 1}")  # OK
    print(f"\tNetwork type: {network[0] == '1' and 'LAN' or 'WAN'}")  # OK
    print(f"\tNetwork IP: {last_ip}/{32 - power}")  # OK
    print(
        f"\tBroadcast IP: {last_ip.split('.')[0]}.{last_ip.split('.')[1]}.{last_ip.split('.')[2]}.{int(last_ip.split('.')[3]) + network_hosts - 1}/{32 - power}")  # OK
    if network[0] == '1':
        print(
            f"\tGateway IP: {last_ip.split('.')[0]}.{last_ip.split('.')[1]}.{last_ip.split('.')[2]}.{int(last_ip.split('.')[3]) + 1}/{32 - power}")
    print(f"\tSubnet mask: /{32 - power} or {from_subnet_to_ip(32 - power)}")
    print(f"\t{network_hosts} hosts.")
    last_ip = ".".join(last_ip.split(
        ".")[:-1] + [str(int(last_ip.split(".")[-1]) + network_hosts)])
os.system("pause")
sys.exit(0)
