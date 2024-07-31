# 👷🏽‍♂️ CRM System for Building and Reviewing Employees' Reports

This project allows supervision of employees by adding them to the system via the admin panel, which is secured by the authentication system, using internally issued tokens, and monitoring their work efficiency by reviewing their formed reports, which consist of affixed images, an employee description of the completed work, and the facility information where the work was carried out. Moreover, the system is capable of external integration, as it has API.

# 🔧 Project Installation

## 1. Clone Git Repository 
```.sh
git clone <https://.git>
```
## 2. Create `.env` file 
2.1 Create `.env` file in the cloned repository:
```.sh
touch .env
```
2.2 Open `.env-example` and copy all the contents present to `.env`.

2.3 To boot up the telegram bot, you have to own a token, which can be acquired via [@BotFather](t.me/BotFather). Change `TOKEN` variable to the API key which was provided and `BOT_NAME` to the username of your bot.

2.4 To ensure the application launches, you need to fill in only `PASSWORD` variable for the admin panel password. `LOGIN` is set to `admin` by default, but if you want to change it, then you either should edit `LOGIN` variable in the `config.py`, or remove it and then list it in `.env`.

## 3. Launch Application
To launch the app, you have to have `docker` and `docker compose` installed, be it Docker-Desktop for OS X or Windows or the shell-based app for Linux.

3.1 Build the containers
```.sh
docker-compose -f docker-compose.yaml build
```
3.2 Run the just built containers
```.sh
docker-compose -f docker-compose.yaml up
```
Beware, if alembic container exits with code 1 on your first run, then you should just terminate upping of the containers by pressing `Ctrl + C` and repeating step 3.2.

# ⭐️ Feedback

[![](https://img.shields.io/badge/Issues-red)](https://github.com/complicat9d/building-report-crm/issues)

If you found this project helpful to you, then subscribe to my github account and star this repo, that motivates me to make better projects and improve this one.

