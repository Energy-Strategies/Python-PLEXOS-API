# -*- coding: utf-8 -*-
"""
Retrieve data from the PLEXOS input dataset

Created on Sat Sep 09 19:19:57 2017

@author: Steven
"""

import os

# Python .NET interface
from dotnet.seamless import add_assemblies, load_assembly#, build_assembly

# load PLEXOS assemblies
plexos_path = 'C:/Program Files (x86)/Energy Exemplar/PLEXOS 7.5/'
add_assemblies(plexos_path)
load_assembly('PLEXOS7_NET.Core')
load_assembly('EEUTILITY')

# .NET related imports
from PLEXOS7_NET.Core import DatabaseCore
from EEUTILITY.Enums import *

# Create an object to store the input data
db = DatabaseCore()
'''
Void Connection(
	String strFile
	)
'''
db.Connection('rts_PLEXOS.xml')

output_file = open('rts_PLEXOS.txt','w')

# list the generators
output_file.write('List of generators\n')
'''
String[] GetObjects(
	ClassEnum nClassId
	)
'''
for gen in db.GetObjects(ClassEnum.Generator):
    output_file.write(gen + '\n')
    
# query data for a generator
'''
Recordset GetPropertiesTable(
	CollectionEnum CollectionId,
	String ParentNameList[ = None],
	String ChildNameList[ = None],
	String TimesliceList[ = None],
	String ScenarioList[ = None],
	String CategoryList[ = None]
	)
'''
rs = db.GetPropertiesTable(CollectionEnum.SystemGenerators,'','101_1')
rs.MoveFirst()

# write the data in the table from the ADODB.Recordset
if not rs is None and not rs.EOF:
    output_file.write('\n\nProperties of generator 101_1\n' + ','.join([x.Name for x in rs.Fields])+'\n')
    while not rs.EOF:
        output_file.write(','.join([str(x.Value) for x in rs.Fields])+'\n')
        rs.MoveNext()

# close the output file
output_file.close()