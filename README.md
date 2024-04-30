# Gatekeeper project

This is the starwars gatekeeper fw, programmed as a fun-internal deepsea project.

Is develop under raspberry OS and a raspberry pi 5, due that the GPIOs only work with the new architecture (a dedicated external chip instead the proper broadcom uc). Can be ported to raspberry pi 4 and below but need to change the led and buttons APIs to the old input/outputs syntax.

To run it like a service an dedicated file was added here. This file must me copied in /etc/systemd/system as root with: 

```sudo cp gatekeeper.service /etc/systemd/system/gatekeeper.service```

Once the file has been copied, it must inform to systemd that a new service has been added typing: 

```sudo systemctl daemon-reload```

Finally we must enable the start after boot daemon: 

```sudo systemctl enable gatekeeper.service```

The rest of commands to manage the service are:

to start the daemon: ```sudo systemctl start gatekeeper.service```

to stop the daemon: ```sudo systemctl stop gatekeeper.service```