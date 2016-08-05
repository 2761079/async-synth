"""Creation de la formaule ltl"""
def ltlgathering(n,k):
		ltlFile = open("ltlFile.ltl",'w')
		#fairness
		for i in range(k):
			ltlFile.write("#define f0_{0} (P_Rbt{0}.RLC)\n".format(i))
			ltlFile.write("#define f1_{0} (P_Rbt{0}.Front || P_Rbt{0}.Back || P_Rbt{0}.Idle)\n\n".format(i))
		#gathering
		ltlFile.write("\n\n#define gather (")
		for i in range(k-1):
			ltlFile.write("pos[{0}]==pos[{1}]".format(i,i+1 ))
			if i != k-2:
				ltlFile.write(" && ")
		ltlFile.write(")\n\n")


		ltlFile.write("#property (G(")
		for i in range(k):
			ltlFile.write("(F(f0_{0})) && (F(f1_{0}))".format(i))
			if i < k-1:
				ltlFile.write(" && ")
		ltlFile.write(")) -> (FG (gather) )")

		ltlFile.close()
		

def uppaalQuery():
		queryFile = open("gathering.q",'w')
		queryFile.write("control: A<>Process.goal")
		queryFile.close()

