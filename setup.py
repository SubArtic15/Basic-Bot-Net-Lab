"""a setup script to initalize docker image information"""
# libraries
import os
from glob import glob
from random import choice
from multiprocessing import Pool


# constants
PRESET_USERNAMES_FILEPATH = 'data/usernames.txt'
PRESET_PASSWORDS_FILEPATH = 'data/passwords.txt'
DOCKERFILE_DIR_PATH = 'data/Dockerfiles'
DEFAULT_DOCKERFILE = 'data/BaseDockerfile'
DEFAULT_IMAGE_NAME = 'ubuntu:botnet-'
NUM_IMAGES = 20


# flags
REMOVE_BOTNET_IMAGES = True
CREATE_BOTNET_DOCKERFILES = True
BUILD_BOTNET_DOCKERFILES = True



# functions
def read_file_contents(filepath):
    """if a file exists, return its contents in a list; if no, return an empty list"""
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as fp:
            return fp.readlines()
    return []





if __name__ == '__main__':
    # TASK: remove all docker botnet images
    if REMOVE_BOTNET_IMAGES:
        def docker_rmi(id_):
            os.system(f"docker rmi {DEFAULT_IMAGE_NAME}{id_}")
        with Pool(processes=10) as func:
            func.map(docker_rmi, range(NUM_IMAGES))




    # TASK: create about 100 unique Dockerfiles using usernames and passwords files
    if CREATE_BOTNET_DOCKERFILES:
        base_dockerfile = read_file_contents(DEFAULT_DOCKERFILE)
        usernames = read_file_contents(PRESET_USERNAMES_FILEPATH)[:5] # setting limit for testing
        passwords = read_file_contents(PRESET_PASSWORDS_FILEPATH)[:5] # setting limit for testing

        for i in range(NUM_IMAGES):
            user = choice(usernames).strip()
            passwd = choice(passwords).strip()

            print(f"[+] NODE_ID={i}".ljust(17) + \
                  f"USERNAME={user}".ljust(30) + \
                  f"PASSWORD={passwd}")

            new_image = base_dockerfile
            for line_index in range(len(new_image)):
                new_image[line_index] = new_image[line_index].replace('ADD_USERNAME', user)
                new_image[line_index] = new_image[line_index].replace('ADD_PASSWORD', passwd)

            with open( os.path.join(DOCKERFILE_DIR_PATH, f"Dockerfile-{i}"), 'w+') as f:
                f.writelines(new_image)



    # TASK: Create unique images from all files created
    if BUILD_BOTNET_DOCKERFILES:
        all_docker_files = glob(f"{DOCKERFILE_DIR_PATH}/**")
        def docker_build(docker_file):
            """runs docker build on a specified file"""
            fp, fn = os.path.split(docker_file)
            _id = fn.split('-')[-1]
            os.system(f"docker build -f {docker_file} -t={DEFAULT_IMAGE_NAME}{_id} .")

        with Pool(processes=10) as func:
            func.map(docker_build, all_docker_files)
