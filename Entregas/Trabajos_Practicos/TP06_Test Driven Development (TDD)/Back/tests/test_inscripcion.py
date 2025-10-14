import pytest
from src.domain.services.inscripcion_service import InscripcionService
from src.domain.models import Actividad, Visitante, Horario, EstadoHorario
from src.domain.exceptions import (
    CupoInsuficienteError,
    TerminosNoAceptadosError,
    HorarioNoEncontradoError,
    VisitanteNoEncontradoError,
    InscripcionDuplicadaError,
    TalleRequeridoError
)

def build_test_data(db_session):
    """Crear datos de prueba en la base de datos"""
    # Crear estados horario
    estado_activo = EstadoHorario(nombre="activo", descripcion="Horario activo")
    estado_inactivo = EstadoHorario(nombre="inactivo", descripcion="Horario inactivo")
    db_session.add_all([estado_activo, estado_inactivo])

    # Crear actividades
    tirolesa = Actividad(nombre="Tirolesa", requiere_talle=True)
    safari = Actividad(nombre="Safari", requiere_talle=False)
    palestra = Actividad(nombre="Palestra", requiere_talle=True)
    jardineria = Actividad(nombre="Jardineria", requiere_talle=False)

    db_session.add_all([tirolesa, safari, palestra, jardineria])
    db_session.commit()

    # Crear horarios
    horario_tirolesa = Horario(
        id_actividad=tirolesa.id,
        hora_inicio="10:00",
        hora_fin="11:00",
        cupo_total=5,
        cupo_ocupado=0,
        estado="activo"
    )

    horario_safari = Horario(
        id_actividad=safari.id,
        hora_inicio="10:00",
        hora_fin="12:00",
        cupo_total=10,
        cupo_ocupado=0,
        estado="activo"
    )

    db_session.add_all([horario_tirolesa, horario_safari])
    db_session.commit()

    # Crear visitantes
    ana = Visitante(nombre="Ana", dni=12345678, edad=25, talle=2)  # M
    luis = Visitante(nombre="Luis", dni=87654321, edad=30, talle=3)  # L

    db_session.add_all([ana, luis])
    db_session.commit()

    return {
        'tirolesa': tirolesa,
        'safari': safari,
        'horario_tirolesa': horario_tirolesa,
        'horario_safari': horario_safari,
        'ana': ana,
        'luis': luis,
        'estado_activo': estado_activo,
        'estado_inactivo': estado_inactivo
    }

def test_inscripcion_exitosa_decrementa_cupo_y_devuelve_resultado(db_session):
    """Verificar que se puede inscribir un visitante individual correctamente"""
    data = build_test_data(db_session)

    # Crear servicio
    svc = InscripcionService(db_session)

    # Realizar inscripción individual
    res = svc.inscripcion_actividad(
        id_horario=data['horario_tirolesa'].id,
        id_visitante=data['ana'].id,
        acepta_terminos=True
    )

    # Verificar resultado
    assert res.id_horario == data['horario_tirolesa'].id
    assert res.id_visitante == data['ana'].id
    assert res.acepta_Terminos_Condiciones == True
    assert res.nro_personas == 1

    # Verificar que el cupo se decrementó
    horario_actualizado = db_session.query(Horario).filter(Horario.id == data['horario_tirolesa'].id).first()
    assert horario_actualizado.cupo_ocupado == 1  # 0 + 1
    assert horario_actualizado.cupo_total == 5  # Sin cambios

def test_inscripcion_falla_sin_cupo_suficiente(db_session):
    """Verificar que no se puede inscribir si no hay cupo suficiente"""
    data = build_test_data(db_session)

    # Crear horario con poco cupo
    horario_pequeno = Horario(
        id_actividad=data['tirolesa'].id,
        hora_inicio="11:00",
        hora_fin="12:00",
        cupo_total=0,  # Sin cupo disponible
        cupo_ocupado=0,
        estado="activo"
    )
    db_session.add(horario_pequeno)
    db_session.commit()

    svc = InscripcionService(db_session)

    # Debería fallar por cupo insuficiente
    with pytest.raises(CupoInsuficienteError) as exc_info:
        svc.inscripcion_actividad(
            id_horario=horario_pequeno.id,
            id_visitante=data['ana'].id,
            acepta_terminos=True
        )

    # Verificar detalles de la excepción
    assert exc_info.value.cupo_disponible == 0
    assert exc_info.value.cupo_solicitado == 1

def test_inscripcion_falla_sin_aceptar_terminos(db_session):
    """Verificar que no se puede inscribir sin aceptar términos"""
    data = build_test_data(db_session)

    svc = InscripcionService(db_session)

    # Debería fallar por no aceptar términos
    with pytest.raises(TerminosNoAceptadosError):
        svc.inscripcion_actividad(
            id_horario=data['horario_tirolesa'].id,
            id_visitante=data['ana'].id,
            acepta_terminos=False
        )

def test_inscripcion_falla_horario_inexistente(db_session):
    """Verificar que no se puede inscribir a horario inexistente"""
    data = build_test_data(db_session)

    svc = InscripcionService(db_session)

    # Debería fallar por horario inexistente
    with pytest.raises(HorarioNoEncontradoError) as exc_info:
        svc.inscripcion_actividad(
            id_horario=999,  # ID inexistente
            id_visitante=data['ana'].id,
            acepta_terminos=True
        )

    # Verificar detalles de la excepción
    assert exc_info.value.id_horario == 999

def test_inscripcion_falla_visitante_inexistente(db_session):
    """Verificar que no se puede inscribir visitante inexistente"""
    data = build_test_data(db_session)

    svc = InscripcionService(db_session)

    # Debería fallar por visitante inexistente
    with pytest.raises(VisitanteNoEncontradoError) as exc_info:
        svc.inscripcion_actividad(
            id_horario=data['horario_tirolesa'].id,
            id_visitante=999,  # ID inexistente
            acepta_terminos=True
        )

    # Verificar detalles de la excepción
    assert "Visitante ID 999" in str(exc_info.value)

def test_inscripcion_falla_ya_inscrito(db_session):
    """Verificar que no se puede inscribir a un horario al que ya estaba inscrito"""
    data = build_test_data(db_session)

    svc = InscripcionService(db_session)

    # Primera inscripción - debería funcionar
    svc.inscripcion_actividad(
        id_horario=data['horario_tirolesa'].id,
        id_visitante=data['ana'].id,
        acepta_terminos=True
    )

    # Segunda inscripción del mismo visitante al mismo horario - debería fallar
    with pytest.raises(InscripcionDuplicadaError) as exc_info:
        svc.inscripcion_actividad(
            id_horario=data['horario_tirolesa'].id,
            id_visitante=data['ana'].id,
            acepta_terminos=True
        )

    # Verificar detalles de la excepción
    assert exc_info.value.id_visitante == data['ana'].id
    assert exc_info.value.id_horario == data['horario_tirolesa'].id

def test_get_all_inscripciones(db_session):
    """Verificar que se pueden obtener todas las inscripciones con nombre de actividad"""
    data = build_test_data(db_session)

    svc = InscripcionService(db_session)

    # Crear algunas inscripciones
    svc.inscripcion_actividad(
        id_horario=data['horario_tirolesa'].id,
        id_visitante=data['ana'].id,
        acepta_terminos=True
    )

    svc.inscripcion_actividad(
        id_horario=data['horario_safari'].id,
        id_visitante=data['luis'].id,
        acepta_terminos=True
    )

    # Obtener todas las inscripciones
    inscripciones = svc.get_all_inscripciones()

    # Verificar resultado
    assert len(inscripciones) == 2

    # Verificar que contienen los datos correctos incluyendo nombre de actividad
    nombres_actividades = [i.nombre_actividad for i in inscripciones]
    assert "Tirolesa" in nombres_actividades
    assert "Safari" in nombres_actividades

    # Verificar que cada inscripción tiene todos los campos requeridos
    for inscripcion in inscripciones:
        assert hasattr(inscripcion, 'id')
        assert hasattr(inscripcion, 'id_horario')
        assert hasattr(inscripcion, 'id_visitante')
        assert hasattr(inscripcion, 'nro_personas')
        assert hasattr(inscripcion, 'acepta_Terminos_Condiciones')
        assert hasattr(inscripcion, 'nombre_actividad')
        assert isinstance(inscripcion.nombre_actividad, str)

def test_inscripcion_falla_requerimiento_talle_sin_talle(db_session):
    """
    Verifica que la inscripción falle si la actividad requiere talle y el visitante no tiene talle asignado.
    """
    # Preparar los datos de prueba
    data = build_test_data(db_session)

    visitante_sin_talle = Visitante(nombre="Carlos", dni=11223344, edad=28, talle=None)
    db_session.add(visitante_sin_talle)
    db_session.commit()

    svc = InscripcionService(db_session)

    # Verificar que se lanza la excepción al intentar inscribir sin talle
    with pytest.raises(TalleRequeridoError) as exc_info:
        svc.inscripcion_actividad(
            id_horario=data['horario_tirolesa'].id,  # Tirolesa requiere talle
            id_visitante=visitante_sin_talle.id,
            acepta_terminos=True
        )

    # Validar que el error menciona la actividad que requiere talle
    assert exc_info.value.nombre_actividad == "Tirolesa"

def test_inscripcion_falla_horario_inactivo(db_session):
    """Verificar que no se puede inscribir en un horario inactivo"""
    data = build_test_data(db_session)

    # Crear horario inactivo usando una actividad existente
    horario_inactivo = Horario(
        id_actividad=data['tirolesa'].id,  # Usar actividad existente
        hora_inicio="14:00",
        hora_fin="15:00",
        cupo_total=5,
        cupo_ocupado=0,
        estado="inactivo"  # Horario no disponible
    )
    db_session.add(horario_inactivo)
    db_session.commit()

    svc = InscripcionService(db_session)

    # Debería fallar por horario inactivo
    with pytest.raises(ValueError) as exc_info:
        svc.inscripcion_actividad(
            id_horario=horario_inactivo.id,
            id_visitante=data['ana'].id,
            acepta_terminos=True
        )

    assert "horario inactivo" in str(exc_info.value).lower()

def test_inscripcion_exitosa_multiples_horarios_mismo_visitante(db_session):
    """Verificar que un visitante puede inscribirse en múltiples horarios diferentes"""
    data = build_test_data(db_session)

    svc = InscripcionService(db_session)

    # Primera inscripción - debería funcionar
    res1 = svc.inscripcion_actividad(
        id_horario=data['horario_tirolesa'].id,
        id_visitante=data['ana'].id,
        acepta_terminos=True
    )

    # Segunda inscripción en horario diferente - debería funcionar también
    res2 = svc.inscripcion_actividad(
        id_horario=data['horario_safari'].id,
        id_visitante=data['ana'].id,
        acepta_terminos=True
    )

    # Verificar ambas inscripciones
    assert res1.id_visitante == data['ana'].id
    assert res2.id_visitante == data['ana'].id
    assert res1.id_horario != res2.id_horario