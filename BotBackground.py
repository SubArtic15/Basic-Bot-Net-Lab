"""
:summary Library of methods used to grab and start up custom docker images
:project Basic-Bot-Net-Lab
"""
from multiprocessing import Pool, cpu_count
from os import walk, path, system
from random import sample

from BotLibrary import run_command





def _get_dockerfile_subset(num_files=15):
    """get a subset of all Dockerfiles in repository"""
    dockerfile_dir = 'dockerfiles/'
    all_docker_files = []
    for root, dirs, files in walk(dockerfile_dir):
        for subdir in dirs:
            all_docker_files.append(path.join(root, subdir))
    return sample(all_docker_files, min(num_files, len(all_docker_files)))


def _parallel_creation(dockerfile_path):
    """builds a specified image from dockerfile_path"""
    image, id_ = dockerfile_path.split('/')[1].split('-')
    print(f"[+] Create docker image {image}:bot-{id_}")
    system(f"docker build -t {image}:bot-{id_} {dockerfile_path}")


def _create_docker_images(docker_subset):
    with Pool(processes=cpu_count() - 1) as func:
        func.map(_parallel_creation, docker_subset)


def _delete_docker_images(docker_subset):
    system("docker container prune -f")
    for dockerfile in docker_subset:
        image, id_ = dockerfile.split('/')[1].split('-')
        print(f"[+] Remove docker image {image}:bot-{id_}")
        system(f"docker image remove {image}:bot-{id_}")


def _create_container_array(docker_subset):
    container_ids = []
    for dockerfile in docker_subset:
        image, id_ = dockerfile.split('/')[1].split('-')
        cont_id = run_command(f"docker run --rm -dt {image}:bot-{id_}")
        container_ids.append(cont_id)
    return container_ids


def _stop_container_array(container_ids):
    for cont_id in container_ids:
        system(f"docker stop {cont_id}")


def _enable_ssh(container_ids):
    for cont_id in container_ids:
        cmd = f"docker exec -dt {cont_id} service ssh start"
        print(f"{cont_id}: {cmd}")
        system(cmd)


def set_up_env(num_images=15):
    docker_sample = _get_dockerfile_subset(num_images)
    _create_docker_images(docker_sample)

    container_ids = _create_container_array(docker_sample)
    _enable_ssh(container_ids)

    return docker_sample, container_ids


def close_up_env(docker_images, running_containers):
    _stop_container_array(running_containers)
    _delete_docker_images(docker_images)


def clean_docker_ip_range():
    for l0 in range(2, 256):
        run_command(f"ssh-keygen -R 172.17.0.{l0}")




if __name__ == '__main__':
    images, containers = set_up_env()
    close_up_env(images, containers)
