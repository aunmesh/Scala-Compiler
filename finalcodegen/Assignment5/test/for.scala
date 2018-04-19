object PrimeSieve{
	def main():Unit = {
	var i,j,k,n,m:Int = 0;
	var p:Array[Int] = new Array[Int](1001);
	m = 1000;

	for(i <- 2 to m){
		p[i] = 1;
	}

	for(i <- 2 to m){
		if(p[i] == 1){
			for(j <- i*i to m by i){
				p[j] = 0;
			}
		}
	}

	for(i <- 2 to m){
		p[i] = p[i] + p[i - 1];
	}

	scan m;
	i = 0;

	while(i <= m){
		scan n;
		println p[n];
		i += 1;
	}
}