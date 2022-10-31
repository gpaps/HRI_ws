#### VPN OMITTED ##################################################
#sudo hamachi login       # connect2vpn
###################################################################

#### Initialize ROS ###############################################
cd ~/Desktop/hri_ws1    # path to main DIR,
source ~/Desktop/hri_ws1/devel/setup.bash # activate ROS environment
gnome-terminal -- roscore
###################################################################

########## Path to Python Scripts##################################
cd ~/Desktop/hri_ws1/src/hri_dm/scripts

################# Subscription #####################################
# These are for Connecting/Subscribing to Network,
# Only occurs ONCE, otherwise comment it out
#gnome-terminal -- python3 sub.py
#gnome-terminal -- python3 mix_sub.py
#echo 		Subscribed???Check above!!
####################################################################

#py listener2ROS sends2Fiware
gnome-terminal -- python3 listen_TaskExec.py
#py listens2Fiware sends2ROS
gnome-terminal -- python3 listen_WFCommand.py m

################## For Debug Script ################################
#py send once 3xROS topics, check py for comment's __TEST_SCRIPT__
#gnome-terminal -- python3 localSender.py
####################################################################


################# fiware sends? ####################################
gnome-terminal -- python3 forthHRIHealthPost.py
####################################################################
