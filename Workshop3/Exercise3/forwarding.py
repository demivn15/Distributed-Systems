# Definición inicial de las ubicaciones
locations = {
 "A": "B",
 "B": "C",
 "C": "D",
 "D": "192.168.1.50:5000"
}

# Función de resolución original del taller
def resolve(location):
 hops = 0
 while location in locations:
     print("Following:", location, "->", locations[location])
     location = locations[location]
     hops += 1
 return location, hops

print("--- 1. ANTES DE LA OPTIMIZACIÓN (Cadena Original) ---")
address, hops = resolve("A")
print("Final address:", address)
print("Number of hops:", hops)

print("\n--- 2. DESPUÉS DE LA OPTIMIZACIÓN (Atajo / Shortcut) ---")
# Aquí implementamos la idea de reducción de cadena (atajo)
locations["A"] = address
address_opt, hops_opt = resolve("A")
print("Final address:", address_opt)
print("Number of hops:", hops_opt)

print("\n--- 3. SIMULACIÓN DE FALLO ---")
# Restauramos el puntero de "A" a "B" para volver a la cadena larga
locations["A"] = "B" 
# Simulamos la caída del nodo eliminando "C"
del locations["C"]

# Ejecutamos la cadena original nuevamente
address_fail, hops_fail = resolve("A")
print("Final address:", address_fail)
print("Number of hops:", hops_fail)