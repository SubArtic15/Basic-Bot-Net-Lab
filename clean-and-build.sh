echo "[+] Stop all running containers"
docker stop $(docker ps -q)

echo "[+] Removing dependent containers"
docker container prune -f

echo "[+] Removing existing image: ubuntu:botnet1"
docker image remove ubuntu:botnet1

echo "[+] Rebuilding image from Dockerfile"
docker build -t ubuntu:botnet1 dockerfiles/test/.

echo "[+] Creating a new container using ubuntu:botnet1"
docker run --rm -dt ubuntu:botnet1

echo "[+] Listing all running containers"
echo "IMAGE               ID           NAME"
docker container ls --format "{{.Image}}\t{{.ID}}\t{{.Names}}\t{{.Labels}}"
