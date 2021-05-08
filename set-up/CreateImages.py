"""
:summary generates custom Dockerfiles based on dependencies
:project Basic-Bot-Net
:author SubArtic15
"""
import os
from random import sample


def _get_file_contents(file_name):
    """generate and strip file contents"""
    with open(file_name, 'r') as f:
        data = f.readlines()
        data = list(map(lambda l: l.strip(), data))
    return data


if __name__ == '__main__':
    # get list of all: images, usernames, passwords
    images = _get_file_contents('dependencies/images.txt')
    users = _get_file_contents('dependencies/usernames.txt')
    passwds = _get_file_contents('dependencies/passwords.txt')

    for image in images:
        dockerfile_id = 0
        for user in users:
            for passwd in sample(passwds, 10):
                image_folder_name = f"{image}-{dockerfile_id}"
                image_folder_path = f"../dockerfiles/{image_folder_name}"

                # if the folder exists, then remove it
                if os.path.exists(image_folder_path):
                    print(f"[-] Removing Directory: {image_folder_path}")
                    for file in os.listdir(image_folder_path):
                        os.remove(f"{image_folder_path}/{file}")
                    os.rmdir(image_folder_path)

                # create directory, since it likely doesn't exist
                print(f"[+] Creating Directory: {image_folder_path}")
                os.mkdir(image_folder_path)

                print("[+] Creating a dockerfile with the following characteristics")
                print("Image Name:{}\nUsername: {}\nPassword: {}".format(image, user, passwd))
                print('-' * 20)

                dockerfile = _get_file_contents('dependencies/base-dockerfile')
                for index, line in enumerate(dockerfile):
                    if "IMAGE" in line:
                        dockerfile[index] = dockerfile[index].replace("IMAGE", image)

                    if "USER" in line:
                        dockerfile[index] = dockerfile[index].replace("USER", user)

                    if "PASSWD" in line:
                        dockerfile[index] = dockerfile[index].replace("PASSWD", passwd)

                with open(f"{image_folder_path}/Dockerfile", 'w') as image_path:
                    for line in dockerfile:
                        image_path.write(line + '\n')

                print()
                dockerfile_id += 1
