import	machine
import	utime

sda	= machine.Pin( 0, machine.Pin.OUT )
scl	= machine.Pin( 1, machine.Pin.OUT )

while True:
	sda.value( 1 )
	scl.value( 1 )
	sda.value( 0 )
	scl.value( 0 )
