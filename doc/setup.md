# DEEPi Array Set Up #


## Pre-requisites ##

 - Raspberry Pi Imager
 - Internet connected hotspot
 
## RPi4 Array Controller ##

1. Set up uSD card using Raspberry Pi Imager using the RASPBERRY PI OS LITE (64 bit). 

 - Hostname: raspberrypi
 - Enable SSH
	 - Use password authentification
 - Set username and password
	 - username: pi
	 - password: raspberry
 - Configure wireless LAN
     - SSID: DEEPiNet
     - password: deepinet
     - Wireless LAN country: US
 - Set locale settings
	 - time zone: Etc/UTC
	 - keyboard layout: us
	 
	 
3. Plug in card into RPi4 and give time to boot up. 

4. Log onto the RPi4 using SSH with username and password

```.bash
ssh pi@raspberrypi.local

```

5. Set up via `sudo raspi-config`

    1. Enable Legacy Camera
    2. Expand filesystem


6. Follow directions on https://github.com/URIL-Group/deepi-setup for
   a basic DEEPi set up. 

7. Add RPiZ Nodes as ethernet devices

```
# /etc/udev/rules.d/90-usbpi.rules
SUBSYSTEM=="net", ATTR{address}=="00:22:82:ff:ff:01", NAME="usb1"
SUBSYSTEM=="net", ATTR{address}=="00:22:82:ff:ff:02", NAME="usb2"
SUBSYSTEM=="net", ATTR{address}=="00:22:82:ff:ff:03", NAME="usb3"
SUBSYSTEM=="net", ATTR{address}=="00:22:82:ff:ff:04", NAME="usb4"
```

8. Set up interfaces for static IP addresses on seperate subnets by
   adding the following to the bottom of `/etc/dhcpcd.conf`.
   
```
interface usb1
static ip_address=10.0.11.1/24
	
interface usb2
static ip_address=10.0.12.1/24
	
interface usb3
static ip_address=10.0.13.1/24

interface usb4
static ip_address=10.0.14.1/24
```

9. Set up IP forwarding

```.bash
sudo sysctl -w net.ipv4.ip_forward=1
```

Check if active w/ `sudo systemctl status sysctl` and start if not
active. TODO: check this



10. Set up IP routing table

```
# /lib/dhcpcd/dhcpcd-hooks/40-route
ip route replace 169.254.0.0/16 dev eth0
ip route replace 10.0.11.0/24 dev usb1
ip route replace 10.0.12.0/24 dev usb2
ip route replace 10.0.13.0/24 dev usb3
ip route replace 10.0.14.0/24 dev usb4
```


```
sudo sh /lib/dhcpcd/dhcpcd-run-hooks
sudo apt-get install iptables-persistent
```

FIXME: need to do this after connecting everything


On install `iptables-persistent` will ask if you want to keep the
current routing table. Say 'yes'.

10. Set up useful networking


```
# /etc/wpa_supplicant/wpa_supplicant.conf
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=US

network={
        ssid="DEEPiNet"
        scan_ssid=1
        psk="deepinet"
        key_mgmt=WPA-PSK
}

network={
        ssid="Fios-Q3Qj9"
        psk="army27fob449mop"
}

network={
        ssid="BIOS"
        psk="Welcome2BIOS"
}
```

11. Set up timesync

```
sudo apt-get install chrony
```

Add to the end of `/etc/chrony/chrony.conf`.

```
server 127.127.1.0
allow
local
```

Restart the service.

```
sudo systemctl daemon-reload
sudo systemctl restart chronyd
```

Check sources with `chronyc sources -v`

Check clients with `sudo chronyc clients`.
	 
## RPiZ Array Nodes ##

> Run through this process for each Wherever {N} appears replace with
> with 1,2,3,4

1. Set up uSD card using Raspberry Pi Imager using the RASPBERRY PI OS LITE (32 bit). 


 - Hostname: deepi{N}
 - Enable SSH
	 - Use password authentification
 - Set username and password
	 - username: deepi{n}
	 - password: raspberry
 - Configure wireless LAN
     - SSID: DEEPiNet
     - password: deepinet
     - Wireless LAN country: US
 - Set locale settings
	 - time zone: Etc/UTC
	 - keyboard layout: us


3. Plug in card into RPi4 and give time to boot up. 

4. Log onto the RPi4 using SSH with username and password

```.bash
ssh pi@deepi{N}.local

```

5. Set up via `sudo raspi-config`

    1. Enable Legacy Camera
    2. Expand filesystem


6. Follow directions on https://github.com/URIL-Group/deepi-setup for
   a basic DEEPi set up. 

7. Set up ethernet over USB networking for each node.

```.bash
sudo sed -i 's/rootwait/rootwait modules-load=dwc2,g_ether g_ether.host_addr=00:22:82:ff:ff:0{N} g_ether.dev_addr=00:22:82:ff:ff:1{N}/' /boot/cmdline.txt
echo "dtoverlay=dwc2" | sudo tee -a /boot/config.txt
```

8. Set static IP and allow hotplug

```
# /etc/network/interfaces.d/usb0
allow-hotplug usb0
iface usb0 inet static
address 10.0.1{N}.2
netmask 255.255.255.0
network 10.0.1{N}.01
broadcast 10.0.1{N}.255
gateway 10.0.1{N}.1
```

9. Set up IP routing table

```
# /lib/dhcpcd/dhcpcd-hooks/40-route
ip route replace 10.0/16 dev usb0
ip route replace 169.254/16 dev usb0 via 10.0.1{N}.1 metric 101
```

```
sudo sh /lib/dhcpcd/dhcpcd-run-hooks
sudo apt-get install iptables-persistent
```

On install `iptables-persistent` will ask if you want to keep the
current routing table. Say 'yes'.

10. Set up useful networking


```
# /etc/wpa_supplicant/wpa_supplicant.conf
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=US

network={
        ssid="DEEPiNet"
        scan_ssid=1
        psk="deepinet"
        key_mgmt=WPA-PSK
}

network={
        ssid="Fios-Q3Qj9"
        psk="army27fob449mop"
}

network={
        ssid="BIOS"
        psk="Welcome2BIOS"
}
```

11. Set up time sync

Open `/etc/systemd/timesyncd.conf` and after `[Time]` add

```
NTP=10.0.1{N}.1
```

Then restart and check status

```
sudo apt-get install systemd-timesyncd
sudo systemctl daemon-reload
sudo systemctl restart systemd-timesyncd
sudo systemctl status systemd-timesyncd 
```

To check if it is working, use `timedatectl show-timesync`

## Controller Software Set Up ##

1. Move executables to `/usr/local/bin` and `/usr/local/sbin`
   respectively.
   
   
2. Add a call to `@reboot resethub` to crontab using `sudo crontab
   -e`.

### Set up parallel ssh ###

1. Set up passwordless ssh
  
```
ssh-keygen # accept all defaults
ssh-copy-id -i .ssh/id_rsa.pub pi@10.0.11.2
ssh-copy-id -i .ssh/id_rsa.pub pi@10.0.12.2
ssh-copy-id -i .ssh/id_rsa.pub pi@10.0.13.2
ssh-copy-id -i .ssh/id_rsa.pub pi@10.0.14.2
```

2. Set up parallel ssh

```
sudo apt-get install pssh
python -m pip install parallel-ssh
```

Create a hosts file

```
# ~/hosts.txt
pi@10.0.11.2:22
pi@10.0.12.2:22
pi@10.0.13.2:22
pi@10.0.14.2:22
```


  * TODO: impliment logging (on each rpi)
  * TODO: what are the most important standard logs
  * TODO: NTP server

### Set up controller script ###

1. `resethub`
2. Check connections in someway
3. 
