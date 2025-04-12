from main import GestorTarea, GestorUsuario


ESTADOS_VALIDOS = ["Por hacer", "En progreso", "Completada"]


def menu_principal():
    print("""
  ╔══════════════════════════════╗
  ║     GESTOR DE TAREAS CLI     ║
  ╚══════════════════════════════╝
  1. Crear cuenta
  2. Iniciar sesión
  0. Salir
""")
    return input("Seleccione una opción: ")


def menu_usuario(usuario):
    print(f"""
  ╔══════════════════════════════╗
  ║    Bienvenido, {usuario}        ║
  ╚══════════════════════════════╝
  1. Crear tarea
  2. Ver mis tareas
  3. Editar tarea
  4. Eliminar tarea
  5. Cambiar contraseña
  0. Cerrar sesión
""")
    return input("Seleccione una opción: ")


def mostrar_tareas(usuario_obj):
    if not usuario_obj.tareas:
        print("\n  No tienes tareas registradas.")
        return
    print("\n  Tus tareas:")
    for i, tarea in enumerate(usuario_obj.tareas, 1):
        print(f"  {i}. [{tarea.estado}] {tarea.txt_tarea} - Categoria: {tarea.categoria}")


def run():
    gestor_usuarios = GestorUsuario()
    gestor_tareas = GestorTarea()
    
    while True:
        opcion = menu_principal()

        if opcion == "1":
            try:
                user = input("  Ingrese nombre de usuario: ")
                pwd = input("  Ingrese contraseña: ")
                gestor_usuarios.crear_cuenta({"id_usuario": user, "contraseña": pwd})
                print("  ✅ Cuenta creada exitosamente!")
            except Exception as e:
                print(f"  ❌ Error: {e}")

        elif opcion == "2":
            user = input("  Usuario: ")
            pwd = input("  Contraseña: ")
            try:
                gestor_usuarios.iniciar_sesion({"id_usuario": user, "contraseña": pwd})
                print("  ✅ Inicio de sesión exitoso!")
                while True:
                    opcion_u = menu_usuario(user)

                    if opcion_u == "1":
                        texto = input("  Descripción de la tarea: ")
                        categoria = input("  Categoría: ")

                        print("  Estados disponibles:")
                        for i, estado_op in enumerate(ESTADOS_VALIDOS, 1):
                            print(f"    {i}. {estado_op}")
                        indice = input("  Seleccione un estado (1-3): ")
                        try:
                            estado = ESTADOS_VALIDOS[int(indice) - 1]
                        except (IndexError, ValueError):
                            print("  ❌ Estado inválido.")
                            continue

                        try:
                            gestor_tareas.crear_tarea({
                                "usuario_creador": user,
                                "txt_tarea": texto,
                                "categoria": categoria,
                                "estado": estado
                            }, gestor_usuarios)
                            print("  ✅ Tarea creada!")
                        except Exception as e:
                            print(f"  ❌ Error: {e}")

                    elif opcion_u == "2":
                        mostrar_tareas(gestor_usuarios.usuarios[user])

                    elif opcion_u == "3":
                        mostrar_tareas(gestor_usuarios.usuarios[user])
                        tarea_original = input("  Nombre exacto de la tarea a editar: ")
                        nuevo_texto = input("  Nuevo texto: ")
                        nueva_categoria = input("  Nueva categoría: ")

                        print("  Estados disponibles:")
                        for i, estado_op in enumerate(ESTADOS_VALIDOS, 1):
                            print(f"    {i}. {estado_op}")
                        indice = input("  Seleccione un nuevo estado (1-3): ")
                        try:
                            nuevo_estado = ESTADOS_VALIDOS[int(indice) - 1]
                        except (IndexError, ValueError):
                            print("  ❌ Estado inválido.")
                            continue

                        try:
                            gestor_tareas.editar_tarea({
                                "usuario": user,
                                "tarea_original": tarea_original,
                                "nuevo_texto": nuevo_texto,
                                "nueva_categoria": nueva_categoria,
                                "nuevo_estado": nuevo_estado
                            }, gestor_usuarios)
                            print("  ✅ Tarea actualizada!")
                        except Exception as e:
                            print(f"  ❌ Error: {e}")

                    elif opcion_u == "4":
                        mostrar_tareas(gestor_usuarios.usuarios[user])
                        nombre = input("  Nombre exacto de la tarea a eliminar: ")
                        try:
                            gestor_tareas.eliminar_tarea({
                                "usuario": user,
                                "tarea_nombre": nombre
                            }, gestor_usuarios)
                            print("  ✅ Tarea eliminada!")
                        except Exception as e:
                            print(f"  ❌ Error: {e}")

                    elif opcion_u == "5":
                        nueva_pwd = input("  Nueva contraseña: ")
                        try:
                            gestor_usuarios.cambiar_contraseña({
                                "id_usuario": user,
                                "nueva_contraseña": nueva_pwd
                            })
                            print("  ✅ Contraseña actualizada!")
                        except Exception as e:
                            print(f"  ❌ Error: {e}")

                    elif opcion_u == "0":
                        break

                    else:
                        print("  ❌ Opción no válida.")

            except Exception as e:
                print(f"  ❌ Error: {e}")

        elif opcion == "0":
            print("  👋 Hasta luego!")
            break

        else:
            print("  ❌ Opción no válida.")


if __name__ == "__main__":
    run()