stat {
  int upperlimit,105329
}

var {
  int x,0
  int y,1
  int z,0
}

text {
start:
  add x,y
  sta z
  trx y,x
  trx z,y
  cmp x,upperlimit
  jna start
  jmp end
end:
  dop x,01
  hlt
}