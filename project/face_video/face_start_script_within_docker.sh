#! /bin/bash

clear
echo "The face_start_script_within_docker starts now"

#cd /root/openface/demos/web/project/face_video
#workon facecourse-py2
cd /root/openface/demos/web/project/face_video

/root/.virtualenvs/facecourse-py2/bin/python fastWebcamFLD.py $*
