cmake_minimum_required(VERSION 3.10)
project(BFS01)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

include_directories(include)

# Archivos fuente (cada uno se agrega cuando esa persona entrega su parte)
set(BFS01_SOURCES
    src/bfs01/graph_core.cpp
    src/bfs01/init.cpp
    src/bfs01/bfs01.cpp
)

# Test de la infraestructura (no depende de init/bfs01 todavia)
add_executable(test_infra tests/test_infra.cpp src/bfs01/graph_core.cpp)

# Test de initBFS01 (no depende de bfs01 todavia)
add_executable(test_init tests/test_init.cpp src/bfs01/graph_core.cpp src/bfs01/init.cpp)

# Test del algoritmo completo (Persona 2)
add_executable(test_bfs01 tests/test_bfs01.cpp ${BFS01_SOURCES})

# Ejecutable final: se habilita cuando esten demo_cases.cpp y main.cpp
# add_executable(bfs01_demo src/demo_cases.cpp src/main.cpp ${BFS01_SOURCES})

# Configuración de compilación
if(MSVC)
    target_compile_options(test_infra PRIVATE /W4)
    target_compile_options(test_init PRIVATE /W4)
    target_compile_options(test_bfs01 PRIVATE /W4)
else()
    target_compile_options(test_infra PRIVATE -Wall -Wextra -Wpedantic)
    target_compile_options(test_init PRIVATE -Wall -Wextra -Wpedantic)
    target_compile_options(test_bfs01 PRIVATE -Wall -Wextra -Wpedantic)
endif()
