object program{
	def main():Unit = {
		var a:Array[Int] = new Array[Int](101);
		var i,j:Int = 0;

		a[0] = 0;
		i = 1;

		while(i < 101){
			j = a[i - 1];
			a[i] = j + i;
			i += 1;
		}

		var k:Int = a[100];
	}
}