from machine import	Pin
import	utime

class bbI2C:
	def __init__( self, sda_pin, scl_pin ):
		self.sda	= bbI2C_pin( sda_pin )
		self.scl	= bbI2C_pin( scl_pin )

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
		i2c.sda.output()
		i2c.scl.output()
		i2c.sda.input()
		i2c.scl.input()

if __name__ == "__main__":
	main()
