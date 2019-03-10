import xml.etree.ElementTree as ET  
import glob, os, sqlite3, os, sys, re, json

processed = 0

#Create sqlite databases
db = sqlite3.connect('usagestats.db')
cursor = db.cursor()

#Create table usagedata.

cursor.execute('''

    CREATE TABLE data(usage_type TEXT, lastime TEXT, timeactive TEXT, package TEXT, types TEXT, classs TEXT,

					  source TEXT, fullatt TEXT)

''')

db.commit()

err=0

print ()
print ('Android Usagestats XML Parser')
print ('By: @AlexisBrignoni')
print ('Web: abrignoni.com')
print ()
print ('Files: ')

#script_dir = os.path.dirname(__file__)
script_dir = os.path.dirname(os.path.abspath(__file__))
for filename in glob.iglob(script_dir+r'\usagestats\**', recursive=True):
	if os.path.isfile(filename): # filter dirs
		file_name = os.path.basename(filename)
		#Test if xml is well formed
		if file_name == 'version':
			continue	
		else:
			if 'daily' in filename:
				sourced = 'daily'
			elif 'weekly' in filename:
				sourced = 'weekly'
			elif 'monthly' in filename:
				sourced = 'monthly'
			elif 'yearly' in filename:
				sourced = 'yearly'
				
			file_name_int = int(file_name)
			
			try:
				ET.parse(filename)
			except ET.ParseError:
				print('Parse error - Non XML file? at: '+filename)
				err = 1
				#print(filename)
			
			if err == 1:
				err = 0
				continue
			else:
				tree = ET.parse(filename)
				root = tree.getroot()
				print('Processing: '+filename)
				for elem in root:
					#print(elem.tag)
					usagetype = elem.tag
					#print("Usage type: "+usagetype)
					if usagetype == 'packages':
						for subelem in elem:
							#print(subelem.attrib)
							fullatti_str = json.dumps(subelem.attrib)
							#print(subelem.attrib['lastTimeActive'])
							time1 = subelem.attrib['lastTimeActive']
							time1 = int(time1)
							if time1 < 0:
								finalt = abs(time1)
							else:
								finalt = file_name_int + time1
							#print('final time: ')
							#print(finalt)
							#print(subelem.attrib['package'])
							pkg = (subelem.attrib['package'])
							#print(subelem.attrib['timeActive'])
							tac = (subelem.attrib['timeActive'])
							#print(subelem.attrib['lastEvent'])
							#insert in database
							cursor = db.cursor()
							datainsert = (usagetype, finalt, tac, pkg, '' , '' , sourced, fullatti_str,)
							#print(datainsert)
							cursor.execute('INSERT INTO data (usage_type, lastime, timeactive, package, types, classs, source, fullatt)  VALUES(?,?,?,?,?,?,?,?)', datainsert)
							db.commit()
					
					elif usagetype == 'configurations':
						for subelem in elem:
							fullatti_str = json.dumps(subelem.attrib)
							#print(subelem.attrib['lastTimeActive'])
							time1 = subelem.attrib['lastTimeActive']
							time1 = int(time1)
							if time1 < 0:
								finalt = abs(time1)
							else:
								finalt = file_name_int + time1
							#print('final time: ')
							#print(finalt)
							#print(subelem.attrib['timeActive'])
							tac = (subelem.attrib['timeActive'])
							#print(subelem.attrib)
							#insert in database
							cursor = db.cursor()
							datainsert = (usagetype, finalt, tac, '' , '' , '' , sourced, fullatti_str,)
							cursor.execute('INSERT INTO data (usage_type, lastime, timeactive, package, types, classs, source, fullatt)  VALUES(?,?,?,?,?,?,?,?)', datainsert)
							db.commit()
			
					elif usagetype == 'event-log':
						for subelem in elem:
							#print(subelem.attrib['time'])
							time1 = subelem.attrib['time']
							time1 = int(time1)
							if time1 < 0:
								finalt = abs(time1)
							else:
								finalt = file_name_int + time1
							
							#time1 = subelem.attrib['time']
							#finalt = file_name_int + int(time1)
							#print('final time: ')
							#print(finalt)
							#print(subelem.attrib['package'])
							pkg = (subelem.attrib['package'])
							#print(subelem.attrib['type'])
							tipes = (subelem.attrib['type'])
							#print(subelem.attrib)
							fullatti_str = json.dumps(subelem.attrib)
							#add variable for type conversion from number to text explanation
							#print(subelem.attrib['fs'])
							#classy = subelem.attrib['class']
							if 'class' in subelem.attrib:
								classy = subelem.attrib['class']
								cursor = db.cursor()
								datainsert = (usagetype, finalt, '' , pkg , tipes , classy , sourced, fullatti_str,)
								cursor.execute('INSERT INTO data (usage_type, lastime, timeactive, package, types, classs, source, fullatt)  VALUES(?,?,?,?,?,?,?,?)', datainsert)
								db.commit()
							else:
							#insert in database
								cursor = db.cursor()
								datainsert = (usagetype, finalt, '' , pkg , tipes , '' , sourced, fullatti_str,)
								cursor.execute('INSERT INTO data (usage_type, lastime, timeactive, package, types, classs, source, fullatt)  VALUES(?,?,?,?,?,?,?,?)', datainsert)
								db.commit()
								
#query for reporting
cursor.execute('''
select 
usage_type,
datetime(lastime/1000, 'UNIXEPOCH', 'localtime') as lasttimeactive,
timeactive as time_Active_in_msecs,
timeactive/1000 as timeactive_in_secs,
package,
CASE types
     WHEN '1' THEN 'MOVE_TO_FOREGROUND'
     WHEN '2' THEN 'MOVE_TO_BACKGROUND'
     WHEN '5' THEN 'CONFIGURATION_CHANGE'
	 WHEN '7' THEN 'USER_INTERACTION'
	 WHEN '8' THEN 'SHORTCUT_INVOCATION'
     ELSE types
END types,
classs,
source,
fullatt
from data
order by lasttimeactive DESC
''')
all_rows = cursor.fetchall()

#HTML report section
h = open('./Report.html', 'w')	
h.write('<html><body>')
h.write('<h2>Android Usagestats report</h2>')
h.write ('<style> table, th, td {border: 1px solid black; border-collapse: collapse;}</style>')
h.write('<br />')

#HTML headers
h.write('<table>')
h.write('<tr>')
h.write('<th>Usage Type</th>')
h.write('<th>Last Time Active</th>')
h.write('<th>Time Active in Msecs</th>')
h.write('<th>Time Active in Secs</th>')
h.write('<th>Package</th>')
h.write('<th>Types</th>')
h.write('<th>Class</th>')
h.write('<th>Source</th>')
h.write('</tr>')

for row in all_rows:
	usage_type = row[0]
	lasttimeactive = row[1]
	time_Active_in_msecs = row[2]
	timeactive_in_secs = row[3]
	package = row[4]
	types = row[5]
	classs = row[6]
	source = row[7]
	
	processed = processed+1
	#report data
	h.write('<tr>')
	h.write('<td>'+str(usage_type)+'</td>')
	h.write('<td>'+str(lasttimeactive)+'</td>')
	h.write('<td>'+str(time_Active_in_msecs)+'</td>')
	h.write('<td>'+str(timeactive_in_secs)+'</td>')
	h.write('<td>'+str(package)+'</td>')
	h.write('<td>'+str(types)+'</td>')
	h.write('<td>'+str(classs)+'</td>')
	h.write('<td>'+str(source)+'</td>')
	h.write('</tr>')

#HTML footer	
h.write('<table>')
h.write('<br />')	

print('')
print('Records processed: '+str(processed))
print('Triage report completed. See Reports.html.')	
	
	
