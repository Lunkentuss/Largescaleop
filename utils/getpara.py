from amplpy import DataFrame


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

# Get the list representing a given parameter that depends
# only on a single valued index set
def para2list(ampl,str,integer=True):
	list_para = ampl.getParameter(str).getValues().toList()
	if(integer):
		list_para = [int(list_para[i][1]) for i in range(len(list_para))]
	else:
		list_para = [list_para[i][1] for i in range(len(list_para))]
	return list_para
	

# Sets a parameter that is indexed by a single ordered set 
def setParamOfSingleSet(ampl,set_name,param_name,values):
	set_list = ampl.getSet(set_name).getValues().toList()
	set_list = [x[0] for x in set_list]
	param_dict = {set_list[i]:values[i] for i in range(len(set_list))}
	df = DataFrame((set_name),(param_name))
	df.setValues(param_dict)
	ampl.setData(df)
	return
