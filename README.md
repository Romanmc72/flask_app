# flask_app
What's up outside world!

I want to learn how to write Flask applications and I started on the MEGA TUTORIAL
provided by https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-ii-templates

thx bruh.

# Production
## Initial Setup
### Raspberry Pi
So for this application I wanted to make it generalizeable enough to be deployed on either my raspberry pi server at home, or via a kubernetes setup. So a lot of these shell scripts are explicitly geared towards making dev/tes easier for locally testing the flask dev server, but for production I plan to launch it on nginx with gunicorn and a postgres backend.

**Installing**
Some steps I took to get the raspberry pi set up:
Make sure apache is not installed or running, then install nginx:
[Thanks to](https://gist.github.com/kizniche/5cea47b44cc1bfd15da837a1b634b9a5)
```bash
sudo apt-get update && sudo apt-get upgrade
sudo apt-get remove nginx* --purge
sudo /etc/init.d/apache2 stop
sudo apt-get remove apache* --purge
sudo apt-get install nginx-common
sudo apt-get install nginx
```
I then installed postgres
[Thanks to](https://opensource.com/article/17/10/set-postgres-database-your-raspberry-pi)
```bash
sudo apt install postgresql libpq-dev postgresql-client postgresql-client-common -y
```

**Databse setup**
signed in as the postgres superuser and created a flask user without superuser permissions.
```bash
sudo su postgres
createuser flask_user -P --interactive
Enter password for new role: 
Enter it again: 
Shall the new role be a superuser? (y/n) n
Shall the new role be allowed to create databases? (y/n) y
Shall the new role be allowed to create more new roles? (y/n) y
```
Then created the database and schema for the app and assigned the schema to the user.
```bash
psql
postgres=# CREATE DATABASE flask_db;
CREATE DATABASE
postgres=# \q
psql flask_db
flask_db=# CREATE SCHEMA flask_app AUTHORIZATION flask_user;
CREATE SCHEMA
flask_db=# SELECT * FROM INFORMATION_SCHEMA.SCHEMATA;
 catalog_name |    schema_name     | schema_owner | default_character_set_catalog | default_character_set_schema | default_character_set_name | sql_path 
--------------+--------------------+--------------+-------------------------------+------------------------------+----------------------------+----------
 flask_db     | pg_toast           | postgres     |                               |                              |                            | 
 flask_db     | pg_temp_1          | postgres     |                               |                              |                            | 
 flask_db     | pg_toast_temp_1    | postgres     |                               |                              |                            | 
 flask_db     | pg_catalog         | postgres     |                               |                              |                            | 
 flask_db     | public             | postgres     |                               |                              |                            | 
 flask_db     | information_schema | postgres     |                               |                              |                            | 
 flask_db     | flask_app          | flask_user   |                               |                              |                            | 
(7 rows)
flask_db=# \q
exit
```



## Deployments
Not exactly cutting edge CICD here, but it does make my life easier to have some helpers and shortcuts to run for sending updates from this repo to the production server.

# TODO fill this in

### Kubernetes
I started with testing on `docker-compose` then moved to `minikube`. Check out the dockerfiles [here]()
