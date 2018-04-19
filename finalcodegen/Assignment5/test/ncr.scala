/*checks recursive function, while, I/O*/
object program{
	def ncr(n:Int, r:Int):Int = {
		if(r > n || r < 0){
			return 0;
		}

		if(r == 0){
			return 1;
		}

		return ncr(n - 1, r) + ncr(n - 1, r - 1);
	}

	def main():Unit = {
		var t,i,j,k,x:Int = 0;

		scan t;
		x = 0;

		while(x < t){
			scan i;
			scan j;
			k = ncr(i,j);
			println k;
			x += 1;
		}
	}
}