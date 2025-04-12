import pytest
from src.main import GestorUsuario

@pytest.fixture
def gestor():
    gestor = GestorUsuario()
    gestor.crear_cuenta({"id_usuario": "juan23", "contraseña": "abc12345"})
    gestor.crear_cuenta({"id_usuario": "maria99", "contraseña": "pass98765"})
    gestor.crear_cuenta({"id_usuario": "usr", "contraseña": "abc45678"})
    return gestor

# 🟢 Casos Normales
def test_cambiar_contraseña_normal_1(gestor):
    gestor.cambiar_contraseña({"id_usuario": "juan23", "nueva_contraseña": "newpass99"})
    assert gestor.usuarios["juan23"].contraseña == "newpass99"

def test_cambiar_contraseña_normal_2(gestor):
    gestor.cambiar_contraseña({"id_usuario": "maria99", "nueva_contraseña": "secure4567"})
    assert gestor.usuarios["maria99"].contraseña == "secure4567"

def test_cambiar_contraseña_normal_3(gestor):
    gestor.cambiar_contraseña({"id_usuario": "usr", "nueva_contraseña": "zxcvbn789"})
    assert gestor.usuarios["usr"].contraseña == "zxcvbn789"

# 🔴 Casos de Error
def test_cambiar_contraseña_none(gestor):
    with pytest.raises(ValueError, match="La contraseña debe tener al menos 7 caracteres y 2 números"):
        gestor.cambiar_contraseña({"id_usuario": "juan23", "nueva_contraseña": None})

def test_cambiar_contraseña_usuario_no_existe(gestor):
    with pytest.raises(ValueError, match="Usuario no encontrado"):
        gestor.cambiar_contraseña({"id_usuario": "usuario_inexistente", "nueva_contraseña": "newpass99"})

def test_cambiar_contraseña_sin_numeros(gestor):
    with pytest.raises(ValueError, match="La contraseña debe tener al menos 7 caracteres y 2 números"):
        gestor.cambiar_contraseña({"id_usuario": "maria99", "nueva_contraseña": "abcdefg"})

# 🟡 Casos Extremos
def test_cambiar_contraseña_usuario_largo(gestor):
    gestor.crear_cuenta({"id_usuario": "usuario_muy_muy_largo_12345", "contraseña": "longpass99"})
    gestor.cambiar_contraseña({"id_usuario": "usuario_muy_muy_largo_12345", "nueva_contraseña": "88NewPass"})
    assert gestor.usuarios["usuario_muy_muy_largo_12345"].contraseña == "88NewPass"

def test_cambiar_contraseña_solo_numeros(gestor):
    gestor.cambiar_contraseña({"id_usuario": "usr", "nueva_contraseña": "87654321"})
    assert gestor.usuarios["usr"].contraseña == "87654321"

def test_cambiar_contraseña_minima_valida(gestor):
    gestor.cambiar_contraseña({"id_usuario": "maria99", "nueva_contraseña": "abc99999"})
    assert gestor.usuarios["maria99"].contraseña == "abc99999"
