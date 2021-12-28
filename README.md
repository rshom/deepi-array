# DEEPi Array #
> Instructions for setting up an array

## Overview ##

  * 4x RPiZ nodes
  * Array RPi4
  * Router
  * Topside RPi4
  
## RPiZ Nodes ##

1. Set up new RPiZ using Raspbian Pi OS lite and do the following from the
   [DEEPi-OS project](https://github.com/rshom/deepi-os).
   
> NOTE: currently, you have to use Buster over the newest version
> because the picamera python package does not work with Bullseye.

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
sudo sed 's/rootwait/rootwait modules-load=dwc2,g_ether g_ether.host_addr=00:22:82:ff:ff:0X g_ether.dev_addr=00:22:82:ff:ff:1X/' /boot/cmdline.txt
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
> quanitified or exampled in some way.

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

3. Add IP forwarding 

## Router ##

> TODO: try to get router to forward IP

## Topside RPi4 ##

1. Set up new RPi4 using Raspbian Pi OS.

2. Add IP forwarding

## References ##

  * http://raspberryjamberlin.de/zero360-part-2-connecting-via-otg-a-cluster-of-raspberry-pi-zeros-to-a-pi-3/

