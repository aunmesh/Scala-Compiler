object program {
	def main():Unit = {
		var p:Array[Int] = new Array[Int](100);
		var i,j,k,n:Int = 0;

		scan n;

		for(i <- 0 to n){
			j = p[i];
			k = j + i * i;
			p[i] = k;
			println p[i];
		}
	}
}
