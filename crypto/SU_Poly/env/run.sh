sudo docker build . -t auth
sudo docker run --name auth -d -p 1337:9999 auth
