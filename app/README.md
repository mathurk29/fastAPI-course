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

export ELASTIC_PASSWORD="<>"

curl --cacert http_ca.crt -u elastic:$ELASTIC_PASSWORD https://localhost:9200

docker pull docker.elastic.co/kibana/kibana:8.12.2

docker run --name kib01 --net elastic -p 5601:5601 docker.elastic.co/kibana/kibana:8.12.2



━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


# Setup new DB
config db in code and run 
`alembic upgrade head`

# Heroku Steps
heroku login\
heroku create\
git push heroku main\
heroku open\
heroku logs --tail\
heroku run python manage.py shell\
heroku run bash\
heroku addons:create heroku-postgresql:mini\
heroku addons:destroy heroku-postgresql\
heroku apps:destroy\
heroku addons --all\
heroku apps --all


# Ubuntu Prod Setup

```bash
sudo apt update && sudo apt upgrade
sudo apt install python3-pip -y
sudo apt install python3-virtualenv -y
sudo apt install postgresql postgresql-contrib -y
psql --version
psql -U postgres -d postgres 
```
Output:
```
psql: error: connection to server on socket "/var/run/postgresql/.s.PGSQL.5432" failed: FATAL:  Peer authentication failed for user "postgres"
```


Local Auth = Ubuntu connecting to PG DB itself \
Peer auth = connecting from another machine (??)

postgres creates new user with name postgres in the Ubuntu, use that to login us `su - postgress`

```bash
sudo cat /etc/passwd | grep postgres
```


>The main difference between "su" and "su -" is the environment they provide when switching to another user.
>
>When you use "su" (switch user) without the hyphen, it keeps the current user's environment settings, such as PATH, home directory, etc. unchanged.
>
>Conversely, "su -" (or "su -l" or "su --login") provides a login environment for the new user, resetting the environment variables to those of the target user, including the home directory.
>
>So, "su -" is typically used when you want to completely switch to another user's environment, while "su" keeps your current environment intact.
>

```bash
su - postgres
psql
\password postgres
\q
```

config remote auth and remove peer auth
```
cd /etc/postgresql/15/main/

vi postgresql.conf
listen_addresses = '*'

vi [pg_hba.conf](pg_hba.conf)
change the authentication value (last col) from *peer* to *md5* for *local*
```
refer: 

[pg_hba.conf](../pg_hba.conf)

[postgresql.conf](../postgresql.conf)

`systemctl restart postgresql`



