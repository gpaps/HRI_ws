# generated from genmsg/cmake/pkg-genmsg.cmake.em

message(STATUS "hri_dm: 2 messages, 0 services")

set(MSG_I_FLAGS "-Ihri_dm:/home/gpapo/Desktop/hri_ws/src/hri_dm/msg;-Istd_msgs:/opt/ros/noetic/share/std_msgs/cmake/../msg;-Igeometry_msgs:/opt/ros/noetic/share/geometry_msgs/cmake/../msg")

# Find all generators
find_package(gencpp REQUIRED)
find_package(geneus REQUIRED)
find_package(genlisp REQUIRED)
find_package(gennodejs REQUIRED)
find_package(genpy REQUIRED)

add_custom_target(hri_dm_generate_messages ALL)

# verify that message/service dependencies have not changed since configure



get_filename_component(_filename "/home/gpapo/Desktop/hri_ws/src/hri_dm/msg/HRIDM2TaskExecution.msg" NAME_WE)
add_custom_target(_hri_dm_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "hri_dm" "/home/gpapo/Desktop/hri_ws/src/hri_dm/msg/HRIDM2TaskExecution.msg" "geometry_msgs/Vector3:geometry_msgs/Pose2D"
)

get_filename_component(_filename "/home/gpapo/Desktop/hri_ws/src/hri_dm/msg/TaskExecution2HRIDM.msg" NAME_WE)
add_custom_target(_hri_dm_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "hri_dm" "/home/gpapo/Desktop/hri_ws/src/hri_dm/msg/TaskExecution2HRIDM.msg" ""
)

#
#  langs = gencpp;geneus;genlisp;gennodejs;genpy
#

### Section generating for lang: gencpp
### Generating Messages
_generate_msg_cpp(hri_dm
  "/home/gpapo/Desktop/hri_ws/src/hri_dm/msg/HRIDM2TaskExecution.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Vector3.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Pose2D.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/hri_dm
)
_generate_msg_cpp(hri_dm
  "/home/gpapo/Desktop/hri_ws/src/hri_dm/msg/TaskExecution2HRIDM.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/hri_dm
)

### Generating Services

### Generating Module File
_generate_module_cpp(hri_dm
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/hri_dm
  "${ALL_GEN_OUTPUT_FILES_cpp}"
)

add_custom_target(hri_dm_generate_messages_cpp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_cpp}
)
add_dependencies(hri_dm_generate_messages hri_dm_generate_messages_cpp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/gpapo/Desktop/hri_ws/src/hri_dm/msg/HRIDM2TaskExecution.msg" NAME_WE)
add_dependencies(hri_dm_generate_messages_cpp _hri_dm_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/gpapo/Desktop/hri_ws/src/hri_dm/msg/TaskExecution2HRIDM.msg" NAME_WE)
add_dependencies(hri_dm_generate_messages_cpp _hri_dm_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(hri_dm_gencpp)
add_dependencies(hri_dm_gencpp hri_dm_generate_messages_cpp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS hri_dm_generate_messages_cpp)

### Section generating for lang: geneus
### Generating Messages
_generate_msg_eus(hri_dm
  "/home/gpapo/Desktop/hri_ws/src/hri_dm/msg/HRIDM2TaskExecution.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Vector3.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Pose2D.msg"
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/hri_dm
)
_generate_msg_eus(hri_dm
  "/home/gpapo/Desktop/hri_ws/src/hri_dm/msg/TaskExecution2HRIDM.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/hri_dm
)

### Generating Services

### Generating Module File
_generate_module_eus(hri_dm
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/hri_dm
  "${ALL_GEN_OUTPUT_FILES_eus}"
)

add_custom_target(hri_dm_generate_messages_eus
  DEPENDS ${ALL_GEN_OUTPUT_FILES_eus}
)
add_dependencies(hri_dm_generate_messages hri_dm_generate_messages_eus)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/gpapo/Desktop/hri_ws/src/hri_dm/msg/HRIDM2TaskExecution.msg" NAME_WE)
add_dependencies(hri_dm_generate_messages_eus _hri_dm_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/gpapo/Desktop/hri_ws/src/hri_dm/msg/TaskExecution2HRIDM.msg" NAME_WE)
add_dependencies(hri_dm_generate_messages_eus _hri_dm_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(hri_dm_geneus)
add_dependencies(hri_dm_geneus hri_dm_generate_messages_eus)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS hri_dm_generate_messages_eus)

### Section generating for lang: genlisp
### Generating Messages
_generate_msg_lisp(hri_dm
  "/home/gpapo/Desktop/hri_ws/src/hri_dm/msg/HRIDM2TaskExecution.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Vector3.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Pose2D.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/hri_dm
)
_generate_msg_lisp(hri_dm
  "/home/gpapo/Desktop/hri_ws/src/hri_dm/msg/TaskExecution2HRIDM.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/hri_dm
)

### Generating Services

### Generating Module File
_generate_module_lisp(hri_dm
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/hri_dm
  "${ALL_GEN_OUTPUT_FILES_lisp}"
)

add_custom_target(hri_dm_generate_messages_lisp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_lisp}
)
add_dependencies(hri_dm_generate_messages hri_dm_generate_messages_lisp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/gpapo/Desktop/hri_ws/src/hri_dm/msg/HRIDM2TaskExecution.msg" NAME_WE)
add_dependencies(hri_dm_generate_messages_lisp _hri_dm_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/gpapo/Desktop/hri_ws/src/hri_dm/msg/TaskExecution2HRIDM.msg" NAME_WE)
add_dependencies(hri_dm_generate_messages_lisp _hri_dm_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(hri_dm_genlisp)
add_dependencies(hri_dm_genlisp hri_dm_generate_messages_lisp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS hri_dm_generate_messages_lisp)

### Section generating for lang: gennodejs
### Generating Messages
_generate_msg_nodejs(hri_dm
  "/home/gpapo/Desktop/hri_ws/src/hri_dm/msg/HRIDM2TaskExecution.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Vector3.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Pose2D.msg"
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/hri_dm
)
_generate_msg_nodejs(hri_dm
  "/home/gpapo/Desktop/hri_ws/src/hri_dm/msg/TaskExecution2HRIDM.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/hri_dm
)

### Generating Services

### Generating Module File
_generate_module_nodejs(hri_dm
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/hri_dm
  "${ALL_GEN_OUTPUT_FILES_nodejs}"
)

add_custom_target(hri_dm_generate_messages_nodejs
  DEPENDS ${ALL_GEN_OUTPUT_FILES_nodejs}
)
add_dependencies(hri_dm_generate_messages hri_dm_generate_messages_nodejs)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/gpapo/Desktop/hri_ws/src/hri_dm/msg/HRIDM2TaskExecution.msg" NAME_WE)
add_dependencies(hri_dm_generate_messages_nodejs _hri_dm_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/gpapo/Desktop/hri_ws/src/hri_dm/msg/TaskExecution2HRIDM.msg" NAME_WE)
add_dependencies(hri_dm_generate_messages_nodejs _hri_dm_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(hri_dm_gennodejs)
add_dependencies(hri_dm_gennodejs hri_dm_generate_messages_nodejs)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS hri_dm_generate_messages_nodejs)

### Section generating for lang: genpy
### Generating Messages
_generate_msg_py(hri_dm
  "/home/gpapo/Desktop/hri_ws/src/hri_dm/msg/HRIDM2TaskExecution.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Vector3.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Pose2D.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/hri_dm
)
_generate_msg_py(hri_dm
  "/home/gpapo/Desktop/hri_ws/src/hri_dm/msg/TaskExecution2HRIDM.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/hri_dm
)

### Generating Services

### Generating Module File
_generate_module_py(hri_dm
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/hri_dm
  "${ALL_GEN_OUTPUT_FILES_py}"
)

add_custom_target(hri_dm_generate_messages_py
  DEPENDS ${ALL_GEN_OUTPUT_FILES_py}
)
add_dependencies(hri_dm_generate_messages hri_dm_generate_messages_py)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/gpapo/Desktop/hri_ws/src/hri_dm/msg/HRIDM2TaskExecution.msg" NAME_WE)
add_dependencies(hri_dm_generate_messages_py _hri_dm_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/gpapo/Desktop/hri_ws/src/hri_dm/msg/TaskExecution2HRIDM.msg" NAME_WE)
add_dependencies(hri_dm_generate_messages_py _hri_dm_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(hri_dm_genpy)
add_dependencies(hri_dm_genpy hri_dm_generate_messages_py)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS hri_dm_generate_messages_py)



if(gencpp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/hri_dm)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/hri_dm
    DESTINATION ${gencpp_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_cpp)
  add_dependencies(hri_dm_generate_messages_cpp std_msgs_generate_messages_cpp)
endif()
if(TARGET geometry_msgs_generate_messages_cpp)
  add_dependencies(hri_dm_generate_messages_cpp geometry_msgs_generate_messages_cpp)
endif()

if(geneus_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/hri_dm)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/hri_dm
    DESTINATION ${geneus_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_eus)
  add_dependencies(hri_dm_generate_messages_eus std_msgs_generate_messages_eus)
endif()
if(TARGET geometry_msgs_generate_messages_eus)
  add_dependencies(hri_dm_generate_messages_eus geometry_msgs_generate_messages_eus)
endif()

if(genlisp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/hri_dm)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/hri_dm
    DESTINATION ${genlisp_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_lisp)
  add_dependencies(hri_dm_generate_messages_lisp std_msgs_generate_messages_lisp)
endif()
if(TARGET geometry_msgs_generate_messages_lisp)
  add_dependencies(hri_dm_generate_messages_lisp geometry_msgs_generate_messages_lisp)
endif()

if(gennodejs_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/hri_dm)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/hri_dm
    DESTINATION ${gennodejs_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_nodejs)
  add_dependencies(hri_dm_generate_messages_nodejs std_msgs_generate_messages_nodejs)
endif()
if(TARGET geometry_msgs_generate_messages_nodejs)
  add_dependencies(hri_dm_generate_messages_nodejs geometry_msgs_generate_messages_nodejs)
endif()

if(genpy_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/hri_dm)
  install(CODE "execute_process(COMMAND \"/usr/bin/python3\" -m compileall \"${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/hri_dm\")")
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/hri_dm
    DESTINATION ${genpy_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_py)
  add_dependencies(hri_dm_generate_messages_py std_msgs_generate_messages_py)
endif()
if(TARGET geometry_msgs_generate_messages_py)
  add_dependencies(hri_dm_generate_messages_py geometry_msgs_generate_messages_py)
endif()
