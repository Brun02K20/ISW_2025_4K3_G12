# Excepciones de dominio para el parque de diversiones
# Estas excepciones representan reglas de negocio violadas


class ExcepcionDominio(Exception):
    """Excepción base para todas las excepciones del dominio"""
    pass


class CupoInsuficienteError(ExcepcionDominio):
    """Se lanza cuando no hay suficiente cupo disponible para la actividad"""

    def __init__(self, cupo_disponible: int, cupo_solicitado: int):
        self.cupo_disponible = cupo_disponible
        self.cupo_solicitado = cupo_solicitado
        super().__init__(
            f"No hay suficiente cupo disponible. Disponible: {cupo_disponible}, Solicitado: {cupo_solicitado}"
        )


class TerminosNoAceptadosError(ExcepcionDominio):
    """Se lanza cuando el usuario no acepta los términos y condiciones"""

    def __init__(self):
        super().__init__("Debe aceptar los términos y condiciones para poder inscribirse")


class HorarioNoEncontradoError(ExcepcionDominio):
    """Se lanza cuando se intenta acceder a un horario que no existe"""

    def __init__(self, id_horario: int):
        self.id_horario = id_horario
        super().__init__(f"El horario con ID {id_horario} no fue encontrado")


class VisitanteNoEncontradoError(ExcepcionDominio):
    """Se lanza cuando se intenta inscribir a un visitante que no existe"""

    def __init__(self, nombre_visitante: str):
        self.nombre_visitante = nombre_visitante
        super().__init__(f"El visitante '{nombre_visitante}' no fue encontrado en el sistema")


class ActividadNoEncontradaError(ExcepcionDominio):
    """Se lanza cuando se intenta acceder a una actividad que no existe"""

    def __init__(self, id_actividad: int):
        self.id_actividad = id_actividad
        super().__init__(f"La actividad con ID {id_actividad} no fue encontrada")


class EstadoHorarioInvalidoError(ExcepcionDominio):
    """Se lanza cuando el estado del horario no permite inscripciones"""

    def __init__(self, estado_actual: str):
        self.estado_actual = estado_actual
        super().__init__(f"El horario tiene un estado '{estado_actual}' que no permite inscripciones")


class InscripcionDuplicadaError(ExcepcionDominio):
    """Se lanza cuando un visitante ya está inscrito en un horario"""

    def __init__(self, id_visitante: int, id_horario: int):
        self.id_visitante = id_visitante
        self.id_horario = id_horario
        super().__init__(f"El visitante ID {id_visitante} ya está inscrito en el horario ID {id_horario}")