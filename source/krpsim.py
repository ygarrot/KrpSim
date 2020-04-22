from Process import *

def krpsim(s, p, o):
	"""
	s : stock
	p : processes
	"""
	b = {}
	t = 0
	"""
	b : buffer for input
	t : time
	"""
	for j in range(100):
		for i in p:
			for k, v in p[i].input.items():
				if k in s and s[k] >= v:
					if k in b:
						b[k] += v
					else:
						b[k] = v
			if all (k in b for k in p[i].input.keys()):
				t += p[i].time
				for k, v in p[i].output.items():
					if k in s:
						s[k] += v
					else:
						s[k] = v
				for k, v in p[i].input.items():
					s[k] -= v
			b = {}
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
