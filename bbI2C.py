from	machine		import	Pin
from	utime		import	sleep_ms

class bbI2C:
	bit_order	= tuple( n for n in range( 7, -1, -1 ) )
	
	def __init__( self, sda_pin, scl_pin ):
		self.sda	= self.pin_init( sda_pin )
		self.scl	= self.pin_init( scl_pin )
		
	def pin_init( self, pin_id ):
		pin	= Pin( pin_id, Pin.OUT )
		pin.value( 0 )
		pin.init( Pin.IN )
		
		return pin
		
	def start_condition( self ):
		self.scl.init( Pin.IN )
		self.sda.init( Pin.OUT )

	def stop_condition( self ):
		self.sda.init( Pin.OUT )
		self.scl.init( Pin.IN )
		self.sda.init( Pin.IN )			
		
	def send_bytes( self, bytes ):
		for nb, b in enumerate( bytes ):
		
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

			if (nb == 0):
				if nack:
					raise OSError( 5 )
				else:
					ack_count	= 0
			else:
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
		
		if stop:
			self.stop_condition()
		
		return ack_count
		
	def readfrom( self, addr, length, stop = True ):
		self.start_condition()
		self.send_bytes( [ (addr << 1) | 0x01 ] )
		data	= self.receive_bytes( length )

		if stop:
			self.stop_condition()

		return bytearray( data )

def main():
	i2c				= bbI2C( 0, 1 )
	target_address	= 0x90 >>1

	while True:
		send_data	= [ 0x00 ]
		num_of_ack	= i2c.writeto( target_address, send_data, stop = False )
		
		if num_of_ack == (len( send_data ) + 1):
			data	= i2c.readfrom( target_address, 2 )
			print( f"{list(data)}" )
		else:
			print( f"target ({target_address}) returned NACK" )	
		
		#sleep_ms( 100 )
		
if __name__ == "__main__":
	main()
