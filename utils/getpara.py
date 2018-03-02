# Creates a matrix from a DataFrame object representing
# the flex matrix mat[j][k].
# Remard: The jobs and machines are index from zero

def flexdf2mat(df,nbr_of_jobs,nbr_of_machines):

	flex_list = df.toList()
	mat = [[0 for x in range(nbr_of_machines)]
			for y in range(nbr_of_jobs)]

	ind = 0;
	for i in range(nbr_of_jobs):
		for j in range(nbr_of_machines):
			mat[i][j] = int(flex_list[ind][2]) 
			ind = ind + 1
	return mat
	

# Get a single valued parameter with name str from the 
# object ampl
def getSingleParameter(ampl,str):
	return ampl.getParameter(str).getValues().toList()[0][0]

# Sets a single valued parameter with name str in the
# object ampl
def setSingleParameter(ampl,str,value):
	ampl.getParameter(str).setValues([value])
	return

# Get the list representing a given set with name str in the 
# object ampl
def set2list(ampl,str):
	return [x[0] for x in ampl.getSet(str).getValues().toList()]
