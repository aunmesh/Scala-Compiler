object Rational {
	def gcd(x: Int, y: Int): Int = {
		var i:Int = 0;
		while(i > 0){
			x = y;
			y = i;
			i = x % y;
		}

		return i;
	}

	var n:Int = 105;
	var d: Int = 10;
	val g:Int = gcd(n, d);
	val numer: Int = n/g;
	val denom: Int = d/g;
}
