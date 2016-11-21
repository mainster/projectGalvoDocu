typedef struct LED
{
	int BitNr;
};
LED 	*LED_Create( int aBitNr )
{
	LED *me = malloc( sizeof( LED ) );
	LED_Init( me, aBitNr );
}
void LED_Destroy( LED *me ) {
	LED_Cleanup( me );
	free( me );
}
void LED_Init( LED *me, int aBitNr )
{
	if ( me != NULL)
	{
		IODIR1 |= 1 << aBitNr;
		me->BitNr = aBitNr;
	}
}
void LED_Cleanup( LED *me )
{
// Do nothing
}
void LED_on( LED *me )
{
	IOSET1 = 1 << me->BitNr;
}
void LED_off( LED *me )
{
	IOCLR1 = 1 << me->BitNr;
}