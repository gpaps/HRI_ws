sudo hamachi login 

cd ~/Desktop/hri_dm
source devel/setup.bash

# init ros
gnome-terminal -- roscore

cd /src/hri_dm/scripts

#py listeners
gnome-terminal -- python3 listen_TaskExec.py
gnome-terminal -- python3 listenerSubscriber.py
#py send once
gnome-terminal -- python3 localSender.py

# this is for conncecting/Subscribing to network, 
# only occures once otherwise comment it out 
gnome-terminal -- python3 sub.py
echo 		Subscribed???Check above!!

# fiware listen's
python3 fiwareFORTH_cleanTest.py

# fiware sends?
gnome-terminal -- python3 forthHRIHealthPost.py
