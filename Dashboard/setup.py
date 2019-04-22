#!/usr/bin/env python3
import errno
import os
import subprocess
import sys
dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)
print("")
print("##############################")
print("#                            #")
print("#    EDVS Dashboard Setup    #")
print("#                            #")
print("##############################")
print("")

# Check if current system is linux-based
if sys.platform != "linux":
    print("EDVS Dashboard is developed for Linux distributions only.")
    print("The setup will now exit.")
    exit(1)

# Install required software
print("Installing Node.js and NPM...")
subprocess.run(["sudo", "apt", "update"])
subprocess.run(["sudo", "apt", "install", "-y", "nodejs", "npm"])
subprocess.run(["sudo", "npm", "install"])

# Setup MongoDB
is_db_local = input("\nWould you like to install MongoDB on this computer too? (y/n)")
mongodb_url = ""
if is_db_local != "y" and is_db_local != "n":
    while is_db_local != "y" and is_db_local != "n":
        is_db_local = input("Please enter 'y' for yes or 'n' for no: ")
if is_db_local == "y":
    print("Installing MongoDB...")
    subprocess.run(["sudo", "apt", "install", "-y", "mongodb"])
    mongodb_url = "mongodb://localhost:27017/dashboard"
elif is_db_local == "n":
    mongodb_url = input("In that case, please enter the URL for the MongoDB server:")

# Setup .env (environment variable) for Node.js server
admin_token = bytes.hex(os.urandom(12))
dotenv_example = open("env.example", "r")
dotenv = ""
for line in dotenv_example:
    if "DASHBOARD_DATABASE_URL" in line:
        line = "DASHBOARD_DATABASE_URL=" + mongodb_url + "\n"
    elif "DASHBOARD_SESSION_SECRET" in line:
        line = "DASHBOARD_SESSION_SECRET=" + bytes.hex(os.urandom(12)) + "\n"
    elif "DASHBOARD_ADMIN_TOKEN" in line:
        line = "DASHBOARD_ADMIN_TOKEN=" + admin_token + "\n"
    elif "ADMIN_TOKEN" in line:
        line = "ADMIN_TOKEN=" + admin_token + "\n"
    dotenv = dotenv + line
open(".env", "w").write(dotenv)

# init scripts
initdScript = """#!/bin/sh

APP_NAME="EdvsDashboard"
USER="root"
GROUP="$USER"
APP_DIR="~path~"
NODE_APP="server.js"
KWARGS=""
PID_DIR="$APP_DIR/pid"
PID_FILE="$PID_DIR/$APP_NAME.pid"
LOG_DIR="$APP_DIR/log"
LOG_FILE="$LOG_DIR/$APP_NAME.log"
NODE_EXEC=$(which node)

###############

# REDHAT chkconfig header

# chkconfig: - 58 74
# description: node-app is the script for starting a node app on boot.
### BEGIN INIT INFO
# Provides: node
# Required-Start:    $network $remote_fs $local_fs
# Required-Stop:     $network $remote_fs $local_fs
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: start and stop node
# Description: Node process for app
### END INIT INFO

###############

USAGE="Usage: $0 {start|stop|restart|status} [--force]"
FORCE_OP=false

if [ "$(id -u)" != "0" ]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi

pid_file_exists() {
    [ -f "$PID_FILE" ]
}

get_pid() {
    echo "$(cat "$PID_FILE")"
}

is_running() {
    PID="$(get_pid)"
    [ -d /proc/$PID ]
}

start_it() {
    mkdir -p "$PID_DIR"
    chown $USER:$GROUP "$PID_DIR"
    mkdir -p "$LOG_DIR"
    chown $USER:$GROUP "$LOG_DIR"

    echo "Starting $APP_NAME ..."
    echo "cd $APP_DIR
        if [ $? -ne 0 ]; then
          exit
        fi
        set -a
        sudo $NODE_EXEC \"$APP_DIR\"/$NODE_APP $KWARGS &> \"$LOG_FILE\" &
        echo \$! > $PID_FILE" | sudo -i -u $USER
    echo "$APP_NAME started with pid $(get_pid)"
}

stop_process() {
    PID=$(get_pid)
    echo "Killing process $PID"
    kill $PID
    wait $PID 2>/dev/null
}

remove_pid_file() {
    echo "Removing pid file"
    rm -f "$PID_FILE"
}

start_app() {
    if pid_file_exists
    then
        if is_running
        then
            PID=$(get_pid)
            echo "$APP_NAME already running with pid $PID"
            exit 1
        else
            echo "$APP_NAME stopped, but pid file exists"
            echo "Forcing start anyways"
            remove_pid_file
            start_it
        fi
    else
        start_it
    fi
}

stop_app() {
    if pid_file_exists
    then
        if is_running
        then
            echo "Stopping $APP_NAME ..."
            stop_process
            remove_pid_file
            echo "$APP_NAME stopped"
        else
            echo "$APP_NAME already stopped, but pid file exists"
            if [ $FORCE_OP = true ]
            then
                echo "Forcing stop anyways ..."
                remove_pid_file
                echo "$APP_NAME stopped"
            else
                exit 1
            fi
        fi
    else
        echo "$APP_NAME already stopped, pid file does not exist"
        exit 1
    fi
}

status_app() {
    if pid_file_exists
    then
        if is_running
        then
            PID=$(get_pid)
            echo "$APP_NAME running with pid $PID"
        else
            echo "$APP_NAME stopped, but pid file exists"
        fi
    else
        echo "$APP_NAME stopped"
    fi
}

case "$2" in
    --force)
        FORCE_OP=true
    ;;

    "")
    ;;

    *)
        echo $USAGE
        exit 1
    ;;
esac

case "$1" in
    start)
        start_app
    ;;

    stop)
        stop_app
    ;;

    restart)
        stop_app
        start_app
    ;;

    status)
        status_app
    ;;

    *)
        echo $USAGE
        exit 1
    ;;
esac"""
initdScript = initdScript.replace("~path~", dir_path)
initdScriptLocation = "/etc/init.d/EdvsDashboard"
try:
    initdScriptFile = open(initdScriptLocation, "w")
    initdScriptFile.write(initdScript)
    initdScriptFile.close()
except IOError as e:
    if (e[0] == errno.EPERM):
        print("Error run as root")
        sys.exit(1)
os.system("sudo chmod 755 " + initdScriptLocation)
os.system("sudo chown root:root " + initdScriptLocation)
os.system("sudo update-rc.d " + initdScriptLocation.split("/")[-1] + " defaults")
os.system("sudo " + initdScriptLocation + " start")
print("USAGE: sudo /etc/init.d/EdvsDashboard (start|stop|restart|status)")
print("ADMIN_TOKEN=" + admin_token)
