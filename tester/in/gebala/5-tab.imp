( tab.imp )
VAR
	n j ta[25] tb[25] tc[25]
BEGIN
	n := 25 - 1;
	tc[0] := n;
	tc[n] := n - n;
	FOR i FROM tc[0] DOWNTO tc[n] DO
		ta[i] := i;
		tb[i] := n - i;
	ENDFOR
	FOR i FROM tc[n] TO tc[0] DO
		tc[i] := ta[i] * tb[i];
	ENDFOR
	FOR i FROM 0 TO n DO
		WRITE tc[i];
	ENDFOR
END
