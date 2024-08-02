{
	if ( NR >= 12 ) {
        h = 0; b = 0; e = 0; g = 0; i = 0; t = 0; s = 0; c = 0;
        h += gsub(/H/,"H",$2); 
        b += gsub(/B/,"B",$2);
        e += gsub(/E/,"E",$2);
        g += gsub(/G/,"G",$2);
        i += gsub(/I/,"I",$2); 
        t += gsub(/T/,"T",$2); 
        s += gsub(/S/,"S",$2); 
        c += gsub(/C/,"C",$2);  
        N = h+b+e+g+i+t+s+c; print (h+g+i)/N, e/N, t/N, (c+s)/N;
        }
}
