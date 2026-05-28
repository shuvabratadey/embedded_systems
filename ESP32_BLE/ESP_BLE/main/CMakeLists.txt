file(GLOB_RECURSE srcs "main.c")

idf_component_register(SRCS "${srcs}"
                       INCLUDE_DIRS ".")
