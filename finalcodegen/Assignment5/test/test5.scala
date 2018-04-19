object HelloWorld
{
  var a:Int = 1;
  var b:Int = 2;
  var c:Int = 1;

  var d:Int = 0;

  d= b * b - 4 * a * c;

  if(d < 0)
  {
    var x:Int = 0;
  }

  else
  {
    var sq:Int = d/2;
    var neg:Int = b;

    var x1:Int = (neg + sq)/(2*a);
    var x2:Int = (neg - sq)/(2*a);
  }
 
}
