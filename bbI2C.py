from	machine	import	Pin
from	utime	import	sleep_ms

from	micropython	import	const

_GPIO_IN		= const( 0xD0000004 )
_GPIO_OE_SET	= const( 0xD0000024 )
_GPIO_OE_CLR	= const( 0xD0000028 )

_SDA			= const( 0 )
_SCL			= const( 1 )

_SDA_PIN		= const( 0x0001 << _SDA )
_SCL_PIN		= const( 0x0001 << _SCL )

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
		
	@micropython.viper
	def start_condition( self ):
		reg_set	= ptr32( _GPIO_OE_SET )

		reg_set[0] = _SDA_PIN
		reg_set[0] = _SCL_PIN

	@micropython.viper
	def stop_condition( self ):
		reg_set	= ptr32( _GPIO_OE_SET )
		reg_clr	= ptr32( _GPIO_OE_CLR )

		reg_set[ 0 ] = _SDA_PIN
		reg_clr[ 0 ] = _SCL_PIN
		reg_clr[ 0 ] = _SDA_PIN
	
	@micropython.viper
	def send_bytes( self, bytes ) -> bool:
		nack	= False
		reg_set	= ptr32( _GPIO_OE_SET )
		reg_clr	= ptr32( _GPIO_OE_CLR )
		
		for b in bytes:
			for i in self.bit_order:
				reg_set[0] = _SCL_PIN
				if (int(b) >> int(i)) & 0x1:
					reg_clr[ 0 ]	 = _SDA_PIN
				else:
					reg_set[ 0 ] = _SDA_PIN
				
				reg_clr[ 0 ]	= _SCL_PIN	
				
			reg_set[ 0 ] = _SCL_PIN
			reg_clr[ 0 ] = _SDA_PIN

			reg_clr[ 0 ] = _SCL_PIN
			nack	= bool( self.sda.value() )
			reg_set[ 0 ] = _SCL_PIN

			if nack:
				return nack
		
		return nack
	
	@micropython.native
	def receive_bytes( self, length ):
		bytes	= []
		for byte_count in range( length ):
			b	= 0
			machine.mem32[ _GPIO_OE_CLR ] = _SDA_PIN

			for i in self.bit_order:
				machine.mem32[ _GPIO_OE_SET ] = _SCL_PIN
				machine.mem32[ _GPIO_OE_CLR ] = _SCL_PIN
				b	|= ((machine.mem32[ _GPIO_IN ] >> _SDA) & 0x1) << i
				
			machine.mem32[ _GPIO_OE_SET ] = _SCL_PIN
			
			if byte_count == (length - 1):
				machine.mem32[ _GPIO_OE_CLR ] = _SDA_PIN
			else:
				machine.mem32[ _GPIO_OE_SET ] = _SDA_PIN
						
			machine.mem32[ _GPIO_OE_CLR ] = _SCL_PIN
			machine.mem32[ _GPIO_OE_SET ] = _SCL_PIN
			
			bytes	+= [ b ]

		return list( bytes )

	def write( self, addr, data ):
		data	= bytearray( [ addr & ~0x01 ] + data )
		
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
	i2c	= bbI2C( _SDA, _SCL )

	while True:
		i2c.write( 0x90, [ 0x00 ] )
		data	= i2c.read( 0x90, 2 )
		print( f"{data}" )
		sleep_ms( 100 )
		
if __name__ == "__main__":
	main()
