stat {
 int inc1,1
}

var {
 int x,327841
 int y,47
 int n,0
}

text {
start:
 sub x,y
 sta x
 add n,inc1
 sta n
 cmp x,y
 jal start
 jmp end
end:
 dop n,01
 dop x,02
 hlt
}