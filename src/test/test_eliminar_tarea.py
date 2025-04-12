import pytest
from src.main import GestorUsuario, GestorTarea

@pytest.fixture
def gestor():
    gestor = GestorUsuario()
    gestor.crear_cuenta({"id_usuario": "juan23", "contraseña": "abc12345"})
    gestor.crear_cuenta({"id_usuario": "maria99", "contraseña": "pass98765"})
    gestor.crear_cuenta({"id_usuario": "usr", "contraseña": "abc45678"})
    
    gestor_tareas = GestorTarea()
    gestor_tareas.crear_tarea({
        "usuario_creador": "juan23",
        "txt_tarea": "Comprar pan",
        "categoria": "Personal",
        "estado": "Por hacer"
    }, gestor)
    gestor_tareas.crear_tarea({
        "usuario_creador": "maria99",
        "txt_tarea": "Hacer informe",
        "categoria": "Trabajo",
        "estado": "Por hacer"
    }, gestor)
    gestor_tareas.crear_tarea({
        "usuario_creador": "usr",
        "txt_tarea": "Ejercicio",
        "categoria": "Salud",
        "estado": "Por hacer"
    }, gestor)
    
    return gestor, gestor_tareas

# 🟢 Casos Normales
def test_eliminar_tarea_normal_1(gestor):
    gestor, gestor_tareas = gestor
    gestor_tareas.eliminar_tarea({
        "usuario": "juan23",
        "tarea_nombre": "Comprar pan"
    }, gestor)
    assert not any(t.txt_tarea == "Comprar pan" for t in gestor.usuarios["juan23"].tareas)

def test_eliminar_tarea_normal_2(gestor):
    gestor, gestor_tareas = gestor
    gestor_tareas.eliminar_tarea({
        "usuario": "maria99",
        "tarea_nombre": "Hacer informe"
    }, gestor)
    assert not any(t.txt_tarea == "Hacer informe" for t in gestor.usuarios["maria99"].tareas)

def test_eliminar_tarea_normal_3(gestor):
    gestor, gestor_tareas = gestor
    gestor_tareas.eliminar_tarea({
        "usuario": "usr",
        "tarea_nombre": "Ejercicio"
    }, gestor)
    assert not any(t.txt_tarea == "Ejercicio" for t in gestor.usuarios["usr"].tareas)

# 🔴 Casos de Error
def test_eliminar_tarea_usuario_no_existe(gestor):
    gestor, gestor_tareas = gestor
    with pytest.raises(ValueError, match="Usuario no encontrado"):
        gestor_tareas.eliminar_tarea({
            "usuario": "usuario_inexistente",
            "tarea_nombre": "Cualquier tarea"
        }, gestor)

def test_eliminar_tarea_no_existe(gestor):
    gestor, gestor_tareas = gestor
    with pytest.raises(ValueError, match="Tarea no encontrada"):
        gestor_tareas.eliminar_tarea({
            "usuario": "juan23",
            "tarea_nombre": "Tarea inexistente"
        }, gestor)

def test_eliminar_tarea_no_pertenece(gestor):
    gestor, gestor_tareas = gestor
   
    gestor_tareas.crear_tarea({
        "usuario_creador": "usr",
        "txt_tarea": "Solo mía",
        "categoria": "Privada",
        "estado": "Por hacer"
    }, gestor)

    # Intentar eliminarla con otro usuario
    with pytest.raises(ValueError, match="No puedes eliminar una tarea que no te pertenece"):
        gestor_tareas.eliminar_tarea({
            "usuario": "maria99",
            "tarea_nombre": "Solo mía"
        }, gestor)


# 🟡 Casos Extremos
def test_eliminar_tarea_texto_maximo(gestor):
    gestor, gestor_tareas = gestor
    nombre_largo = "A" * 255
    gestor_tareas.crear_tarea({
        "usuario_creador": "juan23",
        "txt_tarea": nombre_largo,
        "categoria": "Trabajo",
        "estado": "Por hacer"
    }, gestor)
    gestor_tareas.eliminar_tarea({
        "usuario": "juan23",
        "tarea_nombre": nombre_largo
    }, gestor)
    assert not any(t.txt_tarea == nombre_largo for t in gestor.usuarios["juan23"].tareas)

def test_eliminar_tarea_categoria_maxima(gestor):
    gestor, gestor_tareas = gestor
    nombre_largo = "Tarea con nombre largo de 50 caracteres"
    gestor_tareas.crear_tarea({
        "usuario_creador": "maria99",
        "txt_tarea": nombre_largo,
        "categoria": "Trabajo",
        "estado": "Por hacer"
    }, gestor)
    gestor_tareas.eliminar_tarea({
        "usuario": "maria99",
        "tarea_nombre": nombre_largo
    }, gestor)
    assert not any(t.txt_tarea == nombre_largo for t in gestor.usuarios["maria99"].tareas)

def test_eliminar_tarea_ultima(gestor):
    gestor, gestor_tareas = gestor
    gestor_tareas.eliminar_tarea({
        "usuario": "usr",
        "tarea_nombre": "Ejercicio"
    }, gestor)
    assert len(gestor.usuarios["usr"].tareas) == 0
