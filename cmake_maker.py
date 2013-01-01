#!/usr/bin/env python
# William Wu, 2012-12-31
import os, sys, datetime, getopt

# parameters
author = "William Wu"
time_fmt = "%Y-%m-%d %H:%M"

# usage
def usage():
	print('Usage:\n\t%s' % sys.argv[0])
	print('Synopsis:')
	print('\tGenerates basic CMake directory structure and CMakeLists.txt files.')

# main method
def main(argv):
	
	# defaults
	prompts_flag = True
	project_name = "project"
	main_program_name = "main.cpp"
	executable_name = "demo"
	standard_libraries = [ "m" ]
	special_libraries = [ "OPENCV" ]
	custom_libraries = [ ]
	file_extension = "cpp"
		
	# command-line argument parsing
	try:
		opts, args = getopt.gnu_getopt(argv, "fh", ["fast","help"])
	except getopt.GetoptError:
		usage()
		sys.exit(2)
	for opt, arg in opts:
		if opt in ("-h", "--help"):
			usage()
			sys.exit()
		elif opt in ("-f", "--fast"):
			prompts_flag = False
				
	# gather parameters from user
	if prompts_flag: 
		project_name = raw_input("Enter project directory name: ")
		main_program_name = raw_input("Enter name of main program (ex: main.c): ")
		executable_name = raw_input("Enter name of executable (ex: demo): ")
		standard_libraries = raw_input("List standard third-party libraries (ex: m, blas, crypto): ").split()
		special_libraries = raw_input("List special third-party libraries to be found (ex: GSL, LAPACK, OPENCV): ").split()
		custom_libraries = raw_input("List custom-written libraries in source directory: ").split()	
		file_extension = raw_input("Print file extensions ('c' or 'cpp'): ")
	
	# construct directories
	os.system("mkdir -p %s/src" % project_name)
	os.system("mkdir -p %s/build" % project_name)	
	
	# current time
	now = datetime.datetime.now()
	
	# a = content of top-level makefile
	a = "# %s, %s\n" % (author, now.strftime(time_fmt))
	a += "cmake_minimum_required(VERSION 2.8)\n"
	a += "project( %s )\n" % project_name
	for lib in special_libraries:
		a += "find_package( %s REQUIRED )\n" % lib
	a += "add_subdirectory( src )"	
	
	# write top-level makefile
	cmakefile_a = open("%s/CMakeLists.txt" % project_name,"w")
	cmakefile_a.write(a)
	cmakefile_a.close()

	# b = content of src-level makefile
	b = "# %s, %s\n" % (author, now.strftime(time_fmt))
	b += "include_directories (${%s_SOURCE_DIR}/src)\n" % project_name
	b += "link_directories (${%s_BINARY_DIR}/src)\n" % project_name
	if len(custom_libraries) > 0:
		b += "set (LIBS %s)\n" % " ".join(custom_libraries)
		b += "foreach (lib ${LIBS})\n"
		b += "\tadd_library (${lib} ${lib}.%s)\n" % file_extension
		b += "endforeach (lib)\n"
	corelibs_string = " ".join(standard_libraries) + " " + " ".join(map(lambda x: "${" + x + "_LIBRARIES}", special_libraries))
	b += "set (CORELIBS %s)\n" % corelibs_string
	b += "add_executable (%s %s)\n" % (executable_name,main_program_name)
	if len(custom_libraries) > 0:
		b += "target_link_libraries (%s ${CORELIBS} ${LIBS} )\n" % executable_name
	else:
		b += "target_link_libraries (%s ${CORELIBS} )\n" % executable_name
	b += """# for debugging --- print out all variable names:
# get_cmake_property(_variableNames VARIABLES)
# foreach (_variableName ${_variableNames})
#    message(STATUS "${_variableName}=${${_variableName}}")
# endforeach()
"""

	# write src-level makefile
	cmakefile_b = open("%s/src/CMakeLists.txt" % project_name,"w")
	cmakefile_b.write(b)
	cmakefile_b.close()

# invoke main
if __name__ == "__main__":
	main(sys.argv[1:])