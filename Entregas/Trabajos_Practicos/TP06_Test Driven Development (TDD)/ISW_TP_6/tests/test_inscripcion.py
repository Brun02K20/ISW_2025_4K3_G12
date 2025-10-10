# test_inscripcion.py
from dataclasses import dataclass
from typing import List, Dict, Optional
import re
import pytest

# --- Dominio mínimo (mock) ---

@dataclass
class Horario:
    hora: str  # "10:00"
    cupos: int
    ocupados: int = 0

    @property
    def disponibles(self) -> int:
        return max(self.cupos - self.ocupados, 0)

@dataclass
class Actividad:
    nombre: str
    horarios: Dict[str, Horario]
    requiere_talle: bool = False
    parque_abierto: bool = True

@dataclass
class Participante:
    nombre: str
    dni: str
    edad: int
    talle: Optional[str] = None  # Solo si la actividad lo requiere

class ValidationError(Exception):
    pass

class FakeRepositorio:
    def __init__(self):
        # 4 actividades del requerimiento (Tirolesa, Safari, Palestra, Jardinería)
        self.actividades = {
            "Tirolesa": Actividad(
                "Tirolesa",
                {
                    "10:00": Horario("10:00", cupos=5),
                    "11:00": Horario("11:00", cupos=0),  # sin cupos
                },
                requiere_talle=True,
                parque_abierto=True,
            ),
            "Safari": Actividad(
                "Safari",
                {
                    "14:00": Horario("14:00", cupos=10),
                    "16:00": Horario("16:00", cupos=10),
                },
                requiere_talle=False,
                parque_abierto=True,
            ),
            "Palestra": Actividad(
                "Palestra",
                {
                    "09:00": Horario("09:00", cupos=2),
                },
                requiere_talle=True,
                parque_abierto=False,  # parque/actividad cerrada para probar caso de falla
            ),
            "Jardinería": Actividad(
                "Jardinería",
                {
                    "15:00": Horario("15:00", cupos=1),
                },
                requiere_talle=False,
                parque_abierto=True,
            ),
        }

class InscripcionService:
    VALID_NAMES = re.compile(r"^[A-Za-zÁÉÍÓÚáéíóúñÑ\s'-]{2,}$")
    VALID_DNI = re.compile(r"^\d{9,10}$")
    VALID_TALLE = re.compile(r"^(XS|S|M|L|XL|XXL|\d{2})$")

    def __init__(self, repo: FakeRepositorio):
        self.repo = repo

    def inscribir(
        self,
        actividad_nombre: Optional[str],
        horario_str: Optional[str],
        cantidad: Optional[int],
        participantes: Optional[List[Participante]],
        acepta_tyc: bool,
    ) -> Dict:
        # Validaciones base
        if not actividad_nombre and not horario_str and not cantidad and not participantes:
            raise ValidationError("Datos de inscripción incompletos")

        if not acepta_tyc:
            raise ValidationError("Debe aceptar términos y condiciones")

        # Actividad válida
        if actividad_nombre not in self.repo.actividades:
            raise ValidationError("Actividad inválida o no disponible")
        actividad = self.repo.actividades[actividad_nombre]

        # Horario de esa actividad
        if horario_str not in actividad.horarios:
            raise ValidationError("Horario no disponible para esta actividad")

        # Parque/actividad disponible
        if not actividad.parque_abierto:
            raise ValidationError("Parque cerrado o actividad no disponible en el horario")

        horario = actividad.horarios[horario_str]

        # Cantidad de personas
        if cantidad is None or cantidad <= 0:
            raise ValidationError("Cantidad de cupo inválida")

        if cantidad > horario.disponibles:
            raise ValidationError("No hay cupos suficientes para el horario seleccionado")

        # Participantes completos
        if not participantes or len(participantes) != cantidad:
            raise ValidationError("Debe registrar todos los participantes")

        # Validación de cada participante
        for p in participantes:
            if not self.VALID_NAMES.match(p.nombre):
                raise ValidationError("Nombre inválido")
            if not self.VALID_DNI.match(p.dni):
                raise ValidationError("DNI inválido")
            if actividad.requiere_talle and not (p.talle and self.VALID_TALLE.match(p.talle)):
                raise ValidationError("Talle requerido y/o inválido")
            if not actividad.requiere_talle and p.talle is not None and not self.VALID_TALLE.match(p.talle):
                raise ValidationError("Talle si se provee debe ser válido")

        # Efecto de inscripción
        horario.ocupados += cantidad
        return {"ok": True, "actividad": actividad_nombre, "horario": horario_str, "inscriptos": cantidad}

# --- Fixtures y helpers ---

@pytest.fixture()
def service():
    return InscripcionService(FakeRepositorio())

def p(nombre="Juan Pérez", dni="123456789", edad=20, talle=None):
    # Nombre, DNI, edad, talle válidos por defecto
    return Participante(nombre=nombre, dni=dni, edad=edad, talle=talle)

# --- TESTS (nombres tal cual pediste) ---

def test_seleccionar_actividad_fuera_valida(service):
    # Escribimos una actividad no válida, y esperamos error
    msj_esperado = "Actividad inválida o no disponible"
    with pytest.raises(ValidationError, match=msj_esperado):
        service.inscribir("Parapente", "09:00", 1, [p()], True)

def test_seleccionar_horario_valido_para_safari(service):
    # Seleccionamos un horario válido para Safari y pasa.
    out = service.inscribir("Safari", "14:00", 1, [p()], True)
    assert out["ok"] is True and out["actividad"] == "Safari" and out["horario"] in ("16:00", "14:00")

def test_seleccionar_horario_dentro_disponible(service):
    "Seleccionamos un horario no disponible (sin cupos) y esperamos error"
    msj_esperado = "No hay cupos suficientes para el horario seleccionado"
    with pytest.raises(ValidationError, match=msj_esperado):
        # Tirolesa a las 11:00 no tiene cupos
        service.inscribir("Tirolesa", "11:00", 1, [p(talle="M")], True)

def test_indicar_cantidad_cupo_no_valido(service):
    msj_esperado = "Cantidad de cupo inválida"
    with pytest.raises(ValidationError, match=msj_esperado):
        # Cupo es negativo o 0
        service.inscribir("Safari", "14:00", 0, [p()], True)

def test_indicar_cantidad_cupos_caracteres_invalidos(service):
    # simulamos "caracteres" invalidando el tipo pasando None
    # Con algun STR también falla por type_Error
    with pytest.raises(ValidationError):
        service.inscribir("Safari", "14:00", None, [p()], True)

def test_indicar_cantidad_personas_valida(service):
    # Safari tiene 10 cupos, probamos con 3 que es válido
    # Cupos 10, inscribimos 3 -> FAILED
    out = service.inscribir("Safari", "14:00", 3, [p(), p("Ana"), p("Luis")], True)
    assert out["inscriptos"] == 3

def test_ingreso_datos_correctos_participante(service):
    # Ingresamos datos válidos para participante mockeados en la funcion p().
    # Si metemos algún dato inválido, falla
    out = service.inscribir("Safari", "16:00", 1, [p()], True)
    assert out["ok"] is True

def test_ingreso_datos_participante_nombre_caracteres_invalidos(service):
    with pytest.raises(ValidationError):
        # Nombre con caracteres inválidos
        service.inscribir("Safari", "16:00", 1, [p(nombre="@@@")], True)

def test_registrar_participante(service):
    # Registramos 1 participantes, pero indicamos cantidad 2 y registra el faltante
    with pytest.raises(ValidationError):
        service.inscribir("Safari", "14:00", 2, [p()], True)

def test_ingreso_datos_DNI_participante(service):
    # Fallamos con un DNI inválido (con letras, más de 10 digitos)
    with pytest.raises(ValidationError):
        service.inscribir("Safari", "14:00", 1, [p(dni="43883964")], True)

def test_ingresoTalleValida(service):
    out = service.inscribir("Safari", "14:00", 1, [p(talle="M")], True)
    assert out["ok"] is True

def test_ingresoTalleValidaParaActividadSolicitada(service):
    with pytest.raises(ValidationError):
        service.inscribir("Tirolesa", "10:00", 1, [p()], True)

def test_ingresoTalleValidaParaActividadNoIngresada(service):
    out = service.inscribir("Safari", "14:00", 1, [p()], True)
    assert out["ok"] is True

def test_inscripcionActividadSinDatos(service):
    with pytest.raises(ValidationError):
        service.inscribir(None, None, None, None, True)

def test_inscripcionActividadSinParticipante(service):
    with pytest.raises(ValidationError):
        service.inscribir("Safari", "14:00", 1, [], True)

def test_inscripcionSinAceptarTerminosLanzaError(service):
    # Asumimos que el mensaje de error contiene este texto
    mensaje_esperado = "Debe aceptar términos y condiciones"
    
    with pytest.raises(ValidationError, match=mensaje_esperado):
        service.inscribir("Safari", "14:00", 1, [p()], False)

def test_inscripcionActividadPersonasValidos(service):
    # Jardinería tiene 1 cupo -> 3 personas debe fallar
    """
        Verifica que al inscribir más personas que los cupos disponibles,
        se lance un ValidationError.
    """
    with pytest.raises(ValidationError):
        service.inscribir("Jardinería", "15:00", 10, [p(),p("Juan")], True)