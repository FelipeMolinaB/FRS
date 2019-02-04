import client_camera
import client_recepcion
import server_habilitar
#client_camera.request_open_door()
raw_input("Press enter to exit")
#name = "Juancho"
#message =  name
#client_camera.open_door_face(name)
#client_recepcion.set_door_mode("enable")
#client_recepcion.set_door_mode("disable")
server_habilitar_p = server_habilitar.server_habilitar_puerta()
server_habilitar_p.start_service()



raw_input("Press enter to exit")