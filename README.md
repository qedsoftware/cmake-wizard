cmake-wizard
===============

Description
---------------

This is a simple python script that constructs an out-of-source CMake build directory structure and CMakeLists.txt files.

William Wu (william.wu@themathpath.com), 2012 December 31 


Demo
---------------

$ python cmake-wizard.py 

	Enter author name: W.Wu
	Enter project directory name: cmake-wizard-demo
	Enter name of main program (ex: main.c): main.cpp
	Enter name of executable (ex: demo): demo
	List standard third-party libraries, delimited by spaces (ex: m blas crypto): crypto
	List special third-party libraries to be found, delimited by spaces (ex: GSL LAPACK OPENCV): OPENCV
	List custom-written libraries in source directory: foo bar baz
	Print file extensions ('c' or 'cpp'): cpp

$ tree cmake-wizard-demo/
	cmake-wizard-demo/
	├── CMakeLists.txt
	├── README.txt
	├── build
	└── src
	    └── CMakeLists.txt

	2 directories, 3 files

$ more cmake-wizard-demo/CMakeLists.txt 

	# W.Wu, 2012-12-31 23:00
	cmake_minimum_required(VERSION 2.8)
	project( cmake-wizard-demo )
	find_package( OPENCV REQUIRED )
	add_subdirectory( src )

$ more cmake-wizard-demo/src/CMakeLists.txt 

	# W.Wu, 2013-03-25 23:00
	include_directories (${cmake-wizard-demo_SOURCE_DIR}/src)
	link_directories (${cmake-wizard-demo_BINARY_DIR}/src)
	set (LIBS foo bar baz)
	foreach (lib ${LIBS})
	        add_library (${lib} ${lib}.cpp)
	endforeach (lib)
	set (CORELIBS crypto ${OPENCV_LIBRARIES})
	add_executable (demo main.cpp)
	target_link_libraries (demo ${CORELIBS} ${LIBS} )
	# for debugging --- print out all variable names:
	# get_cmake_property(_variableNames VARIABLES)
	# foreach (_variableName ${_variableNames})
	#    message(STATUS "${_variableName}=${${_variableName}}")
	# endforeach()


Requirements
---------------
System requirements: python