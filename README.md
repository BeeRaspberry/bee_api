# bee_api
![Bee Web Icon](images/beewhitecrosshatch.jpg)

![GitHub issues](https://img.shields.io/github/issues/BeeRaspberry/bee_api?style=flat-square)
![build](https://github.com/BeeRaspberry/bee_api/workflows/build/badge.svg?branch=master)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/7dcc779f81d0483d93f0e7c1c5a735e6)](https://www.codacy.com/gh/BeeRaspberry/bee_api?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=BeeRaspberry/bee_api&amp;utm_campaign=Badge_Grade)
[![Codacy Badge](https://api.codacy.com/project/badge/Coverage/7dcc779f81d0483d93f0e7c1c5a735e6)](https://www.codacy.com/gh/BeeRaspberry/bee_api?utm_source=github.com&utm_medium=referral&utm_content=BeeRaspberry/bee_api&utm_campaign=Badge_Coverage)

This repo provides the API backend for the web front-end. 

## Usage 

The following assumes you're using `sqlite` for your database.

### Running Locally

-   create a virtualenv
-   run ```pip install -r requirements.txt```
-   if using Windows, run ```set FLASK_APP=main.py```, else ```export FLASK_APP=main.py```
-   run ```flask run```

You should be able to access the `graphql` console via `http://127.0.0.1:5000`

### Running a Docker container

If you plan on persisting data between runs then you need to create a Docker volume, and mount it within the container.

-   create a Docker volume, `docker volume create {volume name}`. For example, `docker volume create sqlite_data`.
-   build the container, `docker build -t {tag name} .`. For example: `docker build -t bee_api:latest .`
-   run the container, `docker run -d -v {source volume}:/{target name} -p 127.0.0.1:5001:5000 -e "CONFIG_SETTINGS=config.ProductionConfig" -e "DATABASE_DIR={database location}" {tag name}`. For example: `docker run -d -v sqlite_data:/data -e "CONFIG_SETTINGS=config.ProductionConfig" -p 127.0.0.1:5001:5000-e "DATABASE_DIR=/data" bee_api`.

### Flask Options 

Two additional, `flask` commands exist for prepping the database. 

-   `initdb` creates the table schema for the application. Shouldn't be needed.
-   `seed` populates the database with data found in the directory specified. Usage: `flask seed {load files directory}`. It's not intended to do updates, only initial data load.

## Deploying using Helm
### Local Helm Chart
`helm install helm-charts/bee-api`

### Github Pages Repo
Add the repo
`helm repo add <repo name> https://beeraspberry.github.io/bee_api/`
Install
`helm install <repo name>/bee-api`

## Troubleshooting

If the system reports 
```
Usage: flask [OPTIONS] COMMAND [ARGS]...
Try "flask --help" for help.

Error: No such command "command".
```
when executing some commands then confirm you set `FLASK_APP` to the proper executable.


