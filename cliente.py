import requests

# URL base del servidor Flask
BASE_URL = "http://localhost:5000"

# Encabezados para enviar datos en formato JSON
HEADERS = {"Content-Type": "application/json"}

def obtener_usuarios():
    response = requests.get(f"{BASE_URL}/usuarios")
    
    if response.status_code == 200:
        usuarios = response.json()
        if usuarios:
            print("\n📋 Usuarios registrados:")
            for usuario in usuarios:
                print(f"🆔 ID: {usuario['id']} - 👤 Nombre: {usuario['nombre']}")
        else:
            print("⚠️ No hay usuarios registrados.")
    else:
        print("❌ Error al obtener usuarios.")

def agregar_usuario():
    nombre = input("\nIngrese el nombre del nuevo usuario: ").strip()
    if not nombre:
        print("⚠️ Error: El nombre no puede estar vacío.")
        return

    datos = {"nombre": nombre}
    response = requests.post(f"{BASE_URL}/usuarios", json=datos, headers=HEADERS)  # Agregar headers

    if response.status_code == 201:
        print("✅ Usuario agregado exitosamente.")
    else:
        print(f"❌ Error al agregar usuario: {response.json().get('error', 'Desconocido')}")

def eliminar_usuario():
    usuario_id = input("\nIngrese el ID del usuario a eliminar: ").strip()
    
    if not usuario_id.isdigit():
        print("⚠️ Error: Debe ingresar un número válido.")
        return

    response = requests.delete(f"{BASE_URL}/usuarios/{usuario_id}")

    if response.status_code == 200:
        print("✅ Usuario eliminado exitosamente.")
    else:
        print(f"❌ Error al eliminar usuario: {response.json().get('error', 'Desconocido')}")

def buscar_usuario():
    usuario_id = input("\nIngrese el ID del usuario a buscar: ").strip()
    
    if not usuario_id.isdigit():
        print("⚠️ Error: Debe ingresar un número válido.")
        return

    response = requests.get(f"{BASE_URL}/usuarios/{usuario_id}")

    if response.status_code == 200:
        usuario = response.json()
        print(f"✅ Usuario encontrado: 🆔 ID: {usuario['id']} - 👤 Nombre: {usuario['nombre']}")
    else:
        print(f"❌ Usuario no encontrado: {response.json().get('error', 'Desconocido')}")

if __name__ == "__main__":
    while True:
        print("\n📌 Menú de opciones:")
        print("1️⃣ Obtener usuarios")
        print("2️⃣ Agregar usuario")
        print("3️⃣ Eliminar usuario")
        print("4️⃣ Buscar usuario por ID")
        print("5️⃣ Salir")
        
        opcion = input("\nSeleccione una opción: ").strip()

        if opcion == "1":
            obtener_usuarios()
        elif opcion == "2":
            agregar_usuario()
        elif opcion == "3":
            eliminar_usuario()
        elif opcion == "4":
            buscar_usuario()
        elif opcion == "5":
            print("👋 Saliendo del programa...")
            break
        else:
            print("⚠️ Opción no válida. Intente de nuevo.")
