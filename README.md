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

3. Set static IP and allow hotplug

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

4. Set up ip routing table.

```
# /lib/dhcpcd/dhcpcd-hooks/40-route
ip route replace 192.168.8.0/24 dev usb0 via 10.0.1X.1
ip route replace 10.0.11.0/24 dev usb0 via 10.0.1X.1
ip route replace 10.0.12.0/24 dev usb0 via 10.0.1X.1
ip route replace 10.0.13.0/24 dev usb0 via 10.0.1X.1
ip route replace 10.0.14.0/24 dev usb0 via 10.0.1X.1
ip route replace default dev wlan0
```
> NOTE: IP routing order is from most to least specific.

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
SUBSYSTEM=="net", ATTR{address}=="00:22:82:ff:ff:01", NAME="usb1"
SUBSYSTEM=="net", ATTR{address}=="00:22:82:ff:ff:02", NAME="usb2"
SUBSYSTEM=="net", ATTR{address}=="00:22:82:ff:ff:03", NAME="usb3"
SUBSYSTEM=="net", ATTR{address}=="00:22:82:ff:ff:04", NAME="usb4"
```

3. Set the new interfaces to static ip addresses on seperate subnets
   by adding the following code to `/etc/dhcpcd.conf`.

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



4. Add IP forwarding 

5. Set up ip routing table.

```
# /lib/dhcpcd/dhcpcd-hooks/40-route
ip route replace 192.168.8.0/24 dev eth0
ip route replace 10.0.11.0/24 dev usb0
ip route replace 10.0.12.0/24 dev usb0
ip route replace 10.0.13.0/24 dev usb0
ip route replace 10.0.14.0/24 dev usb0
ip route replace default dev wlan0
```

## Router ##


  * [ ] Plug into a travel router. 
  * [ ] Set up static IPs


## Topside RPi4 ##

1. Set up new RPi4 using Raspbian Pi OS.

2. Add IP forwarding

5. Set up ip routing table.

```
# /lib/dhcpcd/dhcpcd-hooks/40-route
ip route replace 192.168.8.0/24 dev eth0
ip route replace 10.0.11.0/24 via 192.168.8.111
ip route replace 10.0.12.0/24 via 192.168.8.111
ip route replace 10.0.13.0/24 via 192.168.8.111
ip route replace 10.0.14.0/24 via 192.168.8.111
ip route replace default dev wlan0
```

## References ##

  * http://raspberryjamberlin.de/zero360-part-2-connecting-via-otg-a-cluster-of-raspberry-pi-zeros-to-a-pi-3/
  * https://forums.raspberrypi.com/viewtopic.php?t=217320
