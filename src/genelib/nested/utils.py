def weighted_choose(data, weight):
    # Returns an element from an array at random according to a weight.
    # A weight of 2 means the first element will be picked roughly twice as often as the second; a weight of 0.5 means
    # half as often. A weight of 1 gives a flat, even distribution.
    pass
    """
    if (weightChoose<=0 || weightChoose==undefined) weightChoose=1;
    return arr[Math.floor(Math.pow(Math.random(),weightChoose)*arr.length)];
    """
    # return arr[Math.floor((1-Math.pow(Math.random(),1/weightChoose))*arr.length)];
    # this would give a different curve

    # previously
    """
    var iChoose;
    var arrChoose=[];
    if (weightChoose<=0 || weightChoose==undefined) weightChoose=1;
    for (iChoose=0;iChoose<arr.length;iChoose++)
    {
        if (Math.round(Math.random()*(iChoose*weightChoose))==0) arrChoose.push(arr[iChoose]);
    }
    return Choose(arrChoose);
    """


"""
function Title(what)
{
    // Changes a string like "the cat is on the table" to "the Cat Is on the Table"
    what=what.split(" ");
    var toReturn="";
    for (var i in what)
    {
        if (what[i]!="of" && what[i]!="in" && what[i]!="on" && what[i]!="and" && what[i]!="the" && what[i]!="an" && what[i]!="a" && what[i]!="with" && what[i]!="to" && what[i]!="for") what[i]=what[i].substring(0,1).toUpperCase()+what[i].substring(1);
        toReturn+=" "+what[i];
    }
    return toReturn.substring(1);
}
"""
