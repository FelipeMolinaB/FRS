#! /bin/bash

clear
echo "the script starts now"

xhost local:root

#sudo docker run -v /home/miller/Documents/face_course:/root/face_course/ -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=unix$DISPLAY  -t -i camilol/opencv:v11 /bin/bash

#sudo docker run -it --privileged -v /home/miller/Documents/face_course:/root/face_course/ -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=unix$DISPLAY camilol/opencv:v11 /bin/bash

#--add-host="localhost:192.168.56.108" \
#--net="host"\


sudo docker run -it \
  --net="host"\
  --privileged \
  --rm \
	-e DISPLAY=unix$DISPLAY \
  --env="QT_X11_NO_MITSHM=1" \
  --privileged -v /dev/video0:/dev/video0 \
  --privileged -v /dev/video1:/dev/video1 \
  --privileged -v /tmp/.X11-unix:/tmp/.X11-unix:ro  \
	--device /dev/video0 \
	--device /dev/video1 \
	-v /home/miller/Documents/mac_face_computer_backup/app_face_dlib:/root/openface/demos/web\
	-v /home/miller/Documents/mac_face_computer_backup/face_dlib/db/models_per_person/svm_binary/models:/root/openface/demos/web/project/binary_svm_models\
	-v /home/face/Documents/mac_face_computer_backup/face_dlib/db/models_per_person/general_svm:/root/openface/demos/web/project/general_svm\
	camilol/opencv:latest /bin/bash

#-v /media/sf_face_dlib:/root/face_course/\


 #  -v /dev/video0:/dev/video0

#docker run --privileged -it \
#		-v /home/miller/Documents/face_course:/root/face_course/ \
#    --env="DISPLAY" \
#    --env="QT_X11_NO_MITSHM=1" \
#    --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
#		-v /dev/video0:/dev/video0 \
#    camilol/opencv:v11 /bin/bash 



		

#export containerId=$(docker ps -l -q)



#sudo docker commit 50dfef3fd41b  camilol/openface_ubuntu:face_course 
#sudo docker push camilol/openface_ubuntu:face_course




