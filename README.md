# Gatekeeper project

This is the starwars gatekeeper fw, programmed as a fun-internal deepsea project

To run it like a service an dedicated file was added here. This file must me copied in /etc/systemd/system as root with: 

>> sudo cp gatekeeper.service /etc/systemd/system/gatekeeper.service

Once the file has been copied, it must inform to systemd that a new service has been added typing: 

>> sudo systemctl daemon-reload

Finally we must enable the start after boot daemon: 

>> sudo systemctl enable gatekeeper.service"

The rest of commands to manage the service are:

tostart the daemon: >> sudo systemctl start gatekeeper.service
to stop the daemon: >> sudo systemctl stop gatekeeper.service