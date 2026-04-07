# 🧱 CMake Build System (C Project Guide)

A **complete beginner → intermediate guide** to understanding and using **CMake with Make & Ninja** on Windows for building C projects.

---

# 📌 Table of Contents

1. What is CMake?
2. Build System Overview (How everything works)
3. Installing Tools (Windows)
4. First CMake Project (Hello World)
5. Using Different Generators (Make vs Ninja)
6. Multi-file Project Structure
7. Libraries in CMake
8. Common Commands Cheat Sheet
9. Debug vs Release Builds
10. Common Mistakes
11. Recommended Workflow
12. Complete CMake Commands Reference

---

# 1️⃣ What is CMake?

CMake is a **build system generator**.

👉 It does NOT compile your code directly.

Instead:

* It generates build files for tools like:

  * **Make**
  * **Ninja**
  * Visual Studio

---

# 2️⃣ 🧠 How the Build System Works

## 🔁 Full Flow

```
Your Code → CMake → Build System (Ninja/Make) → Compiler (gcc/clang) → Executable
```

## 🔍 Breakdown

| Component    | Role                         |
| ------------ | ---------------------------- |
| CMake        | Generates build instructions |
| Ninja / Make | Executes build               |
| gcc / clang  | Compiles code                |

---

# 3️⃣ ⚙️ Install Everything (Windows)

## Step 1: Install CMake

Download from:
👉 https://cmake.org/download/

✔ Choose:

* Windows x64 Installer (.msi)

✔ During install:

* ✅ Add CMake to PATH

---

## Step 2: Install Compiler

### Option A: MinGW (recommended)

Download from:
👉 https://www.mingw-w64.org/

Or use MSYS2:
👉 https://www.msys2.org/

Install:

```bash
pacman -S mingw-w64-x86_64-gcc
```

---

## Step 3: Install Ninja (optional but recommended)

Download:
👉 https://github.com/ninja-build/ninja/releases

Or via Chocolatey:

```bash
choco install ninja
```

---

## Step 4: Verify Installation

```bash
cmake --version
gcc --version
ninja --version
```

---

# 4️⃣ 🚀 First CMake Project

## Folder Structure

```
hello_project/
├── CMakeLists.txt
└── main.c
```

---

## main.c

```c
#include <stdio.h>

int main() {
    printf("Hello from CMake!\n");
    return 0;
}
```

---

## CMakeLists.txt

```cmake
cmake_minimum_required(VERSION 3.10)

project(HelloProject C)

add_executable(hello main.c)
```

---

## Build (Recommended Method)

```bash
cmake -S . -B build
cmake --build build
```

Run:

```bash
build\hello.exe
```

---

# 5️⃣ ⚔️ Using Different Generators

## 🔹 Using Make (Unix Makefiles)

```bash
cmake -S . -B build -G "Unix Makefiles"
cmake --build build
```

---

## 🔹 Using Ninja (Recommended)

```bash
cmake -S . -B build -G Ninja
cmake --build build
```

---

## 📊 Comparison

| Feature     | Make   | Ninja   |
| ----------- | ------ | ------- |
| Speed       | Medium | Fast ⚡  |
| Complexity  | Higher | Simpler |
| Recommended | ❌      | ✅       |

---

# 6️⃣ 📁 Multi-file C Project (Real Example)

## Project Structure

```
my_project/
├── CMakeLists.txt
├── include/
│   └── math_utils.h
└── src/
    ├── main.c
    └── math_utils.c
```

---

## include/math_utils.h

```c
#ifndef MATH_UTILS_H
#define MATH_UTILS_H

int add(int a, int b);

#endif
```

---

## src/math_utils.c

```c
#include "math_utils.h"

int add(int a, int b) {
    return a + b;
}
```

---

## src/main.c

```c
#include <stdio.h>
#include "math_utils.h"

int main() {
    int result = add(5, 3);
    printf("Result: %d\n", result);
    return 0;
}
```

---

## CMakeLists.txt

```cmake
cmake_minimum_required(VERSION 3.10)

project(MyProject C)

add_executable(my_app
    src/main.c
    src/math_utils.c
)

target_include_directories(my_app PRIVATE include)
```

---

## Build

```bash
cmake -S . -B build -G Ninja
cmake --build build
```

Run:

```bash
build\my_app.exe
```

---

# 7️⃣ 📦 Using Libraries in CMake

## CMakeLists.txt (Library Version)

```cmake
cmake_minimum_required(VERSION 3.10)

project(MyProject C)

add_library(math_utils src/math_utils.c)

target_include_directories(math_utils PUBLIC include)

add_executable(my_app src/main.c)

target_link_libraries(my_app PRIVATE math_utils)
```

---

# 8️⃣ 🧾 CMake Command Cheat Sheet

## Configure

```bash
cmake -S . -B build
```

## Build

```bash
cmake --build build
```

## Clean (manual)

```bash
rmdir /s /q build
```

## Specify Generator

```bash
cmake -S . -B build -G Ninja
cmake -S . -B build -G "Unix Makefiles"
```

## Debug Build

```bash
cmake -S . -B build -DCMAKE_BUILD_TYPE=Debug
```

## Release Build

```bash
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
```

---

# 9️⃣ 🧪 Debug vs Release

| Mode    | Use                         |
| ------- | --------------------------- |
| Debug   | Debugging (slow, more info) |
| Release | Optimized (fast)            |

---

# 🔟 ⚠️ Common Mistakes

### ❌ Building inside source folder

✔ Always use `build/`

---

### ❌ Missing source files

```cmake
add_executable(app main.c math_utils.c)
```

---

### ❌ Headers not found

```cmake
target_include_directories(app PRIVATE include)
```

---

### ❌ Wrong generator confusion

Always specify:

```bash
cmake -S . -B build -G Ninja
```

---

# 1️⃣1️⃣ 🧠 Best Workflow (Recommended)

```bash
cmake -S . -B build -G Ninja
cmake --build build
build\my_app.exe
```

---

# 🎯 Final Summary

* **CMake** → generates build system
* **Ninja / Make** → builds code
* **gcc / clang** → compiles code

---

# 📌 Tip

👉 Always think:

> “CMake prepares → Ninja builds → Compiler compiles”

---

# 1️⃣2️⃣ Complete CMake Commands Reference

This section is a practical notebook of the most useful CMake commands, from the basics to more advanced project setup.

---

## A. Basic CMake File Commands

### `cmake_minimum_required`

Defines the minimum CMake version required.

```cmake
cmake_minimum_required(VERSION 3.10)
```

Example:

```cmake
cmake_minimum_required(VERSION 3.10)
project(MyProject C)
```

---

### `project`

Defines the project name and languages used.

```cmake
project(MyProject C)
```

You can also specify version and description:

```cmake
project(MyProject VERSION 1.0 DESCRIPTION "My C project" LANGUAGES C)
```

---

### `add_executable`

Creates an executable program.

```cmake
add_executable(my_app main.c)
```

With multiple source files:

```cmake
add_executable(my_app
    src/main.c
    src/math_utils.c
    src/file_utils.c
)
```

---

### `add_library`

Creates a library.

#### Static library

```cmake
add_library(math_utils STATIC src/math_utils.c)
```

#### Shared library

```cmake
add_library(math_utils SHARED src/math_utils.c)
```

#### Default type

```cmake
add_library(math_utils src/math_utils.c)
```

---

## B. Include and Linking Commands

### `target_include_directories`

Tells the compiler where header files are located.

```cmake
target_include_directories(my_app PRIVATE include)
```

Scopes:

* `PRIVATE` → used only by this target
* `PUBLIC` → used by this target and targets linking to it
* `INTERFACE` → only for dependents

Example:

```cmake
target_include_directories(math_utils PUBLIC include)
```

---

### `target_link_libraries`

Links a target with a library.

```cmake
target_link_libraries(my_app PRIVATE math_utils)
```

Example with system library:

```cmake
target_link_libraries(my_app PRIVATE m)
```

---

### `link_directories`

Adds library search paths. Older style; use carefully.

```cmake
link_directories(path/to/libs)
```

Usually better to use full target-based linking instead.

---

## C. Source File and Target Control

### `target_sources`

Adds source files to an existing target.

```cmake
target_sources(my_app PRIVATE src/extra.c)
```

Example:

```cmake
add_executable(my_app src/main.c)
target_sources(my_app PRIVATE src/math_utils.c src/file_utils.c)
```

---

### `set`

Creates or modifies a variable.

```cmake
set(MY_SOURCES src/main.c src/math_utils.c)
add_executable(my_app ${MY_SOURCES})
```

Example for version numbers:

```cmake
set(PROJECT_VERSION_MAJOR 1)
set(PROJECT_VERSION_MINOR 0)
```

---

### `unset`

Removes a variable.

```cmake
unset(MY_SOURCES)
```

---

## D. Compiler Options and Definitions

### `target_compile_definitions`

Adds preprocessor macros.

```cmake
target_compile_definitions(my_app PRIVATE DEBUG_MODE=1)
```

Example in C code:

```c
#ifdef DEBUG_MODE
printf("Debug mode enabled\n");
#endif
```

---

### `add_definitions`

Older global style for definitions.

```cmake
add_definitions(-DDEBUG_MODE)
```

Target-based commands are preferred.

---

### `target_compile_options`

Adds compiler flags for one target.

```cmake
target_compile_options(my_app PRIVATE -Wall -Wextra)
```

Example:

```cmake
target_compile_options(my_app PRIVATE -Wall -Wextra -Wpedantic)
```

---

### `add_compile_options`

Adds compiler flags globally.

```cmake
add_compile_options(-Wall -Wextra)
```

---

### `set(CMAKE_C_STANDARD ...)`

Sets the C standard.

```cmake
set(CMAKE_C_STANDARD 99)
set(CMAKE_C_STANDARD_REQUIRED ON)
set(CMAKE_C_EXTENSIONS OFF)
```

Example:

```cmake
cmake_minimum_required(VERSION 3.10)
project(MyProject C)

set(CMAKE_C_STANDARD 11)
set(CMAKE_C_STANDARD_REQUIRED ON)
```

---

## E. Build Type and Output Control

### `CMAKE_BUILD_TYPE`

Used to choose Debug, Release, etc.

Command line:

```bash
cmake -S . -B build -DCMAKE_BUILD_TYPE=Debug
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
```

Common values:

* `Debug`
* `Release`
* `RelWithDebInfo`
* `MinSizeRel`

---

### `set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ...)`

Sets where executables go.

```cmake
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)
```

### `set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ...)`

Sets where shared libraries go.

```cmake
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
```

### `set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ...)`

Sets where static libraries go.

```cmake
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
```

Example:

```cmake
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
```

---

## F. Project Organization Commands

### `add_subdirectory`

Adds another folder containing its own `CMakeLists.txt`.

Project structure:

```text
my_project/
├── CMakeLists.txt
├── app/
│   ├── CMakeLists.txt
│   └── main.c
└── lib/
    ├── CMakeLists.txt
    ├── math_utils.c
    └── math_utils.h
```

Top-level:

```cmake
add_subdirectory(lib)
add_subdirectory(app)
```

---

### `include`

Includes another CMake script file.

```cmake
include(cmake/common_settings.cmake)
```

Useful for shared settings.

---

### `option`

Creates a user-configurable ON/OFF option.

```cmake
option(ENABLE_TESTS "Build tests" ON)
```

Example:

```cmake
option(ENABLE_DEBUG_LOGS "Enable debug logs" OFF)

if(ENABLE_DEBUG_LOGS)
    target_compile_definitions(my_app PRIVATE DEBUG_LOGS=1)
endif()
```

Command line:

```bash
cmake -S . -B build -DENABLE_DEBUG_LOGS=ON
```

---

## G. Conditional Logic Commands

### `if / elseif / else / endif`

```cmake
if(WIN32)
    message(STATUS "Building on Windows")
elseif(UNIX)
    message(STATUS "Building on Unix")
else()
    message(STATUS "Unknown platform")
endif()
```

---

### `message`

Prints text during configuration.

```cmake
message(STATUS "Configuring project...")
message(WARNING "This is a warning")
message(FATAL_ERROR "This stops configuration")
```

Types:

* `STATUS`
* `WARNING`
* `AUTHOR_WARNING`
* `FATAL_ERROR`

---

### `foreach`

Loops through a list.

```cmake
set(FILES main.c math_utils.c file_utils.c)

foreach(file ${FILES})
    message(STATUS "Source file: ${file}")
endforeach()
```

---

### `while`

Loop while a condition is true.

```cmake
set(COUNT 1)
while(COUNT LESS 4)
    message(STATUS "Count = ${COUNT}")
    math(EXPR COUNT "${COUNT} + 1")
endwhile()
```

---

## H. File and Path Commands

### `file`

Works with files and directories.

#### Read file

```cmake
file(READ myfile.txt CONTENT)
```

#### Write file

```cmake
file(WRITE output.txt "Hello")
```

#### Append file

```cmake
file(APPEND output.txt "\nMore text")
```

#### Copy files

```cmake
file(COPY assets DESTINATION ${CMAKE_BINARY_DIR})
```

#### Create directory

```cmake
file(MAKE_DIRECTORY ${CMAKE_BINARY_DIR}/generated)
```

---

### `configure_file`

Copies a file and optionally replaces variables.

Example template `config.h.in`:

```c
#define PROJECT_NAME "@PROJECT_NAME@"
#define PROJECT_VERSION "@PROJECT_VERSION@"
```

In CMake:

```cmake
configure_file(config.h.in config.h @ONLY)
```

This generates `config.h`.

---

## I. Finding Packages and External Libraries

### `find_package`

Finds installed packages/libraries.

```cmake
find_package(OpenSSL REQUIRED)
```

Example use:

```cmake
find_package(OpenSSL REQUIRED)
target_link_libraries(my_app PRIVATE OpenSSL::SSL)
```

---

### `find_library`

Finds a library file.

```cmake
find_library(MATH_LIB m)
```

---

### `find_path`

Finds header file paths.

```cmake
find_path(MYLIB_INCLUDE_DIR mylib.h)
```

---

### `find_program`

Finds an executable tool.

```cmake
find_program(GIT_EXECUTABLE git)
```

---

## J. Testing Commands

### `enable_testing`

Turns on testing support.

```cmake
enable_testing()
```

---

### `add_test`

Adds a test.

```cmake
add_test(NAME MyTest COMMAND my_app)
```

Example:

```cmake
enable_testing()
add_executable(my_app src/main.c)
add_test(NAME RunApp COMMAND my_app)
```

Run tests:

```bash
ctest --test-dir build
```

---

## K. Install Commands

### `install`

Specifies what gets installed.

Install executable:

```cmake
install(TARGETS my_app DESTINATION bin)
```

Install headers:

```cmake
install(FILES include/math_utils.h DESTINATION include)
```

Install a directory:

```cmake
install(DIRECTORY include/ DESTINATION include)
```

Install command:

```bash
cmake --install build
```

Set custom install path:

```bash
cmake --install build --prefix install_dir
```

---

## L. Advanced Target Commands

### `target_link_directories`

Adds link search directories to a specific target.

```cmake
target_link_directories(my_app PRIVATE path/to/libs)
```

---

### `target_precompile_headers`

Used more in C++, but available for advanced setups.

```cmake
target_precompile_headers(my_app PRIVATE stdio.h)
```

Not very common for simple C projects.

---

### `set_target_properties`

Sets advanced properties on a target.

```cmake
set_target_properties(my_app PROPERTIES
    OUTPUT_NAME "myprogram"
    RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin
)
```

---

### `get_target_property`

Reads a target property.

```cmake
get_target_property(APP_TYPE my_app TYPE)
message(STATUS "Target type: ${APP_TYPE}")
```

---

## M. Custom Build Steps

### `add_custom_command`

Adds a custom step to generate files or run commands.

Example:

```cmake
add_custom_command(
    OUTPUT generated.txt
    COMMAND ${CMAKE_COMMAND} -E echo "Generated file" > generated.txt
)
```

---

### `add_custom_target`

Creates a target for custom actions.

```cmake
add_custom_target(print_message ALL
    COMMAND ${CMAKE_COMMAND} -E echo "Building project..."
)
```

---

## N. Useful Built-in Variables

### Common built-in variables

```cmake
${CMAKE_SOURCE_DIR}
${CMAKE_BINARY_DIR}
${CMAKE_CURRENT_SOURCE_DIR}
${CMAKE_CURRENT_BINARY_DIR}
${PROJECT_NAME}
${PROJECT_VERSION}
${CMAKE_C_COMPILER}
${CMAKE_GENERATOR}
${WIN32}
${UNIX}
```

Example:

```cmake
message(STATUS "Source dir: ${CMAKE_SOURCE_DIR}")
message(STATUS "Build dir: ${CMAKE_BINARY_DIR}")
message(STATUS "Compiler: ${CMAKE_C_COMPILER}")
message(STATUS "Generator: ${CMAKE_GENERATOR}")
```

---

## O. Beginner-to-Advanced Command Line CMake Commands

### Configure a project

```bash
cmake -S . -B build
```

### Configure with Ninja

```bash
cmake -S . -B build -G Ninja
```

### Configure with Unix Makefiles

```bash
cmake -S . -B build -G "Unix Makefiles"
```

### Configure Debug build

```bash
cmake -S . -B build -DCMAKE_BUILD_TYPE=Debug
```

### Configure Release build

```bash
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
```

### Build project

```bash
cmake --build build
```

### Build specific configuration

```bash
cmake --build build --config Release
```

### Build with parallel jobs

```bash
cmake --build build --parallel
```

or

```bash
cmake --build build --parallel 4
```

### Install project

```bash
cmake --install build
```

### Run tests

```bash
ctest --test-dir build
```

### Clean build manually

```bash
rmdir /s /q build
```

### Open CMake GUI project folder

```bash
cmake-gui
```

### List available generators

```bash
cmake --help
```

### Show command help

```bash
cmake --help-command add_executable
```

### Show manual

```bash
cmake --help-manual cmake-commands
```

---

## P. Complete Practical Example

```cmake
cmake_minimum_required(VERSION 3.15)

project(MyProject VERSION 1.0 LANGUAGES C)

set(CMAKE_C_STANDARD 11)
set(CMAKE_C_STANDARD_REQUIRED ON)

option(ENABLE_WARNINGS "Enable extra warnings" ON)

add_library(math_utils src/math_utils.c)
target_include_directories(math_utils PUBLIC include)

add_executable(my_app src/main.c)
target_link_libraries(my_app PRIVATE math_utils)

if(ENABLE_WARNINGS)
    target_compile_options(my_app PRIVATE -Wall -Wextra -Wpedantic)
endif()

set_target_properties(my_app PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin
)

enable_testing()
add_test(NAME RunApp COMMAND my_app)

install(TARGETS my_app DESTINATION bin)
install(DIRECTORY include/ DESTINATION include)
```

---

## Q. Final Command Memory Trick

Remember CMake in 3 parts:

### 1. Configure

```bash
cmake -S . -B build
```

### 2. Build

```bash
cmake --build build
```

### 3. Install or Run

```bash
cmake --install build
```

or run the executable:

```bash
build\my_app.exe
```

---

## R. Best Commands to Learn First

Start with these:

```cmake
cmake_minimum_required()
project()
add_executable()
add_library()
target_include_directories()
target_link_libraries()
set()
if()
message()
add_subdirectory()
option()
install()
enable_testing()
add_test()
```

These are enough to build most real beginner and intermediate C projects.
