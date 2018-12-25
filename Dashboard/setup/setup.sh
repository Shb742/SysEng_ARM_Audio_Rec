sudo apt update ; sudo apt install -y mongodb ; sudo systemctl status mongodb ; mongo --eval 'db.runCommand({ connectionStatus: 1 })'; #set up mongodb
npm install;