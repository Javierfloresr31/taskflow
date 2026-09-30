"""Demo del proyecto. Ejecutar con: python -m taskflow"""
from taskflow import GestorTareas, __version__


def main():
    gestor = GestorTareas()
    gestor.agregar("Configurar el repositorio en GitHub", "alta")
    gestor.agregar("Escribir el README", "media")
    gestor.agregar("Repasar el material de la clase", "baja")
    gestor.completar(1)

    print(f"TaskFlow v{__version__}")
    for tarea in gestor.listar():
        estado = "[x]" if tarea.completada else "[ ]"
        print(f"  {estado} #{tarea.id} {tarea.titulo} ({tarea.prioridad})")


if __name__ == "__main__":
    main()