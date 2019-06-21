"""
 pepdrop(  )
    {
    long a, b ;
    extern char globme[];
    user.send_message( " ", " ", -10000, user.location_id, "You start sneezing ATISCCHHOOOOOO!!!!\n" ) ;
    if( ( not Player( 32 ).exists )||( Player( 32 ).location!=user.location_id ) )
    return ;
    /* Ok dragon and pepper time */
    if( ( Item(89).is_carried_by(user) )&&( Item(89).carry_flag==2 ) )
       {
       /* Fried dragon */
       strcpy( Player( 32 ).name, "" ) ; /* No dragon */
       user.score+=100 ;
        yield from user.update()
       return ;
       }
    else
       {
       /* Whoops !*/
       bprintf( "The dragon sneezes forth a massive ball of flame.....\n" ) ;
       bprintf( "Unfortunately you seem to have been fried\n" ) ;
       raise LooseError( "Whoops.....   Frying tonight" ) ;
       }
    }
 
 dragget(  )
    {
    long a, b ;
long l ;
if( user.is_wizard ) return( 0 ) ;
l=Player.find( "dragon" ) ;
if( l== -1 ) return( 0 ) ;
    if( Player( l ).location!=user.location_id ) return( 0 ) ;
    return( 1 ) ;
    }

helpchkr()
{
	long x=user.helping
	if(!user.in_setup) return;
	if(not Player(x).exists) goto nhelp;
	if(Player(x).location!=user.location_id) goto nhelp;
	return;
	nhelp:bprintf("You can no longer help \001c%s\001\n",Player(x).name);
	user.helping = None
}
"""