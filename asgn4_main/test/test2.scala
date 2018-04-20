object Dangling_if_else_demo{
	def main(args: Array[String]): Unit ={
		var i: Int = 0;
		var a: Array[Int] =  new Array[Int](3);
		if (i <= 3)
			a[i]+=1;
		if (i >= 2)
			a[i]-=1;
		else
			a[i]=1;
	}
}
