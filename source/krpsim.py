from Process import *

def get_requests(p, s, mr, sr, pp):
    r = pp.r
    for j in range(10):
        for i in p:
            if any (k in mr for k in p[i].o.keys()) or any (k in sr.keys() for k in p[i].o.keys()):
                for k, v in p[i].i.items():
                    sr[k] = v
    if pp.r <= 0:
    #if all (p[k].r <= 0 for k in p):
        for k in sr.keys():
            if k in pp.o:
                r += sr[k]
        for k in mr:
            if k in pp.o:
                r += 1
    return r, sr;

def check_stock_for_process(pp, s):
    """
    pp : current process
    s : stock
    Parcours les inputs d'un process
    Stock dans un buffer les inputs qui sont dans le stock
    en quantite suffisante.
    Retourne le buffer
    """
    b = {}
    for k, v in pp.i.items():
        if k in s and s[k] >= v:
            b[k] = True
    return b

def check_start_process(pp, b, s, t, i, d):
    """
    pp : current process
    b : buffer
    s : stock
    t : global time
    i : current process name(key)
    d : process doable at time t
    Check if buffer contains all process' inputs
    if so remove from the stock the input and start the process setting it to
    busy.
    """
    if all (k in b for k in pp.i.keys()):
        print(str(t) + ":" + i)
        for k, v in pp.i.items():
            print("Removing " + str(v) + " " + str(k))
            s[k] -= v
        return True, True, s
    return False, d, s

def krpsim(s, p, o):
    """
    s : stock
    p : processes
    o : optimize
    """
    b = {}
    t = 0
    mr = [v for v in o if v != "time"]
    sr = {}
    """
    b : buffer for input
    t : time
    mr : main requests
    sr : sub requests
    """
    while t < 10000:
        d = False
        for i in p:
            p[i].r, sr = get_requests(p, s, mr, sr, p[i])
            if not p[i].b and p[i].r > 0:
                b = check_stock_for_process(p[i], s)
                p[i].b, d, s = check_start_process(p[i], b, s, t, i, d)
            elif p[i].b:
                d = True
                p[i].dt += 1
                if (p[i].dt == p[i].t):
                    for k, v in p[i].o.items():
                        print("Creating " + str(v) + " " + str(k))
                        p[i].r -= v
                        if k in s:
                            s[k] += v
                        else:
                            s[k] = v
                    p[i].dt = 0
                    p[i].b = False
                    print("Process " + i + " ended")
            b = {}
        if (d == False):
            print("no more process doable at time " + str(t))
            break;
        t += 1
    print(s)
    print(t)
