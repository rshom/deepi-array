# DEEPi Array #
> Project for an array of DEEPi cameras for low cost deep sea computer
> vision projects.

## Hardware ##

The array consists of a single RPi4 with USB connections to 4x RPiZ based
DEEPi cameras.

## Network ##

The RPi4 creates a network with the RPiZs using Ethernet-over-USB for
communications. A topside computer can access the array using ethernet
communications to the RPi4.

The RPi4 can control the array directly or simply act as a pass through
for another controller. 


## Software ##



## TODO ##

  * [ ] sample synced images
  * [ ] rectify frames
  * [ ] match points
  * [ ] disparity map
  * [ ] stack frames
  * [ ] stitch frames
