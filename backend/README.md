# Battlecode Backend API

Written in Django Rest Framework. Based on `battlecode19/api`.

## Local Development

You can run `docker-compose up --build` in the root directory of `battlecode20` to run the entire website stack. If for some reason you want to run Django outside of Docker, follow the instructions below.

For a nice interface to test the backend, go to `localhost:8000/docs/`.

### First-Time Setup

#### Virtual Environment

Create a virtual environment by following the instructions below.

- `pip3 install virtualenv` (or `pip` if your default Python installation is 3)
- `virtualenv venv -p python3`
- `source venv/bin/activate`
- `pip install -r requirements.txt` (`pip3` is not necessary since the default Python version within the virtualenv is 3)

It would be good, sometime, to fix `psycopg2` at 2.7.7. Unfortunately, deploy seems to fail. But, this would prevents a bug, in which `psycopg2` requires a working build environmment for the included C code.

If you still have this bug: On Mac, [this StackOverflow answer has a solution](https://stackoverflow.com/a/39800677/3767728) (command should be `env LDFLAGS="-I/usr/local/opt/openssl/include -L/usr/local/opt/openssl/lib" pip install psycopg2==2.8.3 --upgrade`) (if you still have problems with psycopg2 on mac after this, try `brew reinstall openssl` and `brew install postgresql`)

#### Database

Any time you start the backend, there must be a Postgres instance up on `localhost:5432` (or whatever credentials are used in `battlecode/dev_settings.py`) with a database named `battlecode`. It is easy to run Postgres in [Docker](https://docs.docker.com/install/):

```
docker run -p 5432:5432 -e POSTGRES_USER=battlecode -e POSTGRES_PASSWORD=mysecretpassword -e POSTGRES_DB=battlecode --name bc20db -d postgres
```

To stop or start the database container: `docker stop bc20db` `docker start bc20db`. [Postico](https://eggerapps.at/postico/) and [pgAdmin](https://www.pgadmin.org/) are two useful tools for managing the database.

#### Migrations

Run the following to set up the database:

```
python manage.py migrate
```

This must be run the first time the database is setup, or anytime models are changed. When models are changed, you also need to run `python manage.py makemigrations` and then commit the migrations. If run through docker-compose, you need to first `docker exec -it battlecode20_backend_1 /bin/bash` and then perform the `python manage.py makemigrations`.

This will automatically create a new league with league ID 0. This is something we might want to change in the future, if we decide to make use of the multiple leagues.

### Running

Make sure you work in your virtual environment, make sure all packages are up to date, start the database, and set the necessary environment variables (only needed once per terminal session):

```
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
docker start bc20db
export DJANGO_SETTINGS_MODULE="dev_settings"
export EMAIL_PASS="passwordtobattlecodegmail"
```

Then, start the server:

```
python manage.py runserver
```

The backend should now be running on `localhost:8000`. You can open [http://localhost:8000/docs](http://localhost:8000/docs) in your browser to verify that it works.

You can also test with uWSGI (which is what is used in production) by running `uwsgi --ini uwsgi-dev.ini`.

### Testing

`coverage run --source='.' manage.py test`
`coverage report`

To use the Python debugger: `from nose.tools import set_trace; set_trace()` (Note that Nose breaks the regular pdb.)

### Installing Packages

Django 2.0.3 and Webpack 4.0.1 are both very recently released. You may run into backwards compatibility issues with 3rd party packages, or deprecated functions. Try to refer to the most up-to-date documentation when possible. You may also run into problems if i.e. you have different version node modules installed globally instead of locally.

When installing a new Python package:
`pip install <package>`
`pip freeze > requirements.txt`

Always commit the most recent `requirements.txt`.


## Deployment

#### Steps

1. Push to master.
2. Go to [Cloud Build Triggers](https://console.cloud.google.com/cloud-build/triggers?project=battlecode18) on Google Cloud.
3. Click "Run trigger" under the `battlecode/battlecode20` trigger.
4. Go to [Cloud Build History](https://console.cloud.google.com/cloud-build/builds?project=battlecode18). You should see a spinning blue icon next to a recently started build, which should reference the most recent commit ID on master on this repo. Wait until the spinning icon turns into a green checkmark (this usually takes 2-3 minutes).
5. Go to the [battlecode20-backend-true](https://console.cloud.google.com/compute/instanceGroups/details/us-east1-b/battlecode20-backend-true?project=battlecode18) instance group in the Compute Engine. Press `Rolling Restart/Replace`.
6. Change operation from `Restart` to `Replace`. Let maximum surge be 1 and **maximum unavailable be 0** (we don't want our server to go down).
7. Wait until all spinning blue icons have turned into green checkmarks (this takes like 10 minutes I think).

This procedure is currently very long and requires too much manual intervention. We should write a script that does all of this for us (which shouldn't be too hard).

#### Setup

A database should be created.

We currently have continuous builds triggered by pushes to master. Therefore, make sure that everything is actually working before pushing. Also, make sure that any new database migrations are also applied to the production server before deploying. A good way to ensure this is to always test locally with the production database, before committing and pushing to master.

The images are then deployed as an instance group on GCE. To update the instances to use the newly built image, perform a rolling update of the instance group.

Pls pls use SHA256 digests in the `Dockerfile`. Otherwise, the image might be rebuilt, from the same commit tag as before, but not working anymore (this happened, and it was not fun).

Ideally, we would like to move to Kubernetes for everything, as that would make everything much easier, but it doesn't currently support having a load balancer that also points to storage buckets. This is a deal-breaker, since the frontend is static.
