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
	stock = { "euro":10 }
	processes = {}
	processes["achat_materiel"] = Process({"euro":8},{"materiel":1},10)
	processes["realisation_produit"] = Process({"materiel":1},{"produit":1},30)
	processes["livraison"] = Process({"produit":1},{"client_content":1},20)
	krpsim(stock, processes, optimize)

if __name__ == '__main__':
	main()
