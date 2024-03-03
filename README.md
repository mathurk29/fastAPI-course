# Setup ElasticSearch and Kibana

https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html

sudo sysctl -w vm.max_map_count=262144

docker network rm elastic

docker stop es01;  docker rm es01; 

docker stop kib01; docker rm kib01; 

docker network create elastic

docker pull docker.elastic.co/elasticsearch/elasticsearch:8.12.2

docker run --name es01 --net elastic -p 9200:9200 -it -m 1GB docker.elastic.co/elasticsearch/elasticsearch:8.12.2

docker cp es01:/usr/share/elasticsearch/config/certs/http_ca.crt .

export ELASTIC_PASSWORD="<put password here>"

curl --cacert http_ca.crt -u elastic:$ELASTIC_PASSWORD https://localhost:9200

docker pull docker.elastic.co/kibana/kibana:8.12.2

docker run --name kib01 --net elastic -p 5601:5601 docker.elastic.co/kibana/kibana:8.12.2


























Password for the elastic user (reset with `bin/elasticsearch-reset-password -u elastic`):
  xGDDrlnhLUB-yi*3w=zV

ℹ️  HTTP CA certificate SHA-256 fingerprint:
  b3a1bb0967a9538409ec7c43c21f2e82fa4067edc88e730fb336514bcc33302d

ℹ️  Configure Kibana to use this cluster:
• Run Kibana and click the configuration link in the terminal when Kibana starts.
• Copy the following enrollment token and paste it into Kibana in your browser (valid for the next 30 minutes):
  eyJ2ZXIiOiI4LjEyLjIiLCJhZHIiOlsiMTcyLjE4LjAuMjo5MjAwIl0sImZnciI6ImIzYTFiYjA5NjdhOTUzODQwOWVjN2M0M2MyMWYyZTgyZmE0MDY3ZWRjODhlNzMwZmIzMzY1MTRiY2MzMzMwMmQiLCJrZXkiOiJXSHlUQUk0QjJCN2hZSTI2SHNsWTpKNk1uNy1Fb1JwU3pYUjJzYWEtTXpBIn0=
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━



