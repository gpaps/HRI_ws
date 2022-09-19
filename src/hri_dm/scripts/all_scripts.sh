sudo hamachi login       # connect2vpn

cd ~/Desktop/hri_dm     # path to main DIR,
source devel/setup.bash # activate ROS environment

# initialize ROS
gnome-terminal -- roscore

# path to Python Sripts
cd /src/hri_dm/scripts

# this is for connecting/Subscribing to network,
# only occurs once otherwise comment it out
gnome-terminal -- python3 sub.py
echo 		Subscribed???Check above!!

#py listener2ROS sends2Fiware
gnome-terminal -- python3 listen_TaskExec.py
#py listens2Fiware sends2ROS
gnome-terminal -- python3 listenWFCommand.py

#py send once 3xROS topics, check py for comment's __TEST_SCRIPT__
gnome-terminal -- python3 localSender.py


## fiware sends?
#gnome-terminal -- python3 forthHRIHealthPost.py
