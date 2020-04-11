# Battlecode 2020

🍜

## Repository Structure

- `/backend`: Backend API in Django Rest Framework
- `/frontend`: Frontend dashboard in React
- `/engine`: Game engine in Java
- `/schema`: Game serialization schema (basically, an encoding of all units and events in a game)
- `/client`: Game client (visualizer and playback) in TypeScript
- `/example-bots`: A bunch of example bots for the game!

## Development

### Website

To get set up, make sure you have [Node](https://nodejs.org/en/download/) and [Docker](https://docs.docker.com/docker-for-mac/install/) installed. For Windows, you will need Docker Toolbox. If you have Windows, I'd also recommend installing [Cygwin](https://www.cygwin.com/), since we have some bash scripts that won't work with the standard Windows command prompt. (Docker is not strictly necessary, but it makes stuff easier, especially if you want to work on the backend of the website.)

First, install all required packages: run `./install_frontend.sh` in the main folder. (If this fails, run `npm install` in each of the four folders `/schema`, `/client/playback`, `/client/visualizer`, `/frontend`.)

Then, you can start the frontend by running `npm run start` in the `/frontend` folder. (If this fails on Windows, make sure you are using Cygwin.) After this step, you should be able to view the website at http://localhost:3000.

If you also want to run the backend (which will enable things like signing in to the website, and a rankings table, etc) then run `docker-compose -f docker-compose-b.yml up --build` in this folder. If you don't have Docker, you can try following the instructions in the `/backend` folder instead.

You can also run both the backend and the frontend in a Docker container, by running `docker-compose up --build`, but that might be slower.

### Engine

Windows users: Instead of `./gradlew`, use `gradlew` for all commands.

(whenever Gradle has problems with something, run `./gradlew clean` and see if it helps)

To run a game, run

```
./gradlew headless
```

The replay file will be in `/matches`. Use `headlessX` for bots that are in `battlecode20-internal-test-bots`. You can specify the robot code and map like this: `./gradlew headless -Pmaps=maptestsmall -PteamA=examplefuncsplayer -PteamB=examplefuncsplayer`.

### Client

(Make sure you have a recent version of `npm`: `sudo npm cache clean -f && sudo npm install -g n && sudo n stable && PATH="$PATH"`.)

First run `npm install` in the `schema` folder, followed by `npm run install_all` in the `client` folder. You can then run

```
npm run watch
```

which will launch the client on http://localhost:8080 (if available).

### Docs

You can generate javadocs as follows:

```
./gradlew release_docs_zip -Prelease_version=2020.0.0.0.0.1
```

This will create a `zip` file. Unzip and open the `index.html` file in it to view the docs. In particular, looking at the documentation for `RobotController` will be helpful.

## Notes for porting this to battlecode21

When Battlecode 2021 comes around, it will probably useful to reuse a fair amount of this codebase. Mainting git history is nice. Use `git-filter-repo` for this:
```
pip3 install git-filter-repo
```

Make sure you have a recent git version (run `git --version` and make sure it's compatible with git-filter-repo). The following steps were taken to port from `battlecode20` to this repo:

```
cd ..
git clone https://github.com/battlecode/battlecode20
cd battlecode20
git checkout -b battlecode20export
git filter-repo --path backend --path frontend --path infrastructure --path specs --path docker-compose-b.yml --path docker-compose.yml --path README.md --path pre_release.py --path post_release.py --tag-rename '':'bc20-'
cd ..
cd battlehack20
git pull ../battlecode20 —allow-unrelated-histories
```

Note that if you want to rename directories, that is also possible.
