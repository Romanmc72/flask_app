# flask_app
What's up outside world!

I want to learn how to write Flask applications and I started on the MEGA TUTORIAL
provided by https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-ii-templates

thx bruh.

# Production
## Initial Setup
### Debian 10.5 & Kubernetes 1.19.0
This portion of the README is dedicated to showing how I set up my debain box to make it run in production. The other part is dedicated to actually deploying the application in either local (meaning on your laptop) or production.

## Developing, Testing, And Deploying on Kubernetes
### Local Development Setup
I started with testing on `docker-compose` then moved to `minikube`. Check out the dockerfiles [here](https://github.com/Romanmc72/My_Dockerfiles/tree/master/webserver/flask) for the flask application and [here](https://github.com/Romanmc72/My_Dockerfiles/tree/master/db/postgres/images) for the database.

For running the whole stack in minikube, step 1 is download minikube. Minikube is essentially a single node kubernetes cluster that runs on your laptop. Great for testing kubernetes applications locally. Learn more on that [here](https://kubernetes.io/docs/setup/learning-environment/minikube/#:~:text=Minikube%20is%20a%20tool%20that,it%20day%2Dto%2Dday.) (or don't idgaf). If you have a mac (which I do) use homebrew to install minikube with ease via:

```bash
brew install minikube
```
(If you do not have a Mac, first off I am sorry. Secondly there are other ways to install it. Use your google powers to figure it out)

Then start minikube with:

```bash
minikube start
```

After this it is essential that you create a folder in the minikube node under `/var/lib/postgresql/data`. You can do that like this:

```bash
$ minikube ssh
                         _             _            
            _         _ ( )           ( )           
  ___ ___  (_)  ___  (_)| |/')  _   _ | |_      __  
/' _ ` _ `\| |/' _ `\| || , <  ( ) ( )| '_`\  /'__`\
| ( ) ( ) || || ( ) || || |\`\ | (_) || |_) )(  ___/
(_) (_) (_)(_)(_) (_)(_)(_) (_)`\___/'(_,__/'`\____)

$ sudo mkdir -p /var/lib/postgresql/data
$ exit
```

And likewise that you clone this repo and mount it to minikube like so:

```
minikube mount /wherever/you/downloaded/this/to/locally/flask_app:/host/flask_app
📁  Mounting host path /wherever/you/downloaded/this/to/locally/flask_app into VM as /host/flask_app ...
    ▪ Mount type:   <no value>
    ▪ User ID:      docker
    ▪ Group ID:     docker
    ▪ Version:      9p2000.L
    ▪ Message Size: 262144
    ▪ Permissions:  755 (-rwxr-xr-x)
    ▪ Options:      map[]
    ▪ Bind Address: 192.168.99.1:60307
🚀  Userspace file server: ufs starting
✅  Successfully mounted /wherever/you/downloaded/this/to/locally/flask_app to /host/flask_app

📌  NOTE: This process must stay alive for the mount to be accessible ...
```

and then just let this run until you are done testing. Now finally you can use [helm](https://helm.sh/) to install the chart for this application onto the minikube cluster. Navigate to [My_Helm_Charts](https://github.com/Romanmc72/My_Helm_Charts/tree/master/flask_app) repo to see the readme on how to do that.
