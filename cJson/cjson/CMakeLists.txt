cmake_minimum_required(VERSION 3.20.0)
project(app C)
add_executable(app)
target_sources(
    app 
    PRIVATE
    main.c 
    cJSON.c 
    cJSON_Utils.c
)
