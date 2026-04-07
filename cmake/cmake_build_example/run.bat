rd /s /q build
cmake -B build -G "Unix Makefiles"
cmake --build build
cd build && Hello.exe
cd ..
pause