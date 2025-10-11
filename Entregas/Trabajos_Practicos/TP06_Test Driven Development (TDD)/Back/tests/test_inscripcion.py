import pytest
from src.domain.services.inscripcion_service import InscripcionService
from src.domain.models import Actividad, Visitante, Horario, EstadoHorario

def build_test_data(db_session):
    """Crear datos de prueba en la base de datos"""
    # Crear estado horario
    estado_activo = EstadoHorario(nombre="activo", descripcion="Horario activo")
    db_session.add(estado_activo)

    # Crear actividades
    tirolesa = Actividad(nombre="Tirolesa", requiere_talle=True)
    safari = Actividad(nombre="Safari", requiere_talle=False)
    palestra = Actividad(nombre="Palestra", requiere_talle=True)
    jardineria = Actividad(nombre="Jardinería", requiere_talle=False)

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
        'luis': luis
    }

def test_inscripcion_exitosa_decrementa_cupo_y_devuelve_resultado(db_session):
    # Preparar datos de prueba
    data = build_test_data(db_session)

    # Crear servicio
    svc = InscripcionService(db_session)

    # Lista de visitantes
    visitantes = [data['ana'], data['luis']]

    # Realizar inscripción
    res = svc.enroll(
        id_horario=data['horario_tirolesa'].id,
        visitantes=visitantes,
        acepta_terminos=True
    )

    # Verificar resultado
    assert res.id_horario == data['horario_tirolesa'].id
    assert res.acepta_Terminos_Condiciones == True

    # Verificar que el cupo se decrementó
    horario_actualizado = db_session.query(Horario).filter(Horario.id == data['horario_tirolesa'].id).first()
    assert horario_actualizado.cupo_ocupado == 2  # 0 + 2
    assert horario_actualizado.cupo_total == 5  # Sin cambios

def test_inscripcion_falla_sin_cupo_suficiente(db_session):
    """Verificar que no se puede inscribir si no hay cupo suficiente"""
    data = build_test_data(db_session)

    # Crear horario con poco cupo
    horario_pequeno = Horario(
        id_actividad=data['tirolesa'].id,
        hora_inicio="11:00",
        hora_fin="12:00",
        cupo_total=1,  # Solo 1 cupo
        cupo_ocupado=0,
        estado="activo"
    )
    db_session.add(horario_pequeno)
    db_session.commit()

    svc = InscripcionService(db_session)
    visitantes = [data['ana'], data['luis']]  # 2 visitantes

    # Debería fallar por cupo insuficiente
    with pytest.raises(ValueError, match="Cupo insuficiente"):
        svc.enroll(
            id_horario=horario_pequeno.id,
            visitantes=visitantes,
            acepta_terminos=True
        )

def test_inscripcion_falla_sin_aceptar_terminos(db_session):
    """Verificar que no se puede inscribir sin aceptar términos"""
    data = build_test_data(db_session)

    svc = InscripcionService(db_session)
    visitantes = [data['ana']]

    # Debería fallar por no aceptar términos
    with pytest.raises(ValueError, match="Debe aceptar términos y condiciones"):
        svc.enroll(
            id_horario=data['horario_tirolesa'].id,
            visitantes=visitantes,
            acepta_terminos=False
        )

def test_inscripcion_falla_horario_inexistente(db_session):
    """Verificar que no se puede inscribir a horario inexistente"""
    data = build_test_data(db_session)

    svc = InscripcionService(db_session)
    visitantes = [data['ana']]

    # Debería fallar por horario inexistente
    with pytest.raises(ValueError, match="Horario no encontrado"):
        svc.enroll(
            id_horario=999,  # ID inexistente
            visitantes=visitantes,
            acepta_terminos=True
        )

def test_inscripcion_falla_visitante_inexistente(db_session):
    """Verificar que no se puede inscribir visitante inexistente"""
    data = build_test_data(db_session)

    svc = InscripcionService(db_session)

    # Crear visitante que no existe en BD
    visitante_falso = Visitante(nombre="Falso", dni=999, edad=20, talle=1)
    visitante_falso.id = 999  # ID que no existe en BD

    # Debería fallar por visitante inexistente
    with pytest.raises(ValueError, match="Visitante Falso no encontrado"):
        svc.enroll(
            id_horario=data['horario_tirolesa'].id,
            visitantes=[visitante_falso],
            acepta_terminos=True
        )
