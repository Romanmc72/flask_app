# flask_app
What's up outside world!

I want to learn how to write Flask applications and I started on the MEGA TUTORIAL
provided by https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-ii-templates

thx bruh.

The code here all works in tandem with code in other repositories stored in my github. There are links all around so read up and try it yourself or don't. Live your life.

This `flask_app` is running full time on my home k8s cluster under the hostname [r0m4n.com](https://r0m4n.com). Take a look!

# Production
## Initial Setup
### Debian 10.5 & Kubernetes 1.19.0
This portion of the README is dedicated to showing how I set up my debain box to make it run in production. The other part is dedicated to actually deploying the application in either local (meaning on your laptop) or production. If you have a k8s cluster already or generally do not care, skip ahead to the [next section](#local-development-setup). Anyway, diving in!

#### Hardware
I got an old [Dell optiplex 9020](https://www.dell.com/en-us/work/shop/cty/pdp/spd/optiplex-9020-desktop?sc_err=notincat) from my dad who just got an upgraded computer from work. It came with 4GB RAM and a 500GB HDD. Although I was dog sitting for my brother and the dog hip-checked the computer onto the ground and cracked the hard drive. I ended up buying a new 1TB version of the same variety. I additionally got some old CD's that my mom was going to throw in the trash. I booted up the machine in Windows and downloaded Debian 10.5 amd64 onto the CD and then rebooted the computer and overwrote the windows OS with Linux.

#### Software
I went with the headless setup so there is no GUI and no desktop. After that I installed a few tools listed here and ran few other commands to modify the system.


```bash
# Add your username here to get sudo privileges
usermod -aG sudo <my-username>
```

then run `visudo` and update this line so you can run `sudo` without password interruption `<my-username> ALL=(ALL) NOPASSWD:ALL`

Now install a whole buncha stuff

```bash
# Install Docker
sudo apt-get remove docker docker-engine docker.io containerd runc
sudo apt-get update
sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common -y
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo apt-key add -
sudo apt-key fingerprint 0EBFCD88
sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/debian \
   $(lsb_release -cs) \
   stable"
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io -y

# Install kubernetes
sudo apt-get update && sudo apt-get install -y apt-transport-https curl
curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
cat <<EOF | sudo tee /etc/apt/sources.list.d/kubernetes.list
deb https://apt.kubernetes.io/ kubernetes-xenial main
EOF
sudo apt-get update
sudo apt-get install -y kubelet kubeadm kubectl
sudo apt-mark hold kubelet kubeadm kubectl

# This disables swap, which you need to do in order to be a k8s node
# idk why but that is what they said
sudo swapoff -a

# This changes something with the IP tables, not sure what but it is also
# necessary for running a k8s node.
cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
EOF
sudo sysctl --system

# I got rid of apache in favor of using `NGINX`
sudo apt-get remove apache2
sudo rm -r /var/lib/apache2
sudo apt autoremove
sudo rm /var/www/html/index.html

# I like these tools, if you don't then whatever
sudo apt-get install jq -y
sudo apt-get install tree -y
```

```bash
# Add your username here to get docker privileges
usermod -aG docker <my-username>
```

then if this command appears to look like it will run successfully to initialize the kubernetes master node, run it without the `--dry-run` flag. I ran with `--dry-run` first just to make sure everything installed correctly.

```bash
sudo kubeadm init --dry-run
```

And at this point you should have a running kubernetes master node running on a debian box! Well almost. Kubernetes does not come with any pre-configured networking client, so you need to pick and install one of their many options. Calico seemed like the most trusted and robust one but I could not get it to work so I went with flannel which starts and runs in just one command. Try it out for yourself.

```bash
kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml
```

very easy. This all worked for me and I have gone through this twice. This is the first time documenting it all so if I need to do it again we will see if it actually works. I provide no guarantee that the same setup works for you.

The last few things I did for production were install and setup NGINX, buy a domain name and set up the dynamic DNS client, then get SSL certificates and install `certbot` to auto-renew them. That is all a lot more than what I deem to be "in scope" for this repository so I will leave it for another day.

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
