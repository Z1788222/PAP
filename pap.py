'''
Programmer: Chase Pranga
ZID: Z1788222
Due Date: 9 August 2019
Purpose: automates common Linux commands and processes
Tested OS: Raspbian OS
Tested System: Raspberry PI 0W
'''

#imports ElementTree library
#calls it ET
import xml.etree.ElementTree as ET
#library allows running system commands
import os
#library for checking file permissions
import stat
#sys library
import sys
#builds tree
softtree = ET.parse('software.xml')
root = softtree.getroot()



'''
Print Functions

Both functions work together to print out the selected programs values
'''
def printFunction():
	sname = raw_input()
	for program in root:
		programName=program.attrib.values()
		if sname == programName:
			printSubtree(program)
			
def printSubtree(stree):
	print stree.attrib.values()
	for sub in stree:
		if sub.tag == "package":
			print sub.text
		else:
			for option in sub:
				print option.text


'''
installFunction

Purpose: runner functions for the install processes
Variables:
	raw_command: what program to install
	pname: name of the checked program package
	programName: sub-tree program name
'''
def installFunction():
	raw_command=raw_input("Type specific program, or 'package': ")
	#checks each program in tree
	for program in root:
		#checks the name of every program
		for pname in program:
			#if program name matches, call installProgram with the program subtree then return
			if pname.text == raw_command:
				installProgram(program)
				return
			break
	return

'''
installProgram

Purpose: actually installs the selected program
Variables: 
	command: string; what shell command to run
Functions Called:
	os.system(): executes string argument as system/shell command
'''
def installProgram(program):
	#find out the package name of the program
#	name = raw_input("Package name: ")
	for option in program:
		if option.tag == program:
			command = "sudo apt install " + option.text
			os.system(command)

'''
installPackage

Arguments: package -> software package to install

Process:
	- iterates over every program tree
		- iterates over every option within program
			- if option tag is package
				- copies variable
			- if option tag is suite, and it matches the desired package
				- install package
				- continue to next program
'''

def installPackage(package):
	installPackage = raw_input("Package name: ")
	for program in root:
		for option in program:
			if option.tag == installPackage:
				installPackage = option.text
			elif option.tag == installPackage:
				command = "sudo apt install " + option.text
				os.system(command)
				continue

'''
configureFunction
Purpose: runner for the configuration function

Supported Programs: Samba, OpenSSH

Variables:
	raw_command: user input of what they want to do
	program: each individual program inside of the xml file
	pname: each programs name
	
'''
def configureFunction():
	raw_command=raw_input("What program would you like to configure: ")
	#checks each program in tree
	for program in root:
		#checks the name of every program
		for pname in program:
			#if program name matches, call configureProgram with the program subtree then return
			if pname.text == raw_command:
				#goes to the respective program configuration function
				if raw_command == "samba":
					sambaConfig(program)
				elif raw_command == "openssh":
					opensshConfig(program)
				return
			break
	return

'''old opensshConfig
def opensshConfig(program):
	#iterate over every option available in openssh xml tree
	os.system("sudo touch sshd_config.tmp")
	for option in program:
		if option.tag == "name" or option.tag == "package" or option.tag == "suite":
			continue
		#checks if the option in question is inside of the config file
		opensshSearch(option, program)
	os.system("sudo rm sshd_config.tmp")

	return
'''

'''
openSSHSearch

Purpose: allows editing of specific lines inside of the ssh_config file

Variables:
	filepath: path to the file to be searched
	verb: keyword of option to search for in file
	option: each supported configuration option
	suboption: each configurable suboption for each option
	verb: supported configuration items
	permissions: old sshd_config file permissions, used to restore to defaults once it exits
	readfile: file being read fromn
	writefile: file being written to
	line: line being read from readfile, written to writefile
	worddict: broken configuration line, (line -> worddict[0] = verb, worddict[1] = option
	writeLine: checks if we are writing a line to the file
	
'''
def opensshSearch(option, program):
	'''
	filepath: path to the file to be searched
	verb: keyword of option to search for in file
	'''
	filepath, verb, output = "", "", ""
	#fills the two above variables
	for suboption in option:
		if suboption.tag == "filepath":
			filepath = suboption.text
		elif suboption.tag == "pretext":
			verb = str(suboption.text)
			break
	permissions = backupFP(filepath)
	readfile = open(filepath, "r")
	writefile = open("sshd_config.tmp", "w")
	for line in readfile:
		'''
		Roundabout logic again
		Don'ty know try and catches, and worddict[0] may break it
		But by iterating over the worddict, it will not break
		'''
		writeline = True
		worddict = line.split()
		counter = 0
		for word in worddict:
			if word == verb:
				output = "Matching line: " + line
				print output
			
		if writeline == True:
			writefile.write(line)
	restoreFP(filepath, permissions)
	return
'''
configureProgram
Purpose: configures program settings/options
Params: pstree -> program subtree
Returns:
Process:
'''

'''
opensshConfig

Purpose: allows editing already existing lines

Variables:
	verbsdict: dictionary; contains all of the supported configuration verbs for modifying openssh
	verb: current line's verb
	outtext: text that gets printed to the screen
	option: supported configuration options for openssh
	sub: options/attributes for each configuration option
'''
def opensshConfig(program):
	verbsdict = {'temp': 'temp'}
	del verbsdict['temp']
	
	unusedverbs = {'temp': 'temp'}
	del unusedverbs['temp']
	verb, outtext = "",""
	'''
	builds dictionary containing supported verbs, with the outtext to match
	'''
	for option in program:
		'''
		skips to next option if not supported
		'''
		if option.tag == "name" or option.tag == "package" or option.tag == "suite":
			continue		
		for sub in option:
			if sub.tag == "output":
				outtext = sub.text
			elif sub.tag == "pretext":
				verb = sub.text
				verbsdict[verb] = outtext
	'''
	- changes sshd_config permissions to 777
	- returns the old file permissions
	'''
	permissions = backupFP("/etc/ssh/sshd_config")
	'''
	- opens sshd_config as readable
	'''
	readfile = open("/etc/ssh/sshd_config", "r")
	writefile = open("sshd_config.tmp", "w")
	
	'''
	- iterates over every line inside of the readfile
	- line will be commented, or will be broken into two parts (verb and option)
	'''
	for line in readfile:
		'''
		- prints out verb and option
		- asks user if they want to modify it
		- if uinput ==
			"": keeps old option
			"delete": deletes/doesnt copy line
			anything else: sets it to the new option
		'''
		
		'''
		if line is commented, copy it over regardless
		then go to next line
		'''
		if line[0][0] == "#"  or line == "/n":
			writefile.write(line)
			continue
		parsed = line.split()
		
		count = 0
		for part in parsed:
			count = count + 1
		if count <= 1:
			writefile.write(line)
			continue
		print 'Verb: ' + parsed[0] + "\n" + 'Option: ' + parsed[1]
		uinput = raw_input("Command: ")
		
		'''
		Possible user inputs:
			"": do not modify line
			"delete": delete line / don't copy over
			anything else: modify line with new configuration option
		'''
		if uinput == "":
			writefile.write(line)
		elif uinput == "delete":
			continue
		else:
			'''
			- combines verb with new option
			- writes new line to file
			- if verb is in dict, pop it
			'''
			outtext = parsed[0] + " " + uinput
			writefile.write(outtext + "\n")
			if parsed[0] in verbsdict:
				verbsdict.pop(parsed[0])
		
	'''
	- iterates over all the unused supported verbs
	'''
	
	for verb in verbsdict:
		'''
		- prints each verbs output
		- asks user what to do
		'''
		uinput = raw_input(verbsdict[verb])
		
		if uinput == "":
			continue
		else:
			'''
			- combines verb with new option
			- writes new line to file
			- if verb is in dict, pop it
			'''
			outtext = verb + " " + uinput
			writefile.write(outtext + "\n")
	
	'''
	closes opened files
	'''
	readfile.close()
	writefile.close()
	'''
	moves the temp file to the new location
	restores the old file permissions
	'''
	os.system("sudo mv sshd_config.tmp /etc/ssh/sshd_config")
	restoreFP("/etc/ssh/sshd_config", permissions)
	
	return

'''
configureProgram

Purpose: allows configuration of single line options for programs
Supported Programs: openssh, samba

Variables:
	
'''
def configureProgram(pstree):
	#define variables
	filepath, outtext = "",""
	outfile = ""
	for option in pstree:
		#makes sure it actually is a config option
		if option.tag == "name" or option.tag == "package":
			continue
		'''
		for loop iterates over every suboption inside of the current option
		
		filepath: file to be opened
		default: default value
		output: what to print to the screen
		pretext: text to go before the option (verb)
		'''
		for config in option:
			if config.tag == "filepath":
				filepath = config.text
			elif config.tag == "default":
				outtext = config.text
			elif config.tag == "output":
				print config.text
				print outtext
				uinput = raw_input("Do you want to change the default value: ")
				if uinput != "no" and uinput != "":
					outtext = uinput
			elif config.tag == "pretext":
				outtext = config.text + " " +outtext
		'''
		changes file permissions to 777
		returns the old file permissions
		'''
		permissions = backupFP(filepath)
		outfile = open(filepath, "a") #opens file to append
		
		#writes newline char
		outfile.write("\n")
		#wirtes outtext to file
		outfile.write(outtext)
		
		outfile.close() #closes file
		restoreFP(filepath, permissions)
	return

'''
sambaConfig
Args: pstree -> program sub tree
Returns:
Supported Configuration Options: Add, Remove
'''
def sambaConfig(pstree):
	uinput=raw_input("Desired samba configuration action: ")
	if uinput == "add":
		sambaAddServer(pstree)
	elif uinput == "delete":
		sambaDeleteServer()
	return

'''
sambaAddServer
Purpose: runner for adding a server to the samba 
'''
def sambaAddServer(pstree):
	#define variables
	filepath = "/etc/samba/smb.conf"
	outtext = ""
	outfile = ""
	
	'''
	Opens file section
	'''
	permissions = backupFP(filepath)
	outfile = open(filepath, "a") #opens file to append
	
	isServerName=False
	
	lineCounter = 1
	#iterates over every option in tree
	for option in pstree:
		#makes sure it actually is a config option
		if option.tag == "name" or option.tag == "package" or option.tag == "suite":
			continue
		#iterates over every configuration option
		for config in option:
			#all possible configuration tags
			if config.tag == "default":
				outtext = config.text
			elif config.tag == "output":
				print config.text
				print outtext
				uinput = raw_input("Do you want to change the default value: ")
				if uinput != "no" and uinput != "":
					outtext = uinput
			elif config.tag == "pretext":
				if config.text == "[":
					outtext = str(config.text) + outtext
				else:
					outtext = str(config.text) + " " + outtext
			elif config.tag == "posttext":
				outtext = outtext + str(config.text)
		
		#writes newline char
		outfile.write("\n")
		#writes tab to file only if not servername field
		if lineCounter != 1:
			outfile.write("  ")
		lineCounter = lineCounter + 1
		#wirtes outtext to file
		outfile.write(outtext)
		
		#restores file permissions
		restoreFP(filepath, permissions)
	outfile.close() #closes file
	return

'''
sambaDeleteServer

Arguments
Returns
Purpose: delete sections of servers
Note: does not explicitly delete file. Lines marked as to be deleted do not get copied over to temp file, then the temp file overwrites the source file
Process:
	- reads input file line by line
	- if line starts a server section
		- asks if to be deleted
	- if line is to be deleted, does not get written to temp file
	- if line is start of new server section
		- asks if section is to deleted
	- copies over temp file, overwriting old source file
	- deletes source file
'''
def sambaDeleteServer():
	filepath = "/etc/samba/smb.conf"
	deletesection = False
	#backup and modify file permissions
	permissions = backupFP(filepath)
	
	'''
	Delete logic
	- copy all servers and lines except desired delete to seperate file
	- write seperate file to source file
	- delete seperate file
	'''
	#source read file
	readfile = open(filepath, "r")
	#destination write file
	writefile = open("samba.tmp", "w")
	for line in readfile:
		'''
		if not a server
		if not a delete section
		'''
		if line[0][0] != "[" and deletesection == False:
			writefile.write(line)
		'''
		if a server section
		
		if not a deletesection:
			write servername to file
			set deletesection to False
		if a deletesection
			set deletesection to True
		'''
		if line[0][0] == "[":
			outline =  line + " server found. Delete? y/n: "
			command = raw_input(outline)
			if command == "n":
				writefile.write(line)
				deletesection = False
			else:
				deletesection = True
	#close opened files
	readfile.close()
	writefile.close()
	
	#open original source file as writable
	writefile = open(filepath, "w")
	#open origianal destination file as readable
	readfile = open("samba.tmp", "r")
	for line in readfile:
		writefile.write(line)
		
	#close opened files
	readfile.close()
	writefile.close()
	
	#delete temp file
	os.system("sudo rm samba.tmp")
	
	return

'''
backupFP

1) backs up file permissions (returns them at end of function)
2) changes permissions to 777 to allow universal read/write access
'''	
def backupFP(filepath):
	#block finds the permissions of file
	st_permissions = os.stat(filepath)
	permissions = oct(st_permissions.st_mode)[-3:] #converts permissions to octal, retains last 3 nums of it and back it up
	tmpcommand= "sudo chmod 777 " + filepath #builds command to run
	os.system(tmpcommand) #changes permissions of file to 777
	return permissions

'''
restoreFP

restores file permissions
filepath: filepath to file
permissions: permissions to change file to
'''
def restoreFP(filepath, permissions):
	tmpcommand= "sudo chmod " + str(permissions) +" "+ filepath #changes file permissions back
	os.system(tmpcommand)
	return

'''
getName

Returns:
	the name of the tree in string format if found
	NULL if name not found
Purpose:
	save me from writing out these lines countless times
'''
def getName(tree):
	for tag in tree:
		if tag.tag == "name":
			return str(tag.text)
	#if name tag not found
	return "NULL"

def printTagText(tree):
	output = ""
	for tag in tree:
		if isSubtree(tag) == False:
			#ifs are to determine comma placement (if placed atr all)
			if output == "":
				output = "Tags: " + tag.text
			else:
				output = output + ", " +tag.text
	if output == "":
		print "Tags: none"
	else:
		print output
	return

def printTagNames(tree):
	output = ""
	for tag in tree:
		if isSubtree(tag) == False:
			#ifs are to determine comma placement (if placed atr all)
			if output == "":
				output = "Tags: " + tag.tag
			else:
				output = output + ", " +tag.tag
	if output == "":
		print "Tags: none"
	else:
		print output
	return

def printTree(tree):
	print "\n"
	print "Current tree: " + getName(tree)
	printChildren(tree)
	printTagNames(tree)
	return


def modifyxml():
	return

'''
isSubtree

Purpose: answers if a tree is actually a subtree or a tag
Returns:
	true: tree is subtree
	false: tree is not a subtree, or is an empty subtree
'''
def isSubtree(tree):
	'''
	only subtrees can be iterable with a for loop
	so if the for loop is entered, then that means it is a populated subtree
	so it then returns true
	'''
	for option in tree:
		return True
	#if not a populated subtree, return false
	return False

'''
modifyxml

Purpose: recursive implementation of the modifyxml function
Features:
	add
		tag
		subtree
	delete
		tag
		subtree
	browse through tree (go up/down)
'''
def modifyxml(tree):
	printTree(tree)
	
	command = raw_input("Command: ")

	while command != "break":
		if command == "help":
			print "Possible commands: go up, goto <child name>, add tag, add subtree, delete <element>"
		elif command == "go up":
			return
		elif command =="add tag":
			'''
			Input from user:
				tagname: the name of the tag <tagname></tagname>
				tagtext: the text that goes between <></>
			'''
			tagname= raw_input("Name of tag: ")
			tagtext= raw_input("Text of tag: ")
			'''
			Can not directly create tags, but rather have to create subelements
			After the subelement is created, I can change the text 
			'''
			newtag= ET.SubElement(tree, tagname)
			newtag.text = tagtext
			softtree.write('test.xml')
		elif command =="add subtree":
			'''
			Input from userL
				treename: name of the tree
				treeatrib: the attribute within the tree
				treetext: the text of the attributer
			a dict is formed with treeatrib and treetext
			End Format:
				<treename treeatrib="treetext">
				</treename>
			'''
			treename=raw_input("Name of new subtree: ")
			treeatrib=raw_input("Attribute name: ")
			treetext=raw_input("Attribute text: ")
			'''
			Creates a dictionary
			Sets the value to the desired things
			'''
			tempdict={}
			tempdict[treeatrib]=treetext
			#Finally creates thew subelement
			newtree=ET.SubElement(tree,treename,tempdict)
			'''
			Problem: subtrees in my program only get their names from a tag of thiers
			Solution: create a name field right off the bat
			'''
			nametag=ET.SubElement(newtree,"name")
			nametag.text=treeatrib
			softtree.write('software.xml')
			#add subtree
			printTree(tree)
		parsed=command.split()
		if parsed[0] == "goto":
			for subtree in tree:
				if getName(subtree) == parsed[1]:
					modifyxml(subtree)
					print "Current name: " + getName(tree)
					printTree(tree)
					break
		elif parsed[0] == "delete":
			tree.remove(parsed[1])
			softtree.write('software.xml')
			printTree(tree)
		command = raw_input("Command: ")


'''
printChildren

Purpose: prints the passed in trees children on a single line, seperated by commas
	- if no children are present, prints that "Children: none"
	
Process:
	- iterates over each child
	- adds the childs name to a string containing all the childrens name
	- prints children variable out
		- if no children present, prints none
'''

def printChildren(tree):
	children = "Children:"
	'''
	iterates over every child within the tree
	'''
	for child in tree:
		#checks the childs name
		childname = str(getName(child))
		#if child has a name, then it gets added to the variable
		if childname != "NULL":
			children = children + " " + childname
	#if children are present, print out their names
	if children == "Children:":
		print "Children: none"
	else:
		print children
	return
	
'''
getDictName

Purpose: returns the name of the passed in element

Process:
	- creates two variables to contain the key and item of the element
	- returns the element
'''
def getDictName(element):

	for a,b in element.items():
		return b
	return


'''
systemCommands

Purpose: allows user to use shorthand for common system commands (such as restarting services, or handing user management)
Source: system.xml file contains all of the categories and individual commands

Process:
	- asks user which category of commands to do
	- lists each command under that specific category
	- asks user which command from that category to execute
	- if additional user input is needed for that command, it prompts the user for it as well
	- combines the command and the user input if needed, then executes that command
'''
def systemcommands():
	systree = ET.parse('system.xml')
	sysroot = systree.getroot()
	
	output = ""
	for genre in sysroot:
		if output == "":
			output = "Available Categories: " + getDictName(genre)
		else:
			output = output + ", " + getDictName(genre)
	print output
	
	output = ""
	command = raw_input("Which category of commands: ")
	exece = ""
	while command != "break":
		'''
		iterates over each category of user commands 
		ex: user management, restart services
		'''
		for genre in sysroot:
			if command == getDictName(genre):
				'''
				Section is if user specifies user management
				
				Prompts the user for which user is acted upon if nexessary
				Prints out each possible command on a line, seperated by commas
				'''
				if command == "user management":
					for option in genre:
						if output == "":
							output = "Commands: " + getDictName(option)
						else:
							output = output + ", " + getDictName(option)
					print output
					output=""
					ucommand = raw_input("What action would you like to do: ")
					while ucommand != "break":
						username = raw_input("What user would you like to act on: ")
						for option in genre:
							if ucommand == getDictName(option):
								for i in option:
									if ucommand != "add user" and ucommand != "delete user":
										exece = ucommand + " " + username
									else:
										exece = ucommand
									os.system(exece)
						ucommand = raw_input("What action would you like to do: ")
				elif command == "restart services":
					for service in genre:
						if output == "":
							output = "Available services: " + getDictName(service)
						else:
							output = output + ", " + getDictName(service)
					ucommand = raw_input("Which service would you like to restart: ")
					for service in genre:
						if getDictName(service) == "ucommand":
							executeTag(service)

						
		command = raw_input("What category of commands: ")
	return
	
'''
executeTag

Purpose: executes the passed in elements command
Arguments: element: element containing an executable command
'''
def executeTag(element):
	exece=""
	for command in element:
		exece = command.text
		os.system(exece)
	return

#loops until user wants to exit
while 1 == 1:
	command = raw_input("What would you like to do: ")

	if command == "print":
		printFunction()
	elif command == "install":
		installFunction()
	elif command == "configure":
		configureFunction()
	elif command == "exit":
		break
	elif command == "help":
		print "Available commands: install, configure, uninstall, modify xml, exit"
	elif command == "modify xml":
		modifyxml(root)
	elif command == "system commands":
		systemcommands()
