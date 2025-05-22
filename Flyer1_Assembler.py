import sys,re

tklist_vartype = ['int', 'fix', 'asc']
tkdict_opcodes = {
    "lda":[0x000, 2],   "add":[0x100, 3],
    "ldi":[0x010, 2],   "sub":[0x110, 3],
    "sta":[0x020, 2],   "mul":[0x120, 3],
    "sti":[0x030, 3],   "div":[0x130, 3],
    "trx":[0x040, 3],   "ana":[0x140, 2],
    "jmp":[0x050, 2],   "ora":[0x150, 2],
    "jcb":[0x060, 2],   "xra":[0x160, 2],
    "jnc":[0x061, 2],   "not":[0x170, 2],
    "jal":[0x062, 2],   "cmp":[0x180, 3],
    "jna":[0x063, 2],   "shl":[0x190, 3],
    "jeq":[0x064, 2],   "shr":[0x194, 3],
    "jnq":[0x065, 2],   "rol":[0x198, 3],
    "jzr":[0x066, 2],   "ror":[0x19c, 3],
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
    "pop":[0x0d0, 2],   "cla":[0x1d0, 1],
    "nop":[0x0e0, 1],   "itf":[0x1e0, 2],
    "hlt":[0x0f0, 1],   "fti":[0x1f0, 2],
    }

def sourcetostring(source):
    # convert *.asm file into string
    with open(source, mode='r', encoding='utf-8-sig') as f:
        stringified = f.read()
    return stringified

def deletecomments(source_string):
    source_string = re.split("\n", source_string)
    no_comments = ''
    for i in range(0, len(source_string)):
        if '//' in source_string[i]:
            idx_cmt = source_string[i].index('//')
            no_comments += (source_string[i][0:idx_cmt] + '\n')
        else:
            no_comments += (source_string[i] + '\n')
    return no_comments

def tokenize(source_string):
    # tokenize the string
    # e.g. this string, 'and x,y\nsta z\ncmp z,n'
    # the tokenized version is below
    # ['and', 'x,y', 'sta', 'z', 'cmp', 'z,n']
    tokenized = re.split(r" |, |\{|\}|\n|\t", source_string)
    while '' in tokenized: tokenized.remove('')
    return tokenized

def readvariables(source_tokens):
    static, dynamic = {}, {}
    # format: {variable_name:[variable_value, variable_address]}
    idx_stat, idx_dyn, idx_text = 0, 0, 0
    for i in range(0, len(source_tokens)):
        if source_tokens[i] == '.stat': idx_stat = i
        elif source_tokens[i] == '.var': idx_dyn = i
        elif source_tokens[i] == '.text': idx_text = i
        else: pass
    ts = source_tokens[idx_stat:idx_dyn]
    td = source_tokens[idx_dyn:idx_text]
    addr = 0x200000
    for i in range(0, len(ts)):
        if ts[i] in tklist_vartype:
            k = re.split(",", ts[i+1])
            if ts[i] == 'int':
                if '#' in k[1]:
                    k[1] = int(k[1][1:], base=16)
                else: pass
            if ts[i] == 'asc':
                char = 0
                for i in range(0, len(k[1])):
                    char += ord(k[1][i])*(16**(4-2*i))
                k[1] = str(char)
            if ts[i] == 'fix':
                k[1] = int(float(k[1])*(2**8))
            static[k[0]] = [f"{int(k[1]):#0{8}x}"[2:], addr]; addr += 1
        else: pass
    addr = 0x300000
    for i in range(0, len(td)):
        if td[i] in tklist_vartype:
            k = re.split(",", td[i+1])
            if td[i] == 'int':
                if '#' in k[1]:
                    k[1] = int(k[1][1:], base=16)
                else: pass
            if td[i] == 'asc':
                char = 0
                for i in range(0, len(k[1])):
                    char += ord(k[1][i])*(16**(4-2*i))
                k[1] = str(char)
            if td[i] == 'fix':
                k[1] = int(float(k[1])*(2**8))
            dynamic[k[0]] = [f"{int(k[1]):#0{8}x}"[2:], addr]; addr += 1
        else: pass
    return static, dynamic

def pass_1(source_tokens):
    # first pass reads the length of each loop segments (e.g. '*:')
    # outputs a dictionary, format: {loopname: start_ddress}
    # loop_start_address(n) = loop_length(n)
    idx_text = source_tokens.index('.text')
    loop, code_tokens, instr_length = {}, [], 0
    tx = source_tokens[idx_text+1:]
    for i in range(0, len(tx)):
        if ':' not in tx[i]:
            if tx[i] in tkdict_opcodes.keys():
                instr_length += tkdict_opcodes.get(tx[i])[1]
            else: pass
            code_tokens.append(tx[i])
        else:
            loop[tx[i]] = instr_length
    return code_tokens, loop

def pass_2(code_tokens, loops_dict, static_dict, dynamic_dict):
    # compiles the code segment based on three dicts: loop, static vars, and dynamic vars
    machine_code = []
    byte0, byte1 = 0, []
    for i in range(0, len(code_tokens)):
        if code_tokens[i] in tkdict_opcodes.keys():
            byte0 = tkdict_opcodes.get(code_tokens[i])
            opc, span = int(byte0[0])*(2**15), byte0[1]
            machine_code.append(f"{opc:#0{8}x}"[2:])
        else:
            byte1 = re.split(",", code_tokens[i])
            if span == 3: # 3-op instructions
                byte1[0] = f"{(static_dict.get(byte1[0])[1] if byte1[0] in static_dict.keys() else dynamic_dict.get(byte1[0])[1]):#0{8}x}"[2:]
                byte1[1] = f"{(static_dict.get(byte1[1])[1] if byte1[1] in static_dict.keys() else dynamic_dict.get(byte1[1])[1]):#0{8}x}"[2:]
            if opc >= 0x400000 and opc <= 0x580000: # dip, dop, aip, aop
                byte1[0] = f"{(static_dict.get(byte1[0])[1] if byte1[0] in static_dict.keys() else dynamic_dict.get(byte1[0])[1]):#0{8}x}"[2:]
                opcm = int(machine_code[len(machine_code)-1], base=16) + int(byte1[1])*(2**16)
                machine_code[len(machine_code)-1] = f"{opcm:#0{8}x}"[2:]
                byte1.pop()
            if span == 2:
                if opc >= 0x280000 and opc <= 0x378000: # jmp and conditionals
                    byte1[0] = f"{loops_dict.get(byte1[0]+':'):#0{8}x}"[2:]
                if (opc >= 0x000000 and opc <= 0x100000) or (opc >= 0xa00000 and opc <= 0xb80000) or opc == (0x600000 or 0x680000):
                    byte1[0] = f"{(static_dict.get(byte1[0])[1] if byte1[0] in static_dict.keys() else dynamic_dict.get(byte1[0])[1]):#0{8}x}"[2:]
            else:
                pass
            for i in range(0, len(byte1)):
                machine_code.append(byte1[i])
    return machine_code

def hex_obj(machine_code, static_dict, dynamic_dict):
    # adds together the variables into memory
    addr, compiled = 0, []
    for i in range(0, len(machine_code)):
        compiled.append([f"{addr:#0{8}x}"[2:], machine_code[i]])
        addr += 1
    datalist = list(static_dict.items()) + list(dynamic_dict.items())
    for i in range(0, len(datalist)):
        compiled.append([f"{datalist[i][1][1]:#0{8}x}"[2:], datalist[i][1][0]])
    return compiled

# TOKENIZE Pt.1: Turn source file into string
srcstr = sourcetostring('NewAssemblyTypesetTest.asm')
# TOKENIZE Pt.2: Delete comments in string
delcom = deletecomments(srcstr)
# TOKENIZE Pt.3: Tokenize by words
srctkn = tokenize(delcom)

# PASS 1 Pt.1: Extract the data (stat, var) within the tokens
data = readvariables(srctkn)
stt, var = data[0], data[1]
# PASS 1 Pt.2: Extract instruction lines (text) into instkn, read loop lengths into dict loops
prog = pass_1(srctkn)
cdtkn, loops = prog[0], prog[1]

# PASS 2 Pt.1: With reference of stt, var and loops, generate proper code
codehex = pass_2(cdtkn, loops, stt, var)
objthex = hex_obj(codehex, stt, var)

print(delcom)
print('\n', srctkn)
print('\n', stt, '\n', var)
print('\n', cdtkn, '\n', loops)
print('\n', codehex)

print('v3.0 hex words addressed')
for i in range(0, len(objthex)):
    print(f"{objthex[i][0]}: {objthex[i][1]}")
