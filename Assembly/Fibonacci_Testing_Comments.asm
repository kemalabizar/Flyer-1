stat {
  int upperlimit,105329
}

var {
  int x,0	// declare int x = 0
  int y,1	// declare int y = 1
  int z,0	// declare int z = 0
}

text {
start:
  add x,y
  sta z		// z = x + y
  trx y,x	// x = y
  trx z,y	// y = z
  cmp x,upperlimit
  jna start	// if x < upperlimit, loop to start
  jmp end	// if x >= upperlimit, loop to end
end:
  dop x,01
  hlt
}