from machine import	Pin
import	utime

class bbI2C:
	def __init__( self, sda_pin, scl_pin ):
		self.sda	= Pin( sda_pin, Pin.OUT )
		self.sda.value( 0 )
		self.sda.init( Pin.IN )

		self.scl	= Pin( scl_pin, Pin.OUT )
		self.scl.value( 0 )
		self.scl.init( Pin.IN )
		
	def __init__2( self, sda_pin, scl_pin ):
		self.sda	= bbI2C_pin( sda_pin )
		self.scl	= bbI2C_pin( scl_pin )

	def pin_toggle( self ):
		self.sda.init( Pin.OUT )
		self.scl.init( Pin.OUT )
		self.sda.init( Pin.IN )
		self.scl.init( Pin.IN )



class bbI2C_pin( Pin ):
	def __init__( self, pin_number ):
		self.pin	= Pin( pin_number, Pin.OUT )
		self.pin.value( 0 )
		self.pin.init( Pin.IN )
	
	def input( self ):
		self.init( Pin.IN )
		
	def output( self ):
		self.init( Pin.OUT )

def main():
	i2c	= bbI2C( 0, 1 )

	while True:
		i2c.pin_toggle()

if __name__ == "__main__":
	main()
