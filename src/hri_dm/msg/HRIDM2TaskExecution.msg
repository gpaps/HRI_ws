# “pickup“, “navigate”, “handover”, “release”, “reachRecovery”, “graspRecovery”, “homingRecovery”, “navigationRecovery"
string action

# Object to pickup
int32 tool_id

# location for object handover float x, float y, float z
geometry_msgs/Vector3 location

# location for Navigation float x, float y, float theta
geometry_msgs/Pose2D navpos

# For synchronization
int32 request_id
