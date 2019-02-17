import xml.etree.ElementTree as ET  
import glob, os, sqlite3, os, sys, re, json

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
print ('Files processed: ')

script_dir = os.path.dirname(__file__)
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
				print('Processed: '+filename)
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