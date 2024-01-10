from machine import	Pin
import	utime

def main():
	initialize( 0, 1 )
	sda	= pin_init( 0 )
	scl	= pin_init( 1 )

	while True:
		sda.init( Pin.OUT )
		scl.init( Pin.OUT )
		sda.init( Pin.IN )
		scl.init( Pin.IN )


def initialize( sda_pin, scl_pin ):
	sda	= pin_init( sda_pin )
	scl	= pin_init( scl_pin )


def pin_init( pin_number ):
	pin	= Pin( pin_number, Pin.OUT )
	pin.value( 0 )
	pin.init( Pin.IN )
	
	return pin


if __name__ == "__main__":
	main()
