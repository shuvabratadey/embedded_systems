@REM del run.exe && gcc main.c cJSON.c cJSON_Utils.c -o run && run.exe

rd /s /q build
cmake -B build -G "Unix Makefiles"
cmake --build build
cd build && app.exe
cd ..