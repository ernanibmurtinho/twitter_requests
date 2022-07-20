# Welcome to twitter requests demo - ernanibmurtinho 👋

[![Docker](https://img.shields.io/badge/Docker-20.10.6-blue.svg?cacheSeconds=2592000)](/uri)
[![Pyspark](https://img.shields.io/badge/Pyspark-3.0.2-red.svg?cacheSeconds=2592000)](/uri)
[![Python](https://img.shields.io/badge/Python-3.7-yellow.svg?cacheSeconds=2592000)](/uri)

> Here we will have the twitter api case
### 🏠 [Homepage](https://github.com/ernanibmurtinho/twitter_requests)

Twitter api - Ernani
===================================
The purpose of this project, is to gather data from twitter api and make them
available for data analysis.

Installation
------------

PyPi
----
In order to setup your local environment, add the contents of the requirements.txt
of this project to your own.

After of that, install the libs on a new environment (e.g.):

```bash
    $source ~/venvp3_8/bin/activate
    (venvp3_8) $pip install -r requirements.txt
```

Setup Docker
----
linux ubuntu distros (linux mint in this case)

step 1
```bash
    $sudo apt-get update
    $sudo apt-get install \
          apt-transport-https \
          ca-certificates \
          curl \
          gnupg \
          lsb-release
```

step 2

```bash
    $curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
    $echo   "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu focal stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    $sudo apt-get update
```

step 3

```bash
    $sudo apt-get update
    $sudo apt-get install docker-ce docker-ce-cli containerd.io
```

Test install
--------------

```bash
    $sudo docker run hello-world
```

> ref: link - https://docs.docker.com/engine/install/

Run Pex
========

Twitter analysis

This ingestion code, is responsible to gather data from twitter APIs, 
and stores it locally.

* In order to make a local deployment, you will need to have docker installed
* on your local machine
* Please, follow the steps above to configurate your local environment.

Run instructions
-----------------

To make the build of pex and execute the code inside the image, please follow the steps below:

```bash
  $ make deploy-prod
```

The results, will be generated on the file out/result/twitter_ingestion/ in parquet format.
If the results aren't the expected, then will be raised 
an error ( the file for comparison, are located inside the directory result/test_parquet)
The last run log contents, is in the file run_log.txt.

Generating the local build (without docker):

```bash
  $ make build
```

## Author

👤 **Ernani Britto** 

https://github.com/ernanibmurtinho