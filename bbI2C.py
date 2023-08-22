from machine import	Pin
import	utime

class bbI2C:
	def __init__( self, sda_pin, scl_pin ):
		self.sda	= self.pin_init( sda_pin )
		self.scl	= self.pin_init( scl_pin )
		
	def pin_init( self, pin_id ):
		pin	= Pin( pin_id, Pin.OUT )
		pin.value( 0 )
		pin.init( Pin.IN )
		
		return pin

	def pin_toggle( self ):
		self.sda.init( Pin.OUT )
		self.scl.init( Pin.OUT )
		self.sda.init( Pin.IN )
		self.scl.init( Pin.IN )

def main():
	i2c	= bbI2C( 0, 1 )

	while True:
		i2c.pin_toggle()

if __name__ == "__main__":
	main()
