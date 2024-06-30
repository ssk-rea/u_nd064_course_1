docker stop techtrends-app
docker rm techtrends-app
docker rmi techtrends:v1.0.0
docker build . -t techtrends:v1.0.0
docker run -d --name techtrends-app -p 3111:3111 techtrends:v1.0.0
