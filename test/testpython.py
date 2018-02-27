from amplpy import AMPL,DataFrame

ampl = AMPL()
ampl.read('testmodel1.mod')
ampl.readData('testdata1.dat')


testint = ampl.getParameter('testint')
testint.setValues([2,2])

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


# Commands: eval(), getParameter(), getObjective().
