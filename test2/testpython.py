from amplpy import AMPL,DataFrame

ampl = AMPL()
ampl.read('testmodel1.mod')
ampl.readData('testdata1.dat')
ampl.setOption('solver','cplex')


nbr = ampl.getParameter('nbr')
nbr.setValues([1])

#df = DataFrame()
l1 = ampl.getParameter('line')
l1.setValues([1])

c = ampl.getParameter('c')
up = ampl.getParameter('up')
b = ampl.getParameter('b')
line = ampl.getParameter('line')

cdf = c.getValues()
cdf.setValues({2:3})
ampl.setData(cdf)


cdf = c.getValues()
cdf.setValues({2:3})
ampl.setData(cdf)
#
cdf = up.getValues()
cdf.setValues({2:3})
ampl.setData(cdf)
#
cdf = line.getValues()
cdf.setValues({2:3})
ampl.setData(cdf)

# --- Strange bug? ---
#print(repr(ampl.getParameter('line').getValues().toDict()))

#cdic = c.getValues().toDict()
#print(repr(cdic))

#listb = b.getValues().toList()
#print(repr(listb))
#print(line.getValues().getNumCols())

nbr.setValues([2])

#c.setValues([10,20])
#up.setValues([10,20])
#b.setValues([10,20])
#line.setValues([10,20])
#ampl.setData('')
#ampl.setData()
#ampl.setData()
#ampl.setData()

#df = DataFrame('testint')
#df.addRow('testint',[2,2])
#ampl.setData(df,'testint')

#dfint = testint.getValues()
#print(repr(dfint))

# Test adding row to data



#df.addColumn('testint',values=[3])
#ampl.setData(df,setName="testint")

ampl.solve()
profit = ampl.getObjective('profit')
print(repr(profit.value()))
a = profit.value()
print(repr(a + 3))

# Prints the values of the line variable
print("Line var:" + repr(ampl.getParameter('line').getValues().toDict()))

# -- Prints the decision variables
varidf = ampl.getVariable('X').getValues()
print("Decision variables: " + repr(varidf.toDict()))

# Commands: eval(), getParameter(), getObjective().

