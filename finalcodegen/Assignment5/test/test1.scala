object FactorialRecursion {
 
	def fun(b:Int,c:Int):Int = {
		var x:Int = 2;
		var y:Int = 5;
		for (x<- 1 to 2*x - 1 by 2) {
		y = y + 1;
		}
		return x;
	}
	
	
	var z:Int = fun(2,3);
	var ar:Array[Int] = new Array[Int](50);
	var i:Int = 0;
	
	for(i <- 0 to 49){
		ar[i] = i;
	}
}
