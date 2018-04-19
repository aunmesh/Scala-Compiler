object test{
	def summation(n:Int) : Int = {
	var i:Int = 0;

	do{
		i = i + n;
		n -= 1;
	} while(n > 0);
	return i;
	}

	def modexp(x:Int, y:Int, p:Int) : Int = {
		var res:Int = 1;
		x = x % p;
		while(y > 0)
		{
			if(y % 2 == 1)
			{
				res = (res * x) % p;
			}

			y >>= 1;
			x = (x * x) % p;
		}

		return res;
	}
}
