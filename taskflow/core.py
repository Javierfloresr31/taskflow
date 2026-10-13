"""Lógica principal de TaskFlow."""
from dataclasses import dataclass

PRIORIDADES = ("baja", "media", "alta")


@dataclass
class Tarea:
    id: int
    titulo: str
    prioridad: str = "media"
    completada: bool = False


class GestorTareas:
    """Guarda las tareas en memoria y aplica las reglas del negocio."""

    def __init__(self):
        self._tareas = []
        self._siguiente_id = 1

    def agregar(self, titulo, prioridad="media"):
        titulo = titulo.strip()

        if not titulo:
            raise ValueError("El título no puede estar vacío")

        # TF-11: impedir títulos duplicados
        titulo_normalizado = titulo.casefold()

        for tarea in self._tareas:
            if tarea.titulo.strip().casefold() == titulo_normalizado:
                raise ValueError(
                    f"Ya existe una tarea con el título: {titulo}"
                )

        if prioridad not in PRIORIDADES:
            raise ValueError(f"Prioridad inválida: {prioridad}")

        tarea = Tarea(self._siguiente_id, titulo, prioridad)
        self._tareas.append(tarea)
        self._siguiente_id += 1
        return tarea

    def completar(self, tarea_id):
        tarea = self.buscar(tarea_id)
        tarea.completada = True
        return tarea

    def listar(self, solo_pendientes=False):
        if solo_pendientes:
            return [t for t in self._tareas if not t.completada]
        return list(self._tareas)

    def buscar(self, tarea_id):
        for tarea in self._tareas:
            if tarea.id == tarea_id:
                return tarea
        raise KeyError(f"No existe la tarea {tarea_id}")

    def eliminar(self, tarea_id):
        tarea = self.buscar(tarea_id)
        self._tareas.remove(tarea)
        return tarea

    # TF-8: filtrar por prioridad
    def filtrar_por_prioridad(self, prioridad):
        if not isinstance(prioridad, str):
            raise ValueError("La prioridad debe ser un texto")

        prioridad = prioridad.strip().lower()

        if prioridad not in PRIORIDADES:
            raise ValueError(f"Prioridad inválida: {prioridad}")

        return [
            tarea for tarea in self._tareas
            if tarea.prioridad == prioridad
        ]

    # TF-9: buscar por texto
    def buscar_texto(self, texto):
        if not isinstance(texto, str) or not texto.strip():
            raise ValueError("El texto de búsqueda no puede estar vacío")

        texto = texto.strip().casefold()

        return [
            tarea for tarea in self._tareas
            if texto in tarea.titulo.casefold()
        ]

    # TF-10: resumen de avance
    def resumen(self):
        total = len(self._tareas)

        completadas = sum(
            1 for tarea in self._tareas if tarea.completada
        )

        pendientes = total - completadas
        avance = round(completadas / total * 100) if total else 0

        return {
            "total": total,
            "completadas": completadas,
            "pendientes": pendientes,
            "avance": avance,
        }
