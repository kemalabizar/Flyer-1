import sys, re

opclib = {
    "lda":[0x000, 2],    "add":[0x100, 3],
    "ldi":[0x010, 2],    "sub":[0x110, 3],
    "sta":[0x020, 2],    "mul":[0x120, 3],
    "sti":[0x030, 3],    "div":[0x130, 3],
    "trx":[0x040, 3],    "ana":[0x140, 2],
    "jmp":[0x050, 2],    "ora":[0x150, 2],
    "jcb":[0x060, 2],    "xra":[0x160, 2],
    "jnc":[0x061, 2],    "not":[0x170, 2],
    "jal":[0x062, 2],    "cmp":[0x180, 3],
    "jna":[0x063, 2],    "shl":[0x190, 3],
    "jeq":[0x064, 2],    "shr":[0x194, 3],
    "jnq":[0x065, 2],    "rol":[0x198, 3],
    "jzr":[0x066, 2],    "ror":[0x19c, 3],
    "jnz":[0x067, 2],
    "jng":[0x068, 2],
    "jps":[0x069, 2],
    "jpe":[0x06a, 2],
    "jpo":[0x06b, 2],
    "clf":[0x070, 1],
    "dip":[0x080, 2],
    "dop":[0x090, 2],
    "aip":[0x0a0, 2],
    "aop":[0x0b0, 2],
    "pst":[0x0c0, 2],
    "pop":[0x0d0, 2],    "cla":[0x1d, 1],
    "nop":[0x0e0, 1],    "itf":[0x1e, 2],
    "hlt":[0x0f0, 1],    "fti":[0x1f, 2]
    }

# File read into string, split by lines. lines = ['__line1__', '__line2__', ...]
f = open(sys.argv[0], mode='r'); f = f.read()
lines = re.split("\n", f)

# lines[i] split by '//' (comment markers), delete comments
for i in range(0, len(lines)):
    lines[i] = re.split("//", lines[i])
    if len(lines[i]) > 1: lines[i].pop(1)
    else: pass
# remove empty elements, e.g. lines that are empty because of comment deletion
    while '' in lines[i]:
        lines[i].remove('')
while [] in lines:
    lines.remove([])
for i in range(0, len(lines)):
    lines[i] = lines[i][0]
# join the comment-exempt lines into one long s
s = ""
for i in range(0, len(lines)):
    s += lines[i] + "\n"
# separate each section by parentheses
s = re.split("{|}", s); lines.clear()

# static section (s[1]) processing
static = {} # static = {'__label__':[__type__, __value__, __location__]}
s[1] = re.split("\n", s[1])
# initialize memory location for static variables
address = 0x200000
while '' in s[1]: s[1].remove('')
# split each static declaration lines into [type, label, value]
for i in range(0, len(s[1])):
    s[1][i] = re.split(" |,", s[1][i])
    # processing 'int' declarations
    if s[1][i][0] == 'int':
        if '#' in s[1][i][2]:
            s[1][i][2] = '0x' + str(s[1][i][2])[1:7]
        else:
            s[1][i][2] = f"{int(str(s[1][i][2])):#0{8}x}"
    # processing 'fix' declarations
    if s[1][i][0] == 'fix':
        'this might work'
        value = re.split("\.", s[1][i][2])
        value[0] = f"{int(value[0]):#0{6}x}"[2:]
        # converting decimal fractions into binary fractions (fuck me. and thanks Math Stack Exchange)
        # https://math.stackexchange.com/questions/3336008/ upvote both Q and A if you can. He helped made this possible.
        value[1] = float('0.'+value[1]); fracbin = ''
        for j in range(0, 8):
            value[1] *= 2
            #print(j, value[1])
            if value[1] >= 1.0:
                fracbin += '1'; value[1] -= 1
            else:
                fracbin += '0'
        value[1] = hex(int(fracbin, base=2))[2:]
        s[1][i][2] = '0x' + value[0] + value[1]
    # processing 'asc' declarations:
    if s[1][i][0] == 'asc':
        word = s[1][i][2]; char = ''
        for j in range(0, len(word)):
            char += hex(ord(word[j]))[2:]
        char = '0x' + char[:6]
        s[1][i][2] = char
    # add new elements to dict static, per the format previously
    static[s[1][i][1]] = [s[1][i][0], s[1][i][2], hex(address)]
    address += 1

# var section (s[3]) processing
var = {} # var = {'__label__':[__type__, __value__, __location__]}
s[3] = re.split("\n", s[3])
# initialize memory location for dynamic variables (var)
address = 0x300000
while '' in s[3]: s[3].remove('')
# split each var declaration lines into [type, label, value]
for i in range(0, len(s[3])):
    s[3][i] = re.split(" |,", s[3][i])
    # check if the names for dynamic variables are already used as static
    # if that happens, raise error
    if s[3][i][1] in static:
        print("ASSEMBLING ERROR 1: VARIABLE NAME ALREADY USED AS STATIC")
        break
    else: pass
    # processing 'int' declarations
    if s[3][i][0] == 'int':
        if '#' in s[3][i][2]:
            s[3][i][2] = '0x' + str(s[3][i][2])[1:7]
        else:
            s[3][i][2] = f"{int(str(s[3][i][2])):#0{8}x}"
    # processing 'fix' declarations
    if s[3][i][0] == 'fix':
        'this might work'
        value = re.split("\.", s[3][i][2])
        value[0] = f"{int(value[0]):#0{6}x}"[2:]
        # converting decimal fractions into binary fractions (fuck me. and thanks Math Stack Exchange)
        # https://math.stackexchange.com/questions/3336008/ upvote both Q and A if you can. He helped made this possible.
        value[1] = float('0.'+value[1]); fracbin = ''
        for j in range(0, 8):
            value[1] *= 2
            #print(j, value[1])
            if value[1] >= 1.0:
                fracbin += '1'; value[1] -= 1
            else:
                fracbin += '0'
        value[1] = hex(int(fracbin, base=2))[2:]
        s[3][i][2] = '0x' + value[0] + value[1]
    # processing 'asc' declarations:
    if s[3][i][0] == 'asc':
        word = s[3][i][2]; char = ''
        for j in range(0, len(word)):
            char += hex(ord(word[j]))[2:]
        char = '0x' + char[:6]
        s[3][i][2] = char
    # add new elements to dict static, per the format previously
    var[s[3][i][1]] = [s[3][i][0], s[3][i][2], hex(address)]
    address += 1

# code section (s[5]) processing
# PASS 1: Record loop labels and their respective locations.
loop = {} # loop = {'__label__':loopStartLocation}
# split the code by lines
code = re.split("\n", s[5]); location = 0
while '' in code: code.remove('')
for i in range(0, len(code)):
    # if line is a loop label, append it to the dictionary
    if ":" in code[i]:
        loop[code[i]] = location
    # else if line is an instruction, split by tab and space
    else:
        code[i] = re.split("\t| ", code[i])
        while '' in code[i]: code[i].remove('')
        # get the value of how much memory will that instruction line occupy
        location += opclib.get(code[i][0])[1]

# PASS 2: Using var, static and loop dict, fill any necessary labels with corresponding addresses/data
for i in range(0, len(list(loop))):
    # remove lines consisting of just loop labels; we already have them
    if list(loop)[i] in code:
        code.remove(list(loop)[i])
var_keys, static_keys = list(var.keys()), list(static.keys())
loop_keys = list(loop.keys())
for i in range(0, len(code)):
    code[i][0] = opclib.get(code[i][0])[0]
    # print(code[i])
    if len(code[i]) == 2:
        if ',' in code[i][1]:
            op = re.split(",", code[i][1]); code[i].pop(1)
            code[i].append(op[0]); code[i].append(op[1])
            if len(code[i]) == 3:
                # 2-op inst. (sti, trx, add, sub, mul, div, cmp, shl, shr, rol, ror)
                if code[i][0] == 0x030:
                    # sti
                    code[i][1] = f"{int(code[i][1][1:], base=16):#0{8}x}"[2:]
                    code[i][2] = f"{int(code[i][2][1:], base=16):#0{8}x}"[2:]
                if (code[i][0] >= 0x080) and (code[i][0] <= 0x0b0):
                    # dip, dop, aip, aop
                    code[i][0] += int(code[i][2])*2
                    if code[i][1] in var_keys:
                        code[i][1] = var.get(code[i][1])
                        code[i][1] = code[i][1][2][2:]
                    elif code[i][1] in static_keys:
                        code[i][1] = static.get(code[i][1])
                        code[i][1] = code[i][1][2][2:]
                    code[i].pop()
                    # print(code[i][1], code[i][2])
                else:
                    # trx, add, sub, mul, div, cmp, shl, shr, rol, ror
                    if code[i][1] in var_keys:
                        code[i][1] = var.get(code[i][1])
                        code[i][1] = code[i][1][2][2:]
                    elif code[i][1] in static_keys:
                        code[i][1] = static.get(code[i][1])
                        code[i][1] = code[i][1][2][2:]
                    if code[i][2] in var_keys:
                        code[i][2] = var.get(code[i][2])
                        code[i][2] = code[i][2][2][2:]
                    elif code[i][2] in static_keys:
                        code[i][2] = static.get(code[i][2])
                        code[i][2] = code[i][2][2][2:]
                    # print(code[i][1], code[i][2])
        else:
            # 1-op inst. (lda, sta, ldi, jmp, conditional branchings, ana, ora, xra, not, itf, fti)
            if code[i][0] == 0x010:
                # ldi
                pass
            if ((code[i][0] >= 0x050) and (code[i][0] <= 0x06f)):
                # jmp and conditional branching
                colonlabel = code[i][1]+':'
                if colonlabel in loop_keys:
                    code[i][1] = loop.get(colonlabel)
            else:
                # lda, sta, ana, ora, xra, not, itf, fti
                if code[i][1] in var_keys:
                    code[i][1] = var.get(code[i][1])
                    code[i][1] = code[i][1][2][2:]
                elif code[i][1] in static_keys:
                    code[i][1] = static.get(code[i][1])
                    code[i][1] = code[i][1][2][2:]
    else: pass
    code[i][0] *= (2**15)
    code[i][0] = f"{code[i][0]:#0{8}x}"[2:]
    if len(code[i]) > 1 and type(code[i][1]) is int:
        code[i][1] = f"{code[i][1]:#0{8}x}"[2:]

# Printing out the codes
# Printing format: MemoryAddr: Opcode Operand1 Operand2
write_address = 0; print('hex v3.0 addressed')
for i in range(0, len(code)):
    if len(code[i]) == 1:
        write_address = f"{write_address:#0{8}x}"
        print(write_address, ":", code[i][0])
        write_address = int(write_address, base=16) + 1
    if len(code[i]) == 2:
        write_address = f"{write_address:#0{8}x}"
        print(write_address, ":", code[i][0], code[i][1])
        write_address = int(write_address, base=16) + 2
    if len(code[i]) == 3:
        write_address = f"{write_address:#0{8}x}"
        print(write_address, ":", code[i][0], code[i][2])
        write_address = int(write_address, base=16) + 3
