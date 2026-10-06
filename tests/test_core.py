import pytest

from taskflow import GestorTareas


def test_agregar_asigna_ids_consecutivos():
    gestor = GestorTareas()
    primera = gestor.agregar("A")
    segunda = gestor.agregar("B")
    assert (primera.id, segunda.id) == (1, 2)


def test_agregar_rechaza_titulo_vacio():
    with pytest.raises(ValueError):
        GestorTareas().agregar("   ")


def test_agregar_rechaza_prioridad_invalida():
    with pytest.raises(ValueError):
        GestorTareas().agregar("Tarea", prioridad="urgente")


def test_completar_marca_la_tarea():
    gestor = GestorTareas()
    gestor.agregar("A")
    assert gestor.completar(1).completada is True


def test_listar_solo_pendientes():
    gestor = GestorTareas()
    gestor.agregar("A")
    gestor.agregar("B")
    gestor.completar(1)
    assert [t.titulo for t in gestor.listar(solo_pendientes=True)] == ["B"]


def test_buscar_inexistente_lanza_error():
    with pytest.raises(KeyError):
        GestorTareas().buscar(99)


def test_eliminar_quita_la_tarea():
    gestor = GestorTareas()
    gestor.agregar("A")
    gestor.agregar("B")
    gestor.eliminar(1)
    assert [t.id for t in gestor.listar()] == [2]


def test_eliminar_no_reutiliza_ids():
    gestor = GestorTareas()
    gestor.agregar("A")
    gestor.eliminar(1)
    assert gestor.agregar("B").id == 2


def test_eliminar_inexistente_lanza_error():
    with pytest.raises(KeyError):
        GestorTareas().eliminar(42)