from Process import *

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
#			if any (k in mr for k in p[i].o.keys()) or any(k in sr.keys() for k in p[i].o.keys()):
#				for k, v in p[i].i.items():
#					sr[k] = v
			if not p[i].b:
#				if any (k in p[i].o.keys() for k in sr.keys()) or any (k in p[i].o.keys() for k in mr):
					for k, v in p[i].i.items():
						if k in s and s[k] >= v:
							b[k] = True
					if all (k in b for k in p[i].i.keys()):
						print("Process " + i + " started")
						d = True
						p[i].b = True
						for k, v in p[i].i.items():
							print("Removing " + str(v) + " " + str(k))
							s[k] -= v
			elif p[i].b:
				d = True
				p[i].dt += 1
				if (p[i].dt == p[i].t):
					for k, v in p[i].o.items():
						print("Creating " + str(v) + " " + str(k))
						if k in s:
							s[k] += v
						else:
							s[k] = v
					p[i].dt = 0
					p[i].b = False
					print("Process " + i + " ended")
					print(t)
			b = {}
		if (d == False):
			print("No more processes doable at time " + str(t))
			break;
		t += 1
	print(s)
	print(t)

def main():
	stock = {	#"planche":7,
				"euro":8}
	processes = {}
#	processes["do_montant"] = Process({"planche":1},{"montant":1},15)
#	processes["do_fond"] = Process({"planche":2},{"fond":1},20)
#	processes["do_etagere"] = Process({"planche":1},{"etagere":1},10)
#	processes["do_armoire_ikea"] = Process({"montant":2,
#											"fond":1,
#											"etagere":3},{"armoire":1},30)
	processes["achat_materiel"] = Process({"euro":8},{"materiel":1}, 10)
	processes["realisation_produit"] = Process({"materiel":1},{"produit":1}, 30)
	processes["livraison"] = Process({"produit":1},{"client_content":1}, 20)
	optimize = ["armoire", "client_content", "time"]
	krpsim(stock, processes, optimize)

if __name__ == '__main__':
	main()
