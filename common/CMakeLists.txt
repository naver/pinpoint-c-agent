cmake_minimum_required(VERSION 3.2)
project(common)
set(CMAKE_CXX_STANDARD 11)

list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_LIST_DIR}/cmake")

option(AGENT_WITH_PKGCONFIG_SUPPORT "Generate and install .pc files" ON)


set(CMAKE_C_FLAGS   "${CMAKE_C_FLAGS} -Wall -Wextra -fPIC")
set(CMAKE_CXX_FLAGS   "${CMAKE_CXX_FLAGS}  -Wall -Wextra -fPIC")
set(CMAKE_C_FLAGS_DEBUG "${CMAKE_C_FLAGS_DEBUG}   -g3 -O0 -DCOMMON_DEBUG")   
set(CMAKE_C_FLAGS_RELEASE "${CMAKE_C_FLAGS_RELEASE} -DNDEBUG  -O2")
set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG}  -g3 -O0 -DCOMMON_DEBUG")
set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -DNDEBUG  -O2")
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)

option (WITH_TEST_CASE "Enable Gtest" OFF)
option (WITH_CODECOVERAGE "Enable CodeCoverage" OFF)

 if(UNIX AND NOT APPLE)
    set(LINUX_ TRUE)
endif()

if (WITH_CODECOVERAGE AND LINUX_)
    # message("WITH_CODECOVERAGE = ON")
    set(CMAKE_C_FLAGS   "${CMAKE_C_FLAGS} -fprofile-arcs -ftest-coverage")
    set(CMAKE_CXX_FLAGS   "${CMAKE_CXX_FLAGS} -fprofile-arcs -ftest-coverage")
endif()

include_directories("include"
                    "src"
                    "jsoncpp/include")
                    
link_directories(${CMAKE_BINARY_DIR}/lib)

add_subdirectory(jsoncpp)
add_subdirectory(src)

if(UNIX AND NOT APPLE)
    include(GNUInstallDirs)
    add_library(pinpoint_common_shared SHARED $<TARGET_OBJECTS:pinpoint_common_obj> $<TARGET_OBJECTS:jsoncppObj>)  
    install(DIRECTORY include/ DESTINATION include/pinpoint_common
            FILES_MATCHING PATTERN "*.h")

    install(TARGETS pinpoint_common_shared pinpoint_common ${INSTALL_EXPORT}
        RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
        LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
        ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
        OBJECTS DESTINATION ${CMAKE_INSTALL_LIBDIR}
    )
endif()


if (WITH_TEST_CASE)
    include (CTest)
    enable_testing()
    find_package(GTest REQUIRED)
    add_subdirectory(test)
endif(WITH_TEST_CASE)
