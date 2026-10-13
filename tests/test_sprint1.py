import pytest

from taskflow import GestorTareas


@pytest.fixture
def gestor():
    g = GestorTareas()
    g.agregar("Preparar demo", "alta")
    g.agregar("Escribir README", "media")
    g.agregar("Revisar PR de la pareja", "alta")
    return g


# TF-8 Filtrar por prioridad
def test_filtrar_por_prioridad(gestor):
    titulos = [t.titulo for t in gestor.filtrar_por_prioridad("alta")]
    assert titulos == ["Preparar demo", "Revisar PR de la pareja"]


def test_filtrar_prioridad_sin_resultados(gestor):
    assert gestor.filtrar_por_prioridad("baja") == []


def test_filtrar_prioridad_invalida(gestor):
    with pytest.raises(ValueError):
        gestor.filtrar_por_prioridad("urgente")


# TF-9 Buscar por texto
def test_buscar_texto_ignora_mayusculas(gestor):
    assert [t.id for t in gestor.buscar_texto("readme")] == [2]


def test_buscar_texto_vacio(gestor):
    with pytest.raises(ValueError):
        gestor.buscar_texto("  ")


# TF-10 Resumen de avance
def test_resumen(gestor):
    gestor.completar(1)
    assert gestor.resumen() == {"total": 3, "completadas": 1, "pendientes": 2, "avance": 33}


def test_resumen_sin_tareas():
    assert GestorTareas().resumen()["avance"] == 0


# TF-11 Bug: títulos duplicados
def test_no_permite_titulos_duplicados(gestor):
    with pytest.raises(ValueError):
        gestor.agregar("  preparar DEMO ")