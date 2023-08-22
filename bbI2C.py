from machine import	Pin
from utime import sleep_ms
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
		
	def start_condition( self ):
		self.sda.init( Pin.OUT )
		self.scl.init( Pin.OUT )

	def stop_condition( self ):
		self.sda.init( Pin.OUT )
		self.scl.init( Pin.IN )
		self.sda.init( Pin.IN )
		
	def send_bytes( self, bytes ):
		nack	= False
		
		for b in bytes:
			for i in range( 7, -1, -1 ):
				self.scl.init( Pin.OUT )
				if (b >> i) & 1:
					self.sda.init( Pin.IN )
				else:
					self.sda.init( Pin.OUT )
				
				self.scl.init( Pin.IN )
			
			self.scl.init( Pin.OUT )
			self.sda.init( Pin.IN )

			self.scl.init( Pin.IN )
			nack	= self.sda.value()
			self.scl.init( Pin.OUT )

			if nack:
				return nack
		
		return nack
			
	def receive_bytes( self, length ):
		bytes	= []
		for byte_count in range( length ):
			b	= 0
			self.sda.init( Pin.IN )

			# get 8 bits

			for i in range( 7, -1, -1 ):
				self.scl.init( Pin.OUT )
				self.scl.init( Pin.IN )
				b	|= self.sda.value() << i
				
			# send ACK/NACK

			self.scl.init( Pin.OUT )
			
			if byte_count == (length - 1):
				self.sda.init( Pin.IN )
			else:
				self.sda.init( Pin.OUT )
						
			self.scl.init( Pin.IN )
			self.scl.init( Pin.OUT )
			
			bytes	+= [ b ]

		return bytes

	def write( self, addr, data ):
		data	= [ addr & ~0x01 ] + data
		self.start_condition()
		self.send_bytes( data )
		self.stop_condition()
		
	def read( self, addr, length, repeated_start = True ):
		self.start_condition()
		self.send_bytes( [ addr | 0x01 ] )
		data	= self.receive_bytes( length )
		self.stop_condition()
		
		return data

def main():
	i2c	= bbI2C( 0, 1 )

	while True:
		i2c.write( 0x90, [ 0x00 ] )
		data	= i2c.read( 0x90, 2 )
		print( f"{data}" )
		sleep_ms( 100 )
		
if __name__ == "__main__":
	main()
