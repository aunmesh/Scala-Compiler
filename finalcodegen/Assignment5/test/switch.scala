/*Switch Statement*/
object program {
	def main():Unit = {
		var n,i,j:Int = 0;

		scan n;

		while(i <= n){
			scan j;
			j match {
				case 1 => {println "Uno";}
				case 2 => {println "Duo";}
				case 3 => {println "Trio";}
			}

			i += 1;

		}
	}
}