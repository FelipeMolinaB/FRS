import client_recepcion

raw_input("Press enter to exit")

print ("respuesta del servidor: %s" %client_recepcion.set_door_mode("enable"))
print ("respuesta del servidor: %s" %client_recepcion.set_door_mode("disable"))


raw_input("Press enter to exit")