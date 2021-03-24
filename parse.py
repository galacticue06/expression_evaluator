def depth(string,dp):
    l = [string]
    while True:
        if dp < 1:
            break
        n_l = []
        for i in l:
            n = prim_br(i)
            for j in n:
                prt = get_op(i,j)
                n_l.append(prt[1:len(prt)-1])
            l = n_l[:]
        dp -= 1
    return l
    
def solve_func(string,fname,func):
    ph = fname[:]
    fname.sort(key=len)
    fns = []
    for i in fname:
        fns.append(func[ph.index(i)])
    fname = fname[::-1]
    func = fns[::-1]
    for i in range(len(fname)):
        finder = fname[i]
        call = func[i]
        scrape = string.find(finder)
        try:
            seq = string[scrape:scrape+len(finder)]+get_op(string,scrape+len(finder))
        except:
            seq = ""
        if seq[len(finder)] != "(":
            scrape = -1
        if scrape > -1:
            if "," in seq:
                f = get_op(string,scrape+len(finder))
                splt = f[1:len(f)-1].split(",")
                arg = []
                for j in splt:
                    arg.append(float(solve(j)))
                #res = call(arg)
                res = call(*arg)
            else:
                norm = solve(get_op(string,scrape+len(finder)))
                res = call(float(norm))
            if "e" in str(res):
                res = "{:.12f}".format(res)
            else:
                res = str(res)
            string = string.replace(seq,res)
        else:
            pass
                
        if finder+"(" in string:
            cont = 1
            while cont:
                scrape = string.find(finder)
                try:
                    seq = string[scrape:scrape+len(finder)]+get_op(string,scrape+len(finder))
                except:
                    seq = ""
                if seq[len(finder)] != "(":
                    scrape = -1
                if scrape > -1:
                    if "," in seq:
                        f = get_op(string,scrape+len(finder))
                        splt = f[1:len(f)-1].split(",")
                        arg = []
                        for j in splt:
                            arg.append(float(solve(j)))
                        res = call(arg)
                    else:
                        norm = solve(get_op(string,scrape+len(finder)))
                        res = call(float(norm))
                    if "e" in str(res):
                        res = "{:.12f}".format(res)
                    else:
                        res = str(res)
                    string = string.replace(seq,res)
                else:
                    pass
                if not (finder+"(" in string):
                    cont = 0
    return string
    
def load_const(string,cnames,vals):
    ph = cnames[:]
    cnames.sort(key=len)
    valn = []
    for i in cnames:
        valn.append(vals[ph.index(i)])
    cnames = cnames[::-1]
    vals = valn[::-1]
    cont = 1
    for i in range(len(cnames)):
        while cont:
            acs = 1
            try:
                if string[string.find(cnames[i])+len(cnames[i])] == "(":
                    acs = 0
                if string.find(cnames[i]) < 0:
                    break
            except:
                pass
            if acs:
                string = string.replace(cnames[i],str(vals[i]))
    return string
        

def get_op(string,index):
    try:
        if string[index] != "(":
            return False
    except:
        return False
    br = 0
    string = string[index:len(string)]
    for i in range(len(string)):
        if string[i] == "(":
            br += 1
        if string[i] == ")":
            br -= 1
        if br == 0:
            break
    return string[0:i+1]

def prim_br(string):
    inds = []
    br = 0
    rev = 0
    for i in range(len(string)):
        rev = 0
        if string[i] is "(":
            br += 1
            if br == 1 and rev == 0:
                rev = 1
        elif string[i] is ")":
            br -= 1
            rev = 0
        if br == 1 and rev == 1:
            inds.append(i)
    return inds


def comp(string):
    mts = ['+', '-', '*', '/', '%', '^']
    for i in mts:
        if i in string:
            return True
    return False

def val(string):
    if str(string) != string:
        return float(string)
    try:
        ret = float(string)
        if ret == int(ret):
            return int(ret)
        else:
            return ret
    except:
        return False


def norm(string):
    ls = len(string)
    if string.isnumeric():
        return string
    if "(" in string:
        string = solve(string)
    if "*-" in string or "/-" in string or "*+" in string or "/+" in string:
        prim = 1
    elif "^+" in string or "^-" in string:
        prim = 2
    else:
        prim = 0
    mts = ['+', '-', '*', '/', '%', '^']
    if prim > 0 and string[0] in mts:
        mts = ['*', '/', '^', '+', '-', '%']
    tp = [0, 0, 0, 0, 0, 1]
    if prim == 1:
        mts = mts[::-1]
        mts.append(mts.pop(0))
    elif prim == 2:
        mts = mts[::-1]
    ret = []
    for delim in mts:
        if delim in string:
            if string[0] == delim:
                if string.count(delim) > 1:
                    foo = string[0:string.find(delim)]+" "+string[string.find(delim)+1:ls]
                    ind = foo.find(delim)
                    if string[ind-1] in mts:
                        ind -= 1
                else:
                    pass
            else:
                if tp[mts.index(delim)]:
                    ind = string.find(delim)
                else:
                    ind = len(string)-list(string)[::-1].index(delim)-1
            try:
                if not (string[string.find(delim)-1] in mts):
                    ret.append(string[0:ind])
                    ret.append(string[ind])
                    ret.append(string[ind+1:ls])
                    break
            except:
                pass
                           
    try:
        if ret[0] == "":
            for i in range(3):
                ret.pop(0)
        if comp(ret[0]):
            ret[0] = norm(ret[0])
        
        if comp(ret[2]):
            ret[2] = norm(ret[2])
    except:
        if string[0] == "-":
            string = "_"+string[1:ls]
            return norm(string)
        return string
    
    if "_" in str(ret[0]):
        ret[0] = ret[0].replace("_","-")
    if "_" in str(ret[2]):
        ret[2] = ret[2].replace("_","-")
    if ret[1] == "^":
        res = val(ret[0])**val(ret[2])
    elif ret[1] == "%":
        res = val(ret[0])%val(ret[2])
    elif ret[1] == "*":
        res = val(ret[0])*val(ret[2])
    elif ret[1] == "/":
        res = val(ret[0])/val(ret[2])
    elif ret[1] == "+":
        res = val(ret[0])+val(ret[2])
    elif ret[1] == "-":
        res = val(ret[0])-val(ret[2])
    return res

def solve(string):
    if "(" in string:
        pos = prim_br(string)
        to_rep = []
        rep = []
        for i in pos:
            ops = get_op(string,i)
            to_rep.append(ops)
            rep.append(str(solve(ops[1:len(ops)-1])))
        for i in range(len(to_rep)):
            string = string.replace(to_rep[i],rep[i])
    return norm(string)

def exp_evaluate(seq,func_nms={},const_nms={}):
    func_names = []
    funcs = []
    const_names = []
    vals = []
    for i in func_nms:
        if i in seq:
            func_names.append(i)
            funcs.append(func_nms[i])
    for i in const_nms:
        if i in seq:
            const_names.append(i)
            vals.append(const_nms[i])
    return evaluate(seq, func_names, funcs, const_names, vals)

def eq_evaluate(seq,func_nms={},const_nms={}):
    func_names = []
    funcs = []
    const_names = []
    vals = []
    for i in func_nms:
        if i in seq:
            func_names.append(i)
            funcs.append(func_nms[i])
    for i in const_nms:
        if i in seq:
            const_names.append(i)
            vals.append(const_nms[i])
    delim = None
    eq = "==,>=,<=,&&,||,<,>,!=".split(",")
    for i in eq:
        if i in seq:
            if seq.count(i) > 1:
                return None
            if delim == None:
                delim = i
                ns = [seq.find(i),seq.find(i)+len(i)]
            else:
                f = seq.find(i)
                if not(f >= ns[0] and f <= ns[1]):
                    return None
    parts = seq.split(delim)
    norms = []
    for i in parts:
        norms.append(float(evaluate(i, func_names, funcs, const_names, vals)))
    if delim == eq[5]:
        if norms[0] < norms[1]:
            return True
        else:
            return False
    elif delim == eq[6]:
        if norms[0] > norms[1]:
            return True
        else:
            return False
    elif delim == eq[0]:
        if norms[0] == norms[1]:
            return True
        else:
            return False
    elif delim == eq[1]:
        if norms[0] >= norms[1]:
            return True
        else:
            return False
    elif delim == eq[2]:
        if norms[0] <= norms[1]:
            return True
        else:
            return False
    elif delim == eq[3]:
        if norms[0] and norms[1]:
            return True
        else:
            return False
    elif delim == eq[4]:
        if norms[0] or norms[1]:
            return True
        else:
            return False
    elif delim == eq[7]:
        if norms[0] != norms[1]:
            return True
        else:
            return False
    return None

def evaluate(seq, func_names = [], funcs = [], const_names = [], vals = []):
    replacement = load_const(seq, const_names, vals)
    replacement = solve_func(replacement,func_names,funcs)
    return float(solve(replacement))

