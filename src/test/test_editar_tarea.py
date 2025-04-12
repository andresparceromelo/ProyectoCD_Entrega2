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
def test_editar_tarea_normal_1(gestor):
    gestor, gestor_tareas = gestor
    gestor_tareas.editar_tarea({
        "usuario": "juan23",
        "tarea_original": "Comprar pan",
        "nuevo_texto": "Comprar comida",
        "nueva_categoria": "Personal",
        "nuevo_estado": "En progreso"
    }, gestor)
    assert gestor.usuarios["juan23"].tareas[0].txt_tarea == "Comprar comida"

def test_editar_tarea_normal_2(gestor):
    gestor, gestor_tareas = gestor
    gestor_tareas.editar_tarea({
        "usuario": "maria99",
        "tarea_original": "Hacer informe",
        "nuevo_texto": "Terminar informe",
        "nueva_categoria": "Trabajo",
        "nuevo_estado": "Completada"
    }, gestor)
    assert gestor.usuarios["maria99"].tareas[0].txt_tarea == "Terminar informe"

def test_editar_tarea_normal_3(gestor):
    gestor, gestor_tareas = gestor
    gestor_tareas.editar_tarea({
        "usuario": "usr",
        "tarea_original": "Ejercicio",
        "nuevo_texto": "Ir al gimnasio",
        "nueva_categoria": "Salud",
        "nuevo_estado": "Por hacer"
    }, gestor)
    assert gestor.usuarios["usr"].tareas[0].txt_tarea == "Ir al gimnasio"

# 🔴 Casos de Error
def test_editar_tarea_usuario_no_existe(gestor):
    gestor, gestor_tareas = gestor
    with pytest.raises(ValueError, match="Usuario no encontrado"):
        gestor_tareas.editar_tarea({
            "usuario": "usuario_inexistente",
            "tarea_original": "Cualquier tarea",
            "nuevo_texto": "Nuevo texto",
            "nueva_categoria": "Trabajo",
            "nuevo_estado": "Por hacer"
        }, gestor)

def test_editar_tarea_no_existe(gestor):
    gestor, gestor_tareas = gestor
    with pytest.raises(ValueError, match="Tarea no encontrada"):
        gestor_tareas.editar_tarea({
            "usuario": "juan23",
            "tarea_original": "Tarea inexistente",
            "nuevo_texto": "Nuevo texto",
            "nueva_categoria": "Personal",
            "nuevo_estado": "Por hacer"
        }, gestor)

def test_editar_tarea_texto_vacio(gestor):
    gestor, gestor_tareas = gestor
    with pytest.raises(ValueError, match="El texto de la tarea no puede estar vacío"):
        gestor_tareas.editar_tarea({
            "usuario": "maria99",
            "tarea_original": "Hacer informe",
            "nuevo_texto": "",
            "nueva_categoria": "Trabajo",
            "nuevo_estado": "Por hacer"
        }, gestor)

# 🟡 Casos Extremos
def test_editar_tarea_texto_maximo(gestor):
    gestor, gestor_tareas = gestor
    texto_largo = "A" * 255
    gestor_tareas.editar_tarea({
        "usuario": "juan23",
        "tarea_original": "Comprar pan",
        "nuevo_texto": texto_largo,
        "nueva_categoria": "Trabajo",
        "nuevo_estado": "Por hacer"
    }, gestor)
    assert gestor.usuarios["juan23"].tareas[0].txt_tarea == texto_largo

def test_editar_tarea_categoria_maxima(gestor):
    gestor, gestor_tareas = gestor
    categoria_larga = "x" * 50
    gestor_tareas.editar_tarea({
        "usuario": "maria99",
        "tarea_original": "Hacer informe",
        "nuevo_texto": "Leer libros y artículos",
        "nueva_categoria": categoria_larga,
        "nuevo_estado": "Completada"
    }, gestor)
    assert gestor.usuarios["maria99"].tareas[0].categoria == categoria_larga

def test_editar_tarea_estado_maximo(gestor):
    gestor, gestor_tareas = gestor
    estado_largo = "x" * 20
    gestor_tareas.editar_tarea({
        "usuario": "usr",
        "tarea_original": "Ejercicio",
        "nuevo_texto": "Aprender Python",
        "nueva_categoria": "Educación",
        "nuevo_estado": estado_largo
    }, gestor)
    assert gestor.usuarios["usr"].tareas[0].estado == estado_largo
