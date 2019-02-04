#! /bin/bash

clear
echo "The face application starts now"

#xterm -title "Camera 1" -e "./docker_miller_git.sh 0"
#xterm -title "Camera 1" -e "./docker_miller_git.sh 1"

./docker_miller_git.sh 0 & ./docker_miller_git.sh 1  
