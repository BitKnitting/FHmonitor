Raspberry Pi Setup
==================
We use a `Raspberry Pi 3 Model B+ <https://www.adafruit.com/product/3055>`_.

Installation
------------
Our instructions assume a Mac is being used.

- Put the micro-SD e.g.: `cheap one on Amazon <https://www.amazon.com/gp/product/B004ZIENBA/ref=as_li_ss_tl?ie=UTF8&psc=1&linkCode=sl1&tag=bitknittingwo-20&linkId=923f12067ad3395ed04f043c37d8c39f>`_
  that will hold the Rasp Pi image into an SD Card reader (on our Mac).
- Format using SD-Formatter.
- Download a `Rasp Pi image <https://www.raspberrypi.org/downloads/raspbian/>`_.
  `Note: We use the Lite image.`
- Run Etcher to copy the image onto the SD Card.
- Open a terminal window and cd into the boot drive.  For us this was `cd /Volumes/boot`.
- Add "SSH" file to the root of the image.  We do this by opening a terminal on the boot partition and typing `$touch ssh`
- Create the `wpa_supplicant.conf` file : `$touch wpa_supplicant.conf`.  Copy the contents into the file `nano wpa_supplicant.conf`:
```
country=US
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1

network={
    ssid="YOURSSID"
    psk="YOURPWD"
}

```
_Note: Multiple wifi networks can be set up by following [this example](https://www.raspberrypi.org/documentation/configuration/wireless/wireless-cli.md)_:

```
network={
    ssid="SchoolNetworkSSID"
    psk="passwordSchool"
    id_str="school"
}

network={
    ssid="HomeNetworkSSID"
    psk="passwordHome"
    id_str="home"
}
```

Changing the ssid and psk to match your network.
- 'safely' remove the SD-card.
- Put the SD-card into the Rasp-Pi's micro-SD port
- Power up the Rasp Pi.  Hopefully wireless is working!

Put the microSD card into the Rasp Pi and boot it up.  Our next step is to figure out it's IP address.

