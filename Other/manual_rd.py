## case 2
letter = a-z | A-Z
digit = 0 - 9
id: letter (letter|digit)*
digits = digit+
{program var integer}
num: digit+
floatNum: digit+ ( \L | . digits)
relop: \= | <> | > | >\= | < | <\=
assign: \:\=
{real begin end if else then while do read write}
addop: \+ | -
mulop: \* | /
[: ; , . \(\)]

# test
program example ;
var  sum , count  : integer ;
	begin
		pass := 0 ;
		count := 0.343 ;
		sum := 3403 ;
		while pass <> 10  do
		begin
		pass := pass + 1 ;
read (mnt) ;
if mnt <= 0 then
count := count + 1.234
else
sum := sum + mnt
end ;
write (sum , count)
end.



# rd:
{program var integer}
{real begin end if else then while do read write}
[: ; , . \(\)]

rd for them:
rd = "program|var|integer|real|begin|end|if|else|then|while|do|read|write|:|;|,|.|\\"

