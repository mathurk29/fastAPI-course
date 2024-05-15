# Setup ElasticSearch and Kibana

## [Install Elasticsearch with Docker](https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html)

```bash
sudo sysctl -w vm.max_map_count=262144

docker network rm elastic

docker stop es01;  docker rm es01; 

docker stop kib01; docker rm kib01; 

docker network create elastic

docker pull docker.elastic.co/elasticsearch/elasticsearch:8.12.2

docker run --name es01 --net elastic -p 9200:9200 -it -m 1GB docker.elastic.co/elasticsearch/elasticsearch:8.12.2

docker cp es01:/usr/share/elasticsearch/config/certs/http_ca.crt .

export ELASTIC_PASSWORD="8re0N-fHphNhVK*kkPi8"

curl --cacert http_ca.crt -u elastic:$ELASTIC_PASSWORD https://localhost:9200

docker pull docker.elastic.co/kibana/kibana:8.12.2

docker run --name kib01 --net elastic -p 5601:5601 docker.elastic.co/kibana/kibana:8.12.2
```


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


## Setup new DB
config db in code and run 
`alembic upgrade head`

## Heroku Steps
```bash
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
```

## Ubuntu Prod Setup

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
```bash
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
```bash
psql -U potgress
adduser kshitij # created new user in postgress which also created in the ubuntu
su kshitij # created non root user to access prod db server
usermod -aG sudo kshitij # give sudo access to kshitij
ssh kshitij@<IPaddrr> #connect to Ubuntu machine (droplet) at it's IP addr using PgAdmin
sudo apt upgrade
cd /home/kshitij
mkdir app
virtualenv venv
source venv/bin/activate
mkdir src
git clone <git url>
pip install -r requirements.txt
```

### Set environment vars

create .env file outside of app folder for confidentiality
```bash
vi ~/.profile # put below command at end of this to persist in reboots
set -o allexport ; source <path to .env>; set +o allexport` # command to set env vars from file with syntax var=value. no need of export command
cd /home/kshitij/app
alembic upgrade head
uvicorn --host 0.0.0.0 app.main:app # 0.0.0.0 so that it listen to all request coming at it's IP from outside.
pip install gunicorn # cause uvicorn won't restart on reboot
pip install uvloop
pip install httptools
guvicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app  --bind 0.0.0.0:8000 # exposing on 8000 to outside world as it is standard http port 
ps -aef | grep -i gunicorn # to check 
```


### Create service
```bash
cd /etc/systemd/system/
vi api.service
copy contents of gunicorn.service into api.service
```
reference file: [gunicorn.service](../gunicorn.service)
```bash
sudo systemctl start api
sudo systemctl status api
sudo systemctl enable api # to enable auto statup on reboot
```

### Nginx
```bash
sudo apt install nginx
systemctl start nginx # open server IP - will show nginx home page from /var/www/html - set in below config file
cd /etc/nginx/sites-available
cat default
vi default
    # copy content to server localtion from:
```
reference file: [nginx](../nginx)


### Install certificates for https
sudo snap install --classic certbot
sudo certbot --nginx

### Firewall
```bash
sudo ufw status
sudo ufw allow http 
sudo ufw allow https
sudo ufw allow ssh
sudo ufw allow 5432 # for connecting to postgres - but highly risky as it opens up access to DB
sudo ufw enable
```


### Push changes

```bash
cd project folder
git pull 
sudo systemctl restart api
```


## Dockerize the app

### Push to Docker hub
```bash
docker image tag fastapi-course_api:latest mathurk29/fastapi-tutorial
docker push mathurk29/fastapi-tutorial
```


## Testing

### Fixture
A func which is run before your test is executed.