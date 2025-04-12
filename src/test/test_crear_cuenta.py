import pytest
from src.main import GestorUsuario

# 🟢 Casos normales de creación de usuario
def test_crear_usuario_normal():
    gestor = GestorUsuario()
    gestor.crear_cuenta({"id_usuario": "juanitoalimaña", "contraseña": "abc12345"})
    assert "juanitoalimaña" in gestor.usuarios

def test_crear_usuario_con_caracteres_especiales():
    gestor = GestorUsuario()
    gestor.crear_cuenta({"id_usuario": "maria99#*", "contraseña": "pass98765"})
    assert "maria99#*" in gestor.usuarios

def test_crear_usuario_con_minimo_caracteres():
    gestor = GestorUsuario()
    gestor.crear_cuenta({"id_usuario": "usr", "contraseña": "abc45678"})
    assert "usr" in gestor.usuarios

# 🔴 Casos error de creación de usuario 

def test_crear_usuario_existente():
    gestor = GestorUsuario()
    gestor.crear_cuenta({"id_usuario": "juan23", "contraseña": "abc12345"})
    with pytest.raises(ValueError, match="El usuario ya existe"):
        gestor.crear_cuenta({"id_usuario": "juan23", "contraseña": "nueva1234"})

def test_crear_usuario_contraseña_sin_numeros():
    gestor = GestorUsuario()
    with pytest.raises(ValueError, match="La contraseña debe tener al menos 7 caracteres y 2 números"):
        gestor.crear_cuenta({"id_usuario": "nuevoUser", "contraseña": "abcdefg"})

def test_crear_usuario_demasiado_corto():
    gestor = GestorUsuario()
    with pytest.raises(ValueError, match="El nombre de usuario debe tener al menos 3 caracteres"):
        gestor.crear_cuenta({"id_usuario": "ab", "contraseña": "ab123456"})

# 🟡 Casos extremos de creación de usuario

def test_crear_usuario_nombre_extremadamente_largo():
    gestor = GestorUsuario()
    gestor.crear_cuenta({"id_usuario": "usuario_muy_muy_demasiado_demasiadisimo_largo_12345", "contraseña": "longpass99"})
    assert "usuario_muy_muy_demasiado_demasiadisimo_largo_12345" in gestor.usuarios

def test_crear_usuario_vacio():
    gestor = GestorUsuario()
    with pytest.raises(ValueError):
        gestor.crear_cuenta({"id_usuario": "", "contraseña": ""})

def test_crear_usuario_contraseña_minima_valida():
    gestor = GestorUsuario()
    gestor.crear_cuenta({"id_usuario": "usuarioOK", "contraseña": "ab12cd34"})
    assert "usuarioOK" in gestor.usuarios
