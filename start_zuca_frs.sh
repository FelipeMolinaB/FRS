cd cd face_recognition/app_face_dlib/project/server_udp

sudo screen -dmS server bash -c 'python zuca_server.py -b ZUCA -c 0 -so 1'
echo "Server is active"

sleep 10

cd ../..

sudo screen -dmS entrance0 bash -c './docker_face_computer.sh -c 0 -m 0 -e 1 -so 1'
echo "Upper camera in entrance direction is active"

sudo screen -dmS entrance1 bash -c './docker_face_computer.sh -c 1 -m 0 -e 1 -so 1'
echo "Lower camera in entrance direction is active"

sudo screen -dmS exit0 bash -c './docker_face_computer.sh -c 2 -m 0 -e 0 -so 1'
echo "Upper camera in exit direction is active"

sudo screen -dmS exit1 bash -c './docker_face_computer.sh -c 3 -m 0 -e 0 -so 1'
echo "Lower camera in exit direction is active"
