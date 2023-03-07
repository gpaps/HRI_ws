# shellcheck disable=SC2164
cd ~/workspace/platform/hri_ws/src/hri_dm/scripts   # Path to Script DIR,

########## Path to Python Scripts##################################
cd ~/Desktop/hri_ws1/src/hri_dm/scripts

################# Subscription #####################################
# These are for Connecting/Subscribing to Network,
# Only occurs ONCE, otherwise comment it out
#gnome-terminal -- python3 mix_sub.py
#echo 		Subscribed???Check above!!
####################################################################

#py listener2ROS sends2Fiware
gnome-terminal -- python3 listen_TaskExec.py
#py listens2Fiware sends2ROS
gnome-terminal -- python3 listen_WFCommand.py m
####################################################################
