import os
dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)
os.system("sudo apt install -y libatlas-base-dev python3 python3-dev python3-pip build-essential swig git libpulse-dev libasound2-dev python3-pyaudio sox")
os.system("sudo pip3 install -r requirements.txt")
env="""SERVER_URL=<server>
USERNAME=<user>
PASSWORD=<password>
LOCATION=<location>"""
env = env.replace("<server>",input("server address (eg - https://127.0.0.1) :")).replace("<user>",input("user name(eg - test) :")).replace("<password>",input("password(eg - test@test) :")).replace("<location>",input("location :"))

try:
    envFile = open(dir_path+"/.env","w")
    envFile.write(env)
    envFile.close()
except IOError as e:
    print(str(e))
    if (e[0] == errno.EPERM):
        print("Error run as root")
        sys.exit(1)

os.system("sudo apt install -y unzip; unzip rnnoise-master.zip;")
os.system("cd rnnoise-master; sudo ./autogen.sh;sudo ./configure; sudo make install;")
input("press enter to conitnue")

os.system("sudo chmod +x compile;")
os.system("./compile remove_noise.c")
input("press enter to conitnue")

os.system("tar -xvf pocketsphinx-5prealpha.tar; tar -xvf sphinxbase-5prealpha.tar; mv sphinxbase-5prealpha sphinxbase;")
os.system("cd sphinxbase; sudo ./autogen.sh; sudo ./configure; sudo make ; sudo make install")
os.system("cd pocketsphinx-5prealpha; sudo ./autogen.sh; sudo ./configure; sudo make clean all ; sudo make install")
os.system("sudo chmod +x callSpeechRec")
input("press enter to conitnue")



initdScript = """#!/bin/sh

APP_NAME="EDVS"
USER="root"
GROUP="$USER"
APP_DIR="~path~"
APP="callSpeechRec"
KWARGS=""
PID_DIR="$APP_DIR/pid"
PID_FILE="$PID_DIR/$APP_NAME.pid"
LOG_DIR="$APP_DIR/log"
LOG_FILE="$LOG_DIR/$APP_NAME.log"

###############

# REDHAT chkconfig header

# chkconfig: - 58 74
# description: app is the script for starting an app on boot.
### BEGIN INIT INFO
# Provides: node
# Required-Start:    $network $remote_fs $local_fs
# Required-Stop:     $network $remote_fs $local_fs
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: start and stop app
# Description: Process for app
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
        \"$APP_DIR\"/./$APP $KWARGS &> \"$LOG_FILE\" &
        echo \$! > $PID_FILE" | sudo -i -u $USER
    echo "$APP_NAME started with pid $(get_pid)"
}

stop_process() {
    PID=$(get_pid)
    echo "Killing process $PID"
    pkill -TERM -P $PID
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
initdScript = initdScript.replace("~path~",dir_path)
initdScriptLocation = "/etc/init.d/EDVS"
try:
    initdScriptFile = open(initdScriptLocation,"w")
    initdScriptFile.write(initdScript)
    initdScriptFile.close()
except IOError as e:
    if (e[0] == errno.EPERM):
        print("Error run as root")
        sys.exit(1)
os.system("sudo chmod 755 "+initdScriptLocation)
os.system("sudo chown root:root "+initdScriptLocation)
os.system("sudo update-rc.d "+initdScriptLocation.split("/")[-1]+" defaults")
print("Registered script with rc.d.....")
os.system("sudo "+initdScriptLocation+" start")
print("USAGE: sudo /etc/init.d/EDVS (start|stop|restart|status)")