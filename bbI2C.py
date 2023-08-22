import	machine
import	utime

sda	= machine.Pin( 0, machine.Pin.OUT )
scl	= machine.Pin( 1, machine.Pin.OUT )

while True:
	sda.on()
	scl.on()
	sda.off()
	scl.off()
	
