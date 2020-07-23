# Installation on Debian

Install the following packages:
- python3-serial
- python3-paho-mqtt

Then git clone this repository to **/opt/arduino-sensors-toolkit**.

Create the *serial2mqtt* system user and add it to the *dialout* group to read the serial interface:
```
# adduser --system --disabled-password --disabled-login --home /var/lib/serial2mqtt \
    --no-create-home --quiet --force-badname --group serial2mqtt
# usermod -a -G dialout serial2mqtt
```

Copy the [serial2mqtt.service](serial2mqtt.service) file to **/etc/systemd/system/serial2mqtt.service**.

Copy the [serial2mqtt.default](serial2mqtt.default) file to **/etc/default/serial2mqtt**.

Reload systemd configuration with `systemctl daemon-reload`.

Enable service with `systemctl enable serial2mqtt.service`.
