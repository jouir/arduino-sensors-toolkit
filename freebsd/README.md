# Installation on FreeBSD

Install the following packages:
- py37-pyserial
- py37-paho-mqtt

Then git clone this repository to **/usr/local/share/arduino-sensors-toolkit**.

Create the system user:

```
pw user add -n serial2mqtt -s /usr/sbin/nologin -G dialer
```

Copy [serial2mqtt.rc](serial2mqtt.rc) script to **/usr/local/etc/rc.d/serial2mqtt**.

Enable service:
```
echo 'serial2mqtt_enable="YES"' >> /etc/rc.conf
```
