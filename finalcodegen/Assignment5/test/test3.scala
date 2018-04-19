object test3{
    def fact_zeros(x:Int):Int = {
    var i:Int = 1;
    var j:Int = 2;
    var k:Int = 1;
    for(i <- 1 to 10) {
        k = k * i;
    }

    var zeroes:Int = 0;
    var temp:Int = k;
    while(temp != 0)
    {
        zeroes += temp/5 ;
        temp /= 5;
    }
    return zeroes;
    }
 }
