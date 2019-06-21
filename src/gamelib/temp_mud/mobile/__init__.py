

"""
 crashcom(  )
    {
    }
  @not_dumb_action
 singcom(  )
    {
    user.silly( "\001P%s\001\001d sings in Gaelic\n\001" ) ;
    bprintf( "You sing\n" ) ;
    }
 
 spraycom(  )
    {
    long a, b ;
    long c ;
    char bk[ 128 ] ;
    extern long wordbuf[  ] ;
    a = parser.get_target()
    if( a== -1 ) return ;
    if( brkword(  )== -1 )
       {
       bprintf( "With what ?\n" ) ;
       return ;
       }
    if( !strcmp( wordbuf, "with" ) )
       {
       if( brkword(  )== -1 )
          {
          bprintf( "With what ?\n" ) ;
          return ;
          }
       }
    c = Item.find(
	    wordbuf,
	    available=True,
	    destroyed=parser.user.is_wizard,
	)
    if( c== -1 )
       {
       bprintf( "With what ?\n" ) ;
       return ;
       }
    switch( c )
       {
       default:
          bprintf( "You can't do that\n" ) ;
          break ;
          }
    return ;
    }
 
 /* More new stuff */
 
 dircom(  )
    {
    long a ;
    char b[ 40 ] ;
    char d[ 40 ] ;
    long c ;
    extern long numobs ;
    if( not user.is_wizard )
       {
       bprintf( "That's a wiz command\n" ) ;
       return ;
       }
    a=0 ;
    while( a<numobs )
       {
       c=Zone.find( Item( a ).location, b ) ;
       sprintf( d, "%s%d", b, c ) ;
       if( Item( a ).carry_flag ) strcpy( d, "CARRIED" ) ;
       if( Item( a ).carry_flag==3 ) strcpy( d, "IN ITEM" ) ;
       bprintf( "%-13s%-13s", Item( a ).name, d ) ;
       if( a%3==2 )bprintf( "\n" ) ;
       if( a%18==17 ) pbfr(  ) ;
       a++ ;
       }
    bprintf( "\n" ) ;
    }
 
 sys_reset(  )
    {
    char xx[ 128 ] ;
    FILE *fl ;
    long t, u ;
    if( scale()!=2 )
       {
       bprintf( "There are other people on.... So it wont work!\n" ) ;
       return ;
       }
    time( &t ) ;
    fl=connect( RESET_N, "ruf" ) ;
    if(fl==NULL) goto errk;
    fscanf( fl, "%ld", &u ) ;
    fclose(fl ) ;
    if( ( t-u<( 3600 ) )&&( u<t ) )
       {
       bprintf( "Sorry at least an hour must pass between resets\n" ) ;
       return ;
       }
errk:t=user.level ;
    user.level=10 ;
    rescom(  ) ;
    user.level=t ;
    }
 
 
 dorune(  )
    {
    char bf[ 128 ] ;
    long ct ;
    extern long in_fight;
    if(in_fight) return;
    ct=0 ;
    while( ct<32 )
       {
       if( ct==user ){ct++ ;continue ;}
       if( !strlen( Player( ct ).name ) ) {ct++ ;continue ;}
       if( Player( ct ).is_wizard ) {ct++ ;continue ;}
       if( Player( ct ).location==user.location_id ) goto hitrune ;
       ct++ ;
       }
    return ;
    hitrune:if( randperc(  )<9*user.level ) return ;
    if( Player.find( Player( ct ).name )== -1 ) return ;
    bprintf( "The runesword twists in your hands lashing out savagely\n" ) ;
    hitplayer(ct,32);
    }
 

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