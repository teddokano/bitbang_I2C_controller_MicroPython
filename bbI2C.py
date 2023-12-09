"""
# Lisence
This project is licensed under the MIT License, see the LICENSE.txt file for details
https://github.com/teddokano/bitbang_I2C_controller_MicroPython
"""
from	machine		import	Pin
import	uerrno

class bbI2C:
	bit_order	= tuple( n for n in range( 7, -1, -1 ) )
	
	def __init__( self, sda = None, scl = None ):
		self.sda	= sda
		self.scl	= scl
		
		self.sda.value( 0 )
		self.scl.value( 0 )
		self.sda.init( Pin.IN )
		self.scl.init( Pin.IN )
		
	def start_condition( self ):
		self.scl.init( Pin.IN )
		self.sda.init( Pin.OUT )

	def stop_condition( self ):
		self.sda.init( Pin.OUT )
		self.scl.init( Pin.IN )
		self.sda.init( Pin.IN )			
		
	def send_bytes( self, bytes ):
		ack_count	= -1

		for b in bytes:
		
			#	sending data bits
			for i in self.bit_order:
				self.scl.init( Pin.OUT )
				self.sda.init( Pin.IN if (b >> i) & 1 else Pin.OUT )
				self.scl.init( Pin.IN )
			
			#	getting ACK/NACK
			self.scl.init( Pin.OUT )
			self.sda.init( Pin.IN )

			self.scl.init( Pin.IN )
			nack	= self.sda.value()
			self.scl.init( Pin.OUT )

			if nack:
				return ack_count
			else:
				ack_count	+= 1		

		return ack_count
			
	def receive_bytes( self, length ):
		bytes	= []
		for byte_count in range( length ):
			b	= 0
			self.sda.init( Pin.IN )

			#	getting data bits
			for i in self.bit_order:
				self.scl.init( Pin.OUT )
				self.scl.init( Pin.IN )
				b	|= self.sda.value() << i
				
			#	sending ACK/NACK
			self.scl.init( Pin.OUT )
			self.sda.init( Pin.IN if byte_count == (length - 1) else Pin.OUT )
			self.scl.init( Pin.IN )
			self.scl.init( Pin.OUT )
			
			bytes	+= [ b ]

		return bytes

	def writeto( self, addr, data, stop = True ):
		data	= [ (addr << 1) & ~0x01 ] + list( data )
		self.start_condition()
		ack_count	= self.send_bytes( data )
		
		if stop or (ack_count == -1):
			self.stop_condition()
		
		if ack_count == -1:
			raise OSError( uerrno.EIO )
		
		return ack_count
		
	def readfrom( self, addr, length, stop = True ):
		self.start_condition()
		nack	= self.send_bytes( [ (addr << 1) | 0x01 ] )
		
		if not nack:
			data	= self.receive_bytes( length )

		if stop:
			self.stop_condition()
			
		if nack:
			raise OSError( uerrno.EIO )
			
		return bytearray( data )

def main():
	i2c				= bbI2C( sda = Pin( 0 ), scl = Pin( 1 ) )
	target_address	= 0xEC >>1

	while True:
		i2c.writeto( target_address, [ 0x88 ], stop = False )
		data	= i2c.readfrom( target_address, 2 )
		print( list(data) )
		
		sleep_ms( 100 )

if __name__ == "__main__":
	from	utime	import	sleep_ms
	main()
