stat {
  fix s,80.25
  int shrconst,2
  int inc1,1
  int replimit,100
}

var {
  fix x,100.0
  int n,0
  fix t1,0.0
  fix t2,0.0
  fix t3,0.0
}

text {
start:
  div s,x
  sta t1
  add x,t1
  sta t2
  shr t2,shrconst
  sta x
  add n,inc1
  sta n
  cmp n,replimit
  jna start
  jmp end
end:
  dop x,01
  hlt
}