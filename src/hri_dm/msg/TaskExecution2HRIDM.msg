# For synchronization
int32 request_id

# True if success; False if not
bool result

# Error type e.g. “null”, “ArmExtFailed”, “ObjLocFailed”, ReachFailed”, “GraspingFailed”, “ArmHomingFailed”, “ArmRecoveryFailed”, “HandOverReachFailed”, “HandOverReleaseFailed”, “NavigationFailed”
string error_type
