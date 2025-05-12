stat {
 int max,15
 int inc1,1
}

var {
 int n,0
 int x,1
}

text {
start:
 add x,inc1
 sta x
 mul x,x
 sta x
 add n,inc1
 sta n
 cmp n,max
 jna start
 jmp end
end:
 dop x,03
 hlt
}