REM Change directory to the location of the Dockerfile
cd ./api

REM Build Docker image
docker build -t server_rfid .

REM Run Docker container
docker run --rm -it -v database:/home/database -p 8888:5000 --name server_rfid server_rfid
