# Gatekeeper project

This is the starwars gatekeeper fw, programmed as a fun-internal deepsea project.

Is develop under raspberry OS and a raspberry pi 5, due that the GPIOs only work with the new architecture (a dedicated external chip instead the proper broadcom uc). Can be ported to raspberry pi 4 and below but need to change the led and buttons APIs to the old input/outputs syntax.

# Requirements

The system can work with a Deepdeck keyboard (optional) to have remote control to move motors and take actions manually, to do that you´ll pair the devices by BLE. The deepdeck should be in `Media` layer to access to the arrow keys and move the desired axis with these buttons. 

So far the raspberry OS in the rasp-pi5 have some issues when try to reconnect automatically and the GUI BLE options doesn't work properly. Using hcitools can pair the device and update the BLE connection once start the system:

To connect the deepdeck follow this steps:

1. Get the BLE MAC to connect to it:
```sudo hcitool lescan```

2. Search for the `Ahuyama` device and copy its MAC

```
pi@raspberrypi:~ $ sudo hcitool lescan
LE Scan ...
C8:F0:9E:CE:29:7A Ahuyama
C8:F0:9E:CE:29:7A (unknown)
```

3. Create a new connection with the Deepdeck:

```sudo hcitool lecc C8:F0:9E:CE:29:7A```

if successfull then will show you a handler connection number

```
pi@raspberrypi:~ $ sudo hcitool lecc C8:F0:9E:CE:29:7A
Connection handle 65
```

4. Add the connection handler to the LE accept list:

```sudo hcitool lealadd C8:F0:9E:CE:29:7A```

```sudo hcitool lealadd 65```

Now you can start the application and use the deepdeck like remote controller

# Service configuration

To run it like a service an dedicated file was added here. This file must me copied in /etc/systemd/system as root with: 

```sudo cp gatekeeper.service /etc/systemd/system/gatekeeper.service```

Once the file has been copied, it must inform to systemd that a new service has been added typing: 

```sudo systemctl daemon-reload```

Finally we must enable the start after boot daemon: 

```sudo systemctl enable gatekeeper.service```

The rest of commands to manage the service are:

to start the daemon: ```sudo systemctl start gatekeeper.service```

to stop the daemon: ```sudo systemctl stop gatekeeper.service```