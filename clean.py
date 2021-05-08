from os import system

for repo in ["ubuntu", "debian"]:
    for tag_id in range(1, 200):
        system(f"docker image remove {repo}:bot-{tag_id}")
