# DEEPi Array #
> Instructions for setting up an array

## Overview ##
  

  
## RPiZ Nodes ##

1. Set up new RPiZ using Raspbian Pi OS lite and do the following from the
   [DEEPi-OS project](https://github.com/rshom/deepi-os).
   
> NOTE: currently, you have to use Buster over the newest version
> because the picamera python package does not work with
> Bullseye. Except a solution in the future.

```
git clone https://github.com/rshom/deepi-os
cd deepi-os
sudo sh ./setup.sh
sudo reboot now
```

2. Add Ethernet over USB networking to each node. The `X` values in
   the following commands must be replaced with a unique node number
   for each.

```
sudo sed -i 's/rootwait/rootwait modules-load=dwc2,g_ether g_ether.host_addr=00:22:82:ff:ff:0X g_ether.dev_addr=00:22:82:ff:ff:1X/' /boot/cmdline.txt
echo "dtoverlay=dwc2" | sudo tee -a /boot/config.txt
```

Set static IP and allow hotplug

```
# /etc/network/interfaces.d/usb0
allow-hotplug usb0
iface usb0 inet static
address 10.0.1X.2
netmask 255.255.255.0
network 10.0.1X.01
broadcast 10.0.1X.255
gateway 10.0.1X.1
```

> NOTE: Need to use high quality USB cables. This needs to be
> quanitified or exampled in some way because it is more than just
> "good".

## Array RPi4 ##

1. Set up new RPi4 using Raspbian Pi OS and do the following from the
   [DEEPi-OS project](https://github.com/rshom/deepi-os).
   
> NOTE: currently, you have to use Buster over the newest version
> because the picamera python package does not work with Bullseye.

```
git clone https://github.com/rshom/deepi-os
cd deepi-os
sudo sh ./setup.sh
sudo reboot now
```

2. Add RPiZ Nodes as ethernet devices.

```
# /etc/udev/rules.d/90-usbpi.rules
SUBSYSTEM=="net", ATTR{address}=="00:22:82:ff:ff:01", NAME="eth1"
SUBSYSTEM=="net", ATTR{address}=="00:22:82:ff:ff:02", NAME="eth2"
SUBSYSTEM=="net", ATTR{address}=="00:22:82:ff:ff:03", NAME="eth3"
SUBSYSTEM=="net", ATTR{address}=="00:22:82:ff:ff:04", NAME="eth4"
```

3. Set the new interfaces to static ip addresses on seperate subnets
   by adding the following code to `/etc/dhcpcd.conf`.

```
interface eth1
static ip_address=10.0.11.1/24
	
interface eth2
static ip_address=10.0.12.1/24
	
interface eth3
static ip_address=10.0.13.1/24

interface eth4
static ip_address=10.0.14.1/24
```

4. Add IP forwarding by modifying `/etc/sysctl.conf` and uncomment line.

```
net.ipv4.ip_forward=1
```

or run

```
sudo sysctl net.ipv4.ip_forward=1
```

## Router ##

> TODO: try to get router to forward IP

## Topside RPi4 ##

1. Set up new RPi4 using Raspbian Pi OS.

2. Add IP forwarding

https://learn.sparkfun.com/tutorials/setting-up-a-raspberry-pi-3-as-an-access-point/enable-packet-forwarding

https://forums.raspberrypi.com/viewtopic.php?t=170206

https://raspberrypi.stackexchange.com/questions/120387/pass-traffic-from-one-network-interface-to-another/120398#120398



## References ##

  * http://raspberryjamberlin.de/zero360-part-2-connecting-via-otg-a-cluster-of-raspberry-pi-zeros-to-a-pi-3/

