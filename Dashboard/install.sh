#!/bin/bash

# Change to current directory.
cd "$(dirname "$0")"

# Check if running in a supported Linux distro.
if grep -qE "(Microsoft|WSL)" /proc/version &> /dev/null ; then
    echo "Sorry, EDVS Dashboard does not support WSL(Windows Subsystem for Linux) yet."
    echo "For more details on supported platforms, see project README."
    exit 1
fi
if [ "$(uname)" ">" "MINGW" -a "$(uname)" "<" "MINGX" ] ; then
    echo "Sorry, EDVS Dashboard does not support MinGW(Minimalist GNU for Windows) yet."
    echo "For more details on supported platforms, see project README."
    exit 1
fi
if [ "$(uname)" = "Darwin" ] ; then
    echo "Sorry, EDVS Dashboard does not support MacOS/OS X yet."
    echo "For more details on supported platforms, see project README."
    exit 1
fi
if [ "$(uname)" != "Linux" ] ; then
    echo "Sorry, this OS is not supported yet."
    echo "For more details on supported platforms, see project README."
    exit 1
fi

# If ran with -all argument, then install Node.js and MongoDB first.
case $1 in
    -a | --all)
        ./install-nodejs.sh
        ./install-mongodb.sh
        ;;
    *)
        echo "Invalid argument."
        exit 1
        ;;
esac

echo ""
echo "##############################"
echo "#                            #"
echo "#    EDVS Dashboard Setup    #"
echo "#                            #"
echo "##############################"
echo ""

# Check for supported Node.js
if which node > /dev/null ; then
    echo "Node.js is found."
    if /usr/bin/env node -v | grep -E "(v8|v10)" &> /dev/null ; then
        /usr/bin/env node -v
        echo ""
        else
            echo "Current Node.js version is not compatible with EDVS Dashboard."
            echo "You can install Node.js by running:"
            echo ""
            echo "    curl -sL https://deb.nodesource.com/setup_10.x | sudo -E bash -"
            echo "    sudo apt-get install -y nodejs"
            echo ""
            echo "or by running \"./install-nodejs.sh\"."
            echo "or by re-running this script with \"-all\" argument to install them first."
            echo ""
            echo "Please install a newer version of Node.js and re-run this script."
            echo "The installer will now exit."
            exit 1
    fi
    else
        echo "Node.js is not found."
        echo "You can install Node.js by running:"
        echo ""
        echo "    curl -sL https://deb.nodesource.com/setup_10.x | sudo -E bash -"
        echo "    sudo apt-get install -y nodejs"
        echo ""
        echo "or by running \"./install-nodejs.sh\"."
        echo "or by re-running this script with \"-all\" argument to install them first."
        echo ""
        echo "Please install a compatible Node.js and re-run this script."
        echo "The installer will now exit."
        exit 1
fi

# Check for supported MongoDB
MONGODB_URI=""
while true; do
    read -p "Will the MongoDB database be on this server too (y/n)? " -n 1 -r
    echo ""
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]] ; then
        if systemctl is-active mongod | grep -qE "(inactive)" &> /dev/null ; then
            echo "A running MongoDB is not found on this server,"
            echo "Either it is not installed, or it is installed but mongod daemon is not started."
            echo "You can install MongoDB by running:"
            echo ""
            echo "    sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 9DA31620334BD75D9DCB49F368818C72E52529D4"
            echo "    echo "deb [ arch=amd64 ] https://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/4.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.0.list"
            echo "    sudo apt-get update"
            echo "    sudo apt-get install -y mongodb-org"
            echo "    sudo service mongod start"
            echo ""
            echo "or by running \"./install-mongodb.sh\"."
            echo "or by re-running this script with \"-all\" argument to install them first."
            echo "Please re-run this script after installation."
            echo "The installer will now exit."
            exit 1
            else
                MONGODB_URI="mongodb://localhost:27017/dashboard"
        fi
        break
    fi
    if [[ $REPLY =~ ^[Nn]$ ]] ; then
        read -p "In that case, please enter an URI for the MongoDB server: " MONGODB_URI
        break
    fi
    echo "Invalid input, please enter again."
done

# Modify .env file.
./bin/edvs-dashboard set DASHBOARD_DATABASE_URL="$MONGODB_URI"

# Install node_modules
npm install -g
