# NGINX Configurations
The files contained here are simply for configuring the NGINX server and the GUnicorn workers. These pieces of code can be tested in the an nginx docker image. On a remote server though they will live in different locations but have the same values so long as the set up is the same.

## The Setup
The remote server needs to have a user and group called `flask_user` with a home directory and working directory at `/home/flask_user/` which will contain the `flask_app` repo here named as such.

You will need to:
- create an empty file called `/tmp/flask_app.sock` in that location.
- place the `uwsgi.service` file here `/etc/systemd/system/uwsgi.service`
- place the `uwsgi.ini` file here `/home/flask_user/uwsgi.ini`
- remove the `/etc/nginx/sites-enabled/default` file
- add `flask_app_proxy` to `/etc/nginx/sites-available/flask_app_proxy`
- symlink it to the enabled directory `ln -s /etc/nginx/sites-available/flask_app_proxy /etc/nginx/sites-enabled/`
- then retart all of the things
```bash
$ systemctl restart nginx \
> && systemctl daemon-reload \
> && systemctl status uwsgi.service \
> && systemctl enable uwsgi.service
```

# NGINX And GUnicorn files
The nginx file is the one ending in `.conf` and the gunicorn one ends in `.service`.
They need to be placed here on the destination system:
- `/etc/nginx/sites-available/flask_app.conf`
- `/etc/systemd/system/flask_app.service`
You will also need to unlink `/etc/nginx/sites-enabled/default` and in its place symlink the `flask_app.conf` from `sites-available`.
