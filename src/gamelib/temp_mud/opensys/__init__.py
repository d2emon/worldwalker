def closeworld(*args):
    raise NotImplementedError()


def openworld(*args):
    raise NotImplementedError()


"""
/* Fast File Controller v0.1 */
 
FILE *filrf=NULL;  /* - = not open */

closeworld()
{
	extern FILE *filrf;
        extern long objinfo[],numobs,ublock[];
	if(filrf==NULL) return;
	sec_write(filrf,objinfo,400,4*numobs);
	sec_write(filrf,ublock,350,16*48);
	filrf.disconnect()
	filrf= NULL;
}
 
FILE *openworld()
{
	extern FILE *filrf;
        extern long objinfo[],numobs,ublock[];
	if(filrf!=NULL) return(filrf);
	filrf=connect("/usr/tmp/-iy7AM","r+");
	if(filrf==NULL)
	   crapup("Cannot find World file");
	sec_read(filrf,objinfo,400,4*numobs);
	sec_read(filrf,ublock,350,16*48);
	return(filrf);
}
 
"""