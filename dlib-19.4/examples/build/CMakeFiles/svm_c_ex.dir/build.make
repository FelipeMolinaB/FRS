# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.5

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list


# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /root/face_course/dlib-19.4/examples

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /root/face_course/dlib-19.4/examples/build

# Include any dependencies generated for this target.
include CMakeFiles/svm_c_ex.dir/depend.make

# Include the progress variables for this target.
include CMakeFiles/svm_c_ex.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/svm_c_ex.dir/flags.make

CMakeFiles/svm_c_ex.dir/svm_c_ex.cpp.o: CMakeFiles/svm_c_ex.dir/flags.make
CMakeFiles/svm_c_ex.dir/svm_c_ex.cpp.o: ../svm_c_ex.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/root/face_course/dlib-19.4/examples/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object CMakeFiles/svm_c_ex.dir/svm_c_ex.cpp.o"
	/usr/bin/c++   $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/svm_c_ex.dir/svm_c_ex.cpp.o -c /root/face_course/dlib-19.4/examples/svm_c_ex.cpp

CMakeFiles/svm_c_ex.dir/svm_c_ex.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/svm_c_ex.dir/svm_c_ex.cpp.i"
	/usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /root/face_course/dlib-19.4/examples/svm_c_ex.cpp > CMakeFiles/svm_c_ex.dir/svm_c_ex.cpp.i

CMakeFiles/svm_c_ex.dir/svm_c_ex.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/svm_c_ex.dir/svm_c_ex.cpp.s"
	/usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /root/face_course/dlib-19.4/examples/svm_c_ex.cpp -o CMakeFiles/svm_c_ex.dir/svm_c_ex.cpp.s

CMakeFiles/svm_c_ex.dir/svm_c_ex.cpp.o.requires:

.PHONY : CMakeFiles/svm_c_ex.dir/svm_c_ex.cpp.o.requires

CMakeFiles/svm_c_ex.dir/svm_c_ex.cpp.o.provides: CMakeFiles/svm_c_ex.dir/svm_c_ex.cpp.o.requires
	$(MAKE) -f CMakeFiles/svm_c_ex.dir/build.make CMakeFiles/svm_c_ex.dir/svm_c_ex.cpp.o.provides.build
.PHONY : CMakeFiles/svm_c_ex.dir/svm_c_ex.cpp.o.provides

CMakeFiles/svm_c_ex.dir/svm_c_ex.cpp.o.provides.build: CMakeFiles/svm_c_ex.dir/svm_c_ex.cpp.o


# Object files for target svm_c_ex
svm_c_ex_OBJECTS = \
"CMakeFiles/svm_c_ex.dir/svm_c_ex.cpp.o"

# External object files for target svm_c_ex
svm_c_ex_EXTERNAL_OBJECTS =

svm_c_ex: CMakeFiles/svm_c_ex.dir/svm_c_ex.cpp.o
svm_c_ex: CMakeFiles/svm_c_ex.dir/build.make
svm_c_ex: dlib_build/libdlib.a
svm_c_ex: /usr/lib/x86_64-linux-gnu/libnsl.so
svm_c_ex: /usr/lib/x86_64-linux-gnu/libSM.so
svm_c_ex: /usr/lib/x86_64-linux-gnu/libICE.so
svm_c_ex: /usr/lib/x86_64-linux-gnu/libX11.so
svm_c_ex: /usr/lib/x86_64-linux-gnu/libXext.so
svm_c_ex: /usr/lib/x86_64-linux-gnu/libpng.so
svm_c_ex: /usr/lib/x86_64-linux-gnu/libjpeg.so
svm_c_ex: /usr/lib/libatlas.so
svm_c_ex: /usr/lib/libcblas.so
svm_c_ex: /usr/lib/liblapack.so
svm_c_ex: CMakeFiles/svm_c_ex.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/root/face_course/dlib-19.4/examples/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable svm_c_ex"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/svm_c_ex.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/svm_c_ex.dir/build: svm_c_ex

.PHONY : CMakeFiles/svm_c_ex.dir/build

CMakeFiles/svm_c_ex.dir/requires: CMakeFiles/svm_c_ex.dir/svm_c_ex.cpp.o.requires

.PHONY : CMakeFiles/svm_c_ex.dir/requires

CMakeFiles/svm_c_ex.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/svm_c_ex.dir/cmake_clean.cmake
.PHONY : CMakeFiles/svm_c_ex.dir/clean

CMakeFiles/svm_c_ex.dir/depend:
	cd /root/face_course/dlib-19.4/examples/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /root/face_course/dlib-19.4/examples /root/face_course/dlib-19.4/examples /root/face_course/dlib-19.4/examples/build /root/face_course/dlib-19.4/examples/build /root/face_course/dlib-19.4/examples/build/CMakeFiles/svm_c_ex.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/svm_c_ex.dir/depend

