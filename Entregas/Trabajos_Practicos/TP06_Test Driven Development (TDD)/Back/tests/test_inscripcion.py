import pytest
from src.domain.services.inscripcion_service import InscripcionService
from src.domain.models import Actividad, Visitante, Horario, EstadoHorario
from src.domain.exceptions import (
    CupoInsuficienteError,
    TerminosNoAceptadosError,
    HorarioNoEncontradoError,
    VisitanteNoEncontradoError,
    InscripcionDuplicadaError,
    TalleRequeridoError,
    EdadMinimaRequeridaError,
    DatosVisitantesInvalidosError,
    DnisDuplicadosEnListaError,
    ListaVisitantesVaciaError
)
from fastapi.testclient import TestClient
from src.application.main import app

def build_test_data(db_session):
    """Crear datos de prueba en la base de datos"""
    # Crear estados horario
    estado_activo = EstadoHorario(nombre="activo", descripcion="Horario activo")
    estado_inactivo = EstadoHorario(nombre="inactivo", descripcion="Horario inactivo")
    db_session.add_all([estado_activo, estado_inactivo])

    # Crear actividades
    tirolesa = Actividad(nombre="Tirolesa", requiere_talle=True, edad_minima=12, descripcion="Deslízate por las copas de los árboles en una experiencia emocionante de aventura extrema")
    safari = Actividad(nombre="Safari", requiere_talle=False, edad_minima=None, descripcion="Recorre el parque en vehículos especiales y observa la fauna local en su hábitat natural")
    palestra = Actividad(nombre="Palestra", requiere_talle=True, edad_minima=8, descripcion="Zona de juegos infantiles con estructuras")
    jardineria = Actividad(nombre="Jardineria", requiere_talle=False, edad_minima=None, descripcion="Aprende técnicas de cultivo sustentable y participa en el cuidado de nuestro vivero ecológico")

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

    horario_palestra = Horario(
        id_actividad=palestra.id,
        hora_inicio="13:00",
        hora_fin="14:00",
        cupo_total=8,
        cupo_ocupado=0,
        estado="inactivo"
    )

    horario_jardineria = Horario(
        id_actividad=jardineria.id,
        hora_inicio="14:00",
        hora_fin="15:00",
        cupo_total=10,
        cupo_ocupado=0,
        estado="activo"
    )

    horario_palestra_2 = Horario(
        id_actividad=palestra.id,
        hora_inicio="15:00",
        hora_fin="16:00",
        cupo_total=8,
        cupo_ocupado=0,
        estado="activo"
    )

    db_session.add_all([horario_tirolesa, horario_safari, horario_palestra, horario_jardineria, horario_palestra_2])
    db_session.commit()

    # Crear visitantes
    ana = Visitante(nombre="Ana", dni=12345678, edad=25, talle="M")
    luis = Visitante(nombre="Luis", dni=87654321, edad=30, talle="L")

    db_session.add_all([ana, luis])
    db_session.commit()

    return {
        'tirolesa': tirolesa,
        'safari': safari,
        'palestra': palestra,
        'jardineria': jardineria,
        'horario_tirolesa': horario_tirolesa,
        'horario_safari': horario_safari,
        'horario_palestra': horario_palestra,
        'horario_jardineria': horario_jardineria,
        'horario_palestra_2': horario_palestra_2,
        'ana': ana,
        'luis': luis,
        'estado_activo': estado_activo,
        'estado_inactivo': estado_inactivo
    }

def visitante_a_lista(db_session, id_visitante):
    """Convierte un id_visitante en lista de visitantes para la nueva API"""
    visitante = db_session.query(Visitante).filter(Visitante.id == id_visitante).first()
    if not visitante:
        raise VisitanteNoEncontradoError(f"Visitante ID {id_visitante}")
    
    return [{
        'nombre': visitante.nombre,
        'dni': visitante.dni,
        'edad': visitante.edad,
        'talle': visitante.talle
    }]

def test_inscripcion_exitosa_decrementa_cupo_y_devuelve_resultado(db_session):
    """Verificar que se puede inscribir un visitante individual correctamente"""
    data = build_test_data(db_session)
    visitantes = visitante_a_lista(db_session, data['ana'].id)

    # Crear servicio
    svc = InscripcionService(db_session)

    # Realizar inscripción individual
    res = svc.inscripcion_actividad(
        id_horario=data['horario_tirolesa'].id,
        visitantes=visitantes,
        acepta_terminos=True
    )[0]  # Acceder al primer elemento de la lista

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
    visitantes = visitante_a_lista(db_session, data['ana'].id)

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
            visitantes=visitantes,
            acepta_terminos=True
        )

    # Verificar detalles de la excepción
    assert exc_info.value.cupo_disponible == 0
    assert exc_info.value.cupo_solicitado == 1

def test_inscripcion_falla_sin_aceptar_terminos(db_session):
    """Verificar que no se puede inscribir sin aceptar términos"""
    data = build_test_data(db_session)
    visitantes = visitante_a_lista(db_session, data['ana'].id)

    svc = InscripcionService(db_session)

    # Debería fallar por no aceptar términos
    with pytest.raises(TerminosNoAceptadosError) as exc_info:
        svc.inscripcion_actividad(
            id_horario=data['horario_tirolesa'].id,
            visitantes=visitantes,
            acepta_terminos=False
        )
    assert "términos" in str(exc_info.value).lower()

def test_inscripcion_falla_horario_inexistente(db_session):
    """Verificar que no se puede inscribir a horario inexistente"""
    data = build_test_data(db_session)
    visitantes = visitante_a_lista(db_session, data['ana'].id)

    svc = InscripcionService(db_session)

    # Debería fallar por horario inexistente
    with pytest.raises(HorarioNoEncontradoError) as exc_info:
        svc.inscripcion_actividad(
            id_horario=999,  # ID inexistente
            visitantes=visitantes,
            acepta_terminos=True
        )

    # Verificar detalles de la excepción
    assert exc_info.value.id_horario == 999

def test_inscripcion_crea_visitante_automaticamente_cuando_no_existe(db_session):
    """Verificar que se crea automáticamente un visitante cuando no existe en la BD"""
    data = build_test_data(db_session)
    
    # Crear datos de visitante que no existe en la BD
    visitante_nuevo = {'nombre': 'Sofia Rodriguez', 'dni': 44444444, 'edad': 30, 'talle': 'M'}

    svc = InscripcionService(db_session)

    # Verificar que el visitante no existe antes
    visitante_antes = db_session.query(Visitante).filter(Visitante.dni == 44444444).first()
    assert visitante_antes is None

    # Realizar inscripción - debería crear el visitante automáticamente
    resultado = svc.inscripcion_actividad(
        id_horario=data['horario_tirolesa'].id,
        visitantes=[visitante_nuevo],
        acepta_terminos=True
    )

    # Verificar resultado
    assert isinstance(resultado, list)
    assert len(resultado) == 1
    assert resultado[0].id_horario == data['horario_tirolesa'].id
    assert resultado[0].acepta_Terminos_Condiciones == True
    assert resultado[0].nro_personas == 1

    # Verificar que el visitante fue creado
    visitante_creado = db_session.query(Visitante).filter(Visitante.dni == 44444444).first()
    assert visitante_creado is not None
    assert visitante_creado.nombre == 'Sofia Rodriguez'
    assert visitante_creado.edad == 30
    assert visitante_creado.talle == 'M'

    # Verificar que la inscripción apunta al visitante creado
    assert resultado[0].id_visitante == visitante_creado.id

def test_inscripcion_falla_ya_inscrito(db_session):
    """Verificar que no se puede inscribir a un horario al que ya estaba inscrito"""
    data = build_test_data(db_session)
    visitantes = visitante_a_lista(db_session, data['ana'].id)

    svc = InscripcionService(db_session)

    # Primera inscripción - debería funcionar
    svc.inscripcion_actividad(
        id_horario=data['horario_tirolesa'].id,
        visitantes=visitantes,
        acepta_terminos=True
    )

    # Segunda inscripción del mismo visitante al mismo horario - debería fallar
    with pytest.raises(InscripcionDuplicadaError) as exc_info:
        svc.inscripcion_actividad(
            id_horario=data['horario_tirolesa'].id,
            visitantes=visitantes,
            acepta_terminos=True
        )

    # Verificar detalles de la excepción
    assert exc_info.value.id_visitante == data['ana'].id
    assert exc_info.value.id_horario == data['horario_tirolesa'].id

# def test_get_all_inscripciones(db_session):
#     """Verificar que se pueden obtener todas las inscripciones con nombre de actividad"""
#     data = build_test_data(db_session)
#     visitantes_ana = visitante_a_lista(db_session, data['ana'].id)
#     visitantes_luis = visitante_a_lista(db_session, data['luis'].id)

#     svc = InscripcionService(db_session)

#     # Crear algunas inscripciones
#     svc.inscripcion_actividad(
#         id_horario=data['horario_tirolesa'].id,
#         visitantes=visitantes_ana,
#         acepta_terminos=True
#     )

#     svc.inscripcion_actividad(
#         id_horario=data['horario_safari'].id,
#         visitantes=visitantes_luis,
#         acepta_terminos=True
#     )

#     # Obtener todas las inscripciones
#     inscripciones = svc.get_all_inscripciones()

#     # Verificar resultado
#     assert len(inscripciones) == 2

#     # Verificar que contienen los datos correctos incluyendo nombre de actividad
#     nombres_actividades = [i.nombre_actividad for i in inscripciones]
#     assert "Tirolesa" in nombres_actividades
#     assert "Safari" in nombres_actividades

#     # Verificar que cada inscripción tiene todos los campos requeridos
#     for inscripcion in inscripciones:
#         assert hasattr(inscripcion, 'id')
#         assert hasattr(inscripcion, 'id_horario')
#         assert hasattr(inscripcion, 'id_visitante')
#         assert hasattr(inscripcion, 'nro_personas')
#         assert hasattr(inscripcion, 'acepta_Terminos_Condiciones')
#         assert hasattr(inscripcion, 'nombre_actividad')
#         assert isinstance(inscripcion.nombre_actividad, str)

def test_inscripcion_falla_requerimiento_talle_sin_talle(db_session):
    """
    Verifica que la inscripción falle si la actividad requiere talle y el visitante no tiene talle asignado.
    """
    # Preparar los datos de prueba
    data = build_test_data(db_session)

    visitante_sin_talle = Visitante(nombre="Carlos", dni=11223344, edad=28, talle=None)
    db_session.add(visitante_sin_talle)
    db_session.commit()

    visitantes = visitante_a_lista(db_session, visitante_sin_talle.id)

    svc = InscripcionService(db_session)

    # Verificar que se lanza la excepción al intentar inscribir sin talle
    with pytest.raises(TalleRequeridoError) as exc_info:
        svc.inscripcion_actividad(
            id_horario=data['horario_tirolesa'].id,  # Tirolesa requiere talle
            visitantes=visitantes,
            acepta_terminos=True
        )

    # Validar que el error menciona la actividad que requiere talle
    assert exc_info.value.nombre_actividad == "Tirolesa"

def test_inscripcion_falla_edad_minima_requerida(db_session):
    """
    Verifica que la inscripción falle si la actividad requiere una edad mínima y el visitante no la cumple.
    """
    # Preparar los datos de prueba
    data = build_test_data(db_session)

    # Crear un visitante menor de edad para la Tirolesa (requiere 12 años)
    visitante_menor = Visitante(nombre="Juanito", dni=55555555, edad=10, talle="M")
    db_session.add(visitante_menor)
    db_session.commit()

    visitantes = visitante_a_lista(db_session, visitante_menor.id)

    svc = InscripcionService(db_session)

    # Verificar que se lanza la excepción al intentar inscribir con edad insuficiente
    with pytest.raises(EdadMinimaRequeridaError) as exc_info:
        svc.inscripcion_actividad(
            id_horario=data['horario_tirolesa'].id,  # Tirolesa requiere edad mínima 12
            visitantes=visitantes,
            acepta_terminos=True
        )

    # Validar que el error menciona la actividad y las edades
    assert exc_info.value.nombre_actividad == "Tirolesa"
    assert exc_info.value.edad_visitante == 10
    assert exc_info.value.edad_minima == 12

def test_inscripcion_exitosa_edad_cumple_minima(db_session):
    """
    Verifica que la inscripción funciona cuando la edad del visitante cumple con la edad mínima requerida.
    """
    # Preparar los datos de prueba
    data = build_test_data(db_session)

    # Crear un visitante con edad suficiente para la Tirolesa (requiere 12 años)
    visitante_mayor = Visitante(nombre="Pedro", dni=66666666, edad=15, talle="L")
    db_session.add(visitante_mayor)
    db_session.commit()

    visitantes = visitante_a_lista(db_session, visitante_mayor.id)

    svc = InscripcionService(db_session)

    # La inscripción debería funcionar porque cumple con la edad mínima
    resultado = svc.inscripcion_actividad(
        id_horario=data['horario_tirolesa'].id,  # Tirolesa requiere edad mínima 12
        visitantes=visitantes,
        acepta_terminos=True
    )

    # Verificar que la inscripción se realizó correctamente
    assert len(resultado) == 1
    assert resultado[0].id_horario == data['horario_tirolesa'].id
    assert resultado[0].id_visitante == visitante_mayor.id

def test_inscripcion_exitosa_sin_edad_minima(db_session):
    """
    Verifica que la inscripción funciona cuando la actividad no tiene edad mínima requerida.
    """
    # Preparar los datos de prueba
    data = build_test_data(db_session)

    # Crear un visitante menor de edad para Safari (no requiere edad mínima)
    visitante_joven = Visitante(nombre="Carlitos", dni=77777777, edad=5, talle=None)
    db_session.add(visitante_joven)
    db_session.commit()

    visitantes = visitante_a_lista(db_session, visitante_joven.id)

    svc = InscripcionService(db_session)

    # La inscripción debería funcionar porque Safari no tiene edad mínima
    resultado = svc.inscripcion_actividad(
        id_horario=data['horario_safari'].id,  # Safari no requiere edad mínima
        visitantes=visitantes,
        acepta_terminos=True
    )

    # Verificar que la inscripción se realizó correctamente
    assert len(resultado) == 1
    assert resultado[0].id_horario == data['horario_safari'].id
    assert resultado[0].id_visitante == visitante_joven.id

def test_inscripcion_falla_horario_inactivo(db_session):
    """Verificar que no se puede inscribir con un talle inválido"""
    data = build_test_data(db_session)
    
    # Intentar inscribir con talle inválido
    visitante_invalido = {'nombre': 'Test User', 'dni': 99999999, 'edad': 25, 'talle': 'INVALID'}

    svc = InscripcionService(db_session)

    # Debería fallar por talle inválido
    with pytest.raises(ValueError) as exc_info:
        svc.inscripcion_actividad(
            id_horario=data['horario_tirolesa'].id,
            visitantes=[visitante_invalido],
            acepta_terminos=True
        )

    assert "talle" in str(exc_info.value).lower()

def test_inscripcion_exitosa_con_diferentes_talles_validos(db_session):
    """Verificar que se puede inscribir con diferentes talles válidos"""
    data = build_test_data(db_session)
    
    # Lista de talles válidos a probar
    talles_validos = ["XS", "S", "M", "L", "XL", "XXL"]
    
    svc = InscripcionService(db_session)
    
    for i, talle in enumerate(talles_validos):
        dni = 10000000 + i  # DNI único para cada test
        visitante = {'nombre': f'Test User {i}', 'dni': dni, 'edad': 25, 'talle': talle}
        
        # Realizar inscripción - debería funcionar
        resultado = svc.inscripcion_actividad(
            id_horario=data['horario_safari'].id,  # Safari no requiere talle específico
            visitantes=[visitante],
            acepta_terminos=True
        )
        
        assert len(resultado) == 1
        assert resultado[0].id_horario == data['horario_safari'].id
        
        # Verificar que el visitante fue creado con el talle correcto
        visitante_creado = db_session.query(Visitante).filter(Visitante.dni == dni).first()
        assert visitante_creado is not None
        assert visitante_creado.talle == talle

def test_inscripcion_falla_horario_inactivo(db_session):
    """Verificar que un visitante puede inscribirse en múltiples horarios diferentes"""
    data = build_test_data(db_session)
    visitantes = visitante_a_lista(db_session, data['ana'].id)

    svc = InscripcionService(db_session)

    # Primera inscripción - debería funcionar
    res1 = svc.inscripcion_actividad(
        id_horario=data['horario_tirolesa'].id,
        visitantes=visitantes,
        acepta_terminos=True
    )[0]

    # Segunda inscripción en horario diferente - debería funcionar también
    res2 = svc.inscripcion_actividad(
        id_horario=data['horario_safari'].id,
        visitantes=visitantes,
        acepta_terminos=True
    )[0]

    # Verificar ambas inscripciones
    assert res1.id_visitante == data['ana'].id
    assert res2.id_visitante == data['ana'].id
    assert res1.id_horario != res2.id_horario

def test_inscripcion_exitosa_tres_visitantes(db_session):
    """Verificar que se pueden realizar inscripciones grupales correctamente"""
    data = build_test_data(db_session)
    
    # Crear lista de 3 visitantes
    visitantes = [
        visitante_a_lista(db_session, data['ana'].id)[0],  # Ana existente
        visitante_a_lista(db_session, data['luis'].id)[0], # Luis existente
        {'nombre': 'Pedro Martínez', 'dni': 33333333, 'edad': 22, 'talle': 'S'}  # Nuevo visitante
    ]

    svc = InscripcionService(db_session)

    # Realizar inscripción grupal
    resultado = svc.inscripcion_actividad(
        id_horario=data['horario_safari'].id,  # Safari no requiere talle
        visitantes=visitantes,
        acepta_terminos=True
    )

    # Verificar resultado - devuelve lista de objetos Inscripcion
    assert isinstance(resultado, list)
    assert len(resultado) == 3

    # Verificar que todas las inscripciones tienen los mismos datos básicos
    for inscripcion in resultado:
        assert inscripcion.id_horario == data['horario_safari'].id
        assert inscripcion.acepta_Terminos_Condiciones == True
        assert inscripcion.nro_personas == 1

    # Verificar que el nuevo visitante fue creado
    pedro = db_session.query(Visitante).filter(Visitante.dni == 33333333).first()
    assert pedro is not None
    assert pedro.nombre == 'Pedro Martínez'
    assert pedro.edad == 22
    assert pedro.talle == 'S'

    # Verificar que el cupo se decrementó correctamente (3 personas)
    horario_actualizado = db_session.query(Horario).filter(Horario.id == data['horario_safari'].id).first()
    assert horario_actualizado.cupo_ocupado == 3

# Tests de integración para verificar códigos de error HTTP
def test_post_inscripcion_endpoint_retorna_400_sin_cupo(client, db_session):
    """Verificar que el endpoint POST retorna 400 cuando no hay cupo"""
    data = build_test_data(db_session)
    
    # Crear horario sin cupo
    horario_sin_cupo = Horario(
        id_actividad=data['tirolesa'].id,
        hora_inicio="15:00",
        hora_fin="16:00",
        cupo_total=0,
        cupo_ocupado=0,
        estado="activo"
    )
    db_session.add(horario_sin_cupo)
    db_session.commit()

    payload = {
        "id_horario": horario_sin_cupo.id,
        "visitantes": [{
            "nombre": "Test User",
            "dni": 99999999,
            "edad": 25,
            "talle": "M"
        }],
        "acepta_terminos": True
    }

    response = client.post("/inscripciones/", json=payload)
    assert response.status_code == 400
    assert "No hay cupo disponible" in response.json()["detail"]

def test_post_inscripcion_endpoint_retorna_400_sin_aceptar_terminos(client, db_session):
    """Verificar que el endpoint POST retorna 400 cuando no se aceptan términos"""
    data = build_test_data(db_session)

    payload = {
        "id_horario": data['horario_tirolesa'].id,
        "visitantes": [{
            "nombre": "Test User",
            "dni": 99999999,
            "edad": 25,
            "talle": "M"
        }],
        "acepta_terminos": False
    }

    response = client.post("/inscripciones/", json=payload)
    assert response.status_code == 400
    assert "Debe aceptar los términos y condiciones" in response.json()["detail"]

def test_post_inscripcion_endpoint_retorna_404_horario_inexistente(client):
    """Verificar que el endpoint POST retorna 404 para horario inexistente"""
    payload = {
        "id_horario": 99999,
        "visitantes": [{
            "nombre": "Test User",
            "dni": 99999999,
            "edad": 25,
            "talle": "M"
        }],
        "acepta_terminos": True
    }

    response = client.post("/inscripciones/", json=payload)
    assert response.status_code == 404
    assert "Horario no encontrado" in response.json()["detail"]

def test_post_inscripcion_endpoint_retorna_409_inscripcion_duplicada(client, db_session):
    """Verificar que el endpoint POST retorna 409 para inscripción duplicada"""
    data = build_test_data(db_session)

    payload = {
        "id_horario": data['horario_tirolesa'].id,
        "visitantes": [{
            "nombre": data['ana'].nombre,
            "dni": data['ana'].dni,
            "edad": data['ana'].edad,
            "talle": data['ana'].talle
        }],
        "acepta_terminos": True
    }

    # Primera inscripción - debería funcionar
    response1 = client.post("/inscripciones/", json=payload)
    assert response1.status_code == 200

    # Segunda inscripción del mismo visitante - debería fallar
    response2 = client.post("/inscripciones/", json=payload)
    assert response2.status_code == 409

def test_post_inscripcion_endpoint_retorna_400_talle_requerido(client, db_session):
    """Verificar que el endpoint POST retorna 400 cuando se requiere talle"""
    data = build_test_data(db_session)

    payload = {
        "id_horario": data['horario_tirolesa'].id,  # Tirolesa requiere talle
        "visitantes": [{
            "nombre": "Test User",
            "dni": 99999999,
            "edad": 25,
            "talle": None  # Sin talle
        }],
        "acepta_terminos": True
    }

    response = client.post("/inscripciones/", json=payload)
    assert response.status_code == 400
    assert "requiere talle" in response.json()["detail"]

def test_get_inscripciones_con_visitantes_endpoint(client, db_session):
    """Verificar que el endpoint GET /con-visitantes funciona correctamente"""
    data = build_test_data(db_session)

    # Crear una inscripción primero
    payload = {
        "id_horario": data['horario_tirolesa'].id,
        "visitantes": [{
            "nombre": data['ana'].nombre,
            "dni": data['ana'].dni,
            "edad": data['ana'].edad,
            "talle": data['ana'].talle
        }],
        "acepta_terminos": True
    }
    
    client.post("/inscripciones/", json=payload)

    # Obtener inscripciones con visitantes
    response = client.get("/inscripciones/con-visitantes")
    assert response.status_code == 200
    
    data_response = response.json()
    assert isinstance(data_response, list)
    assert len(data_response) == 1
    
    inscripcion = data_response[0]
    assert "visitante" in inscripcion
    assert "nombre_actividad" in inscripcion
    assert inscripcion["visitante"]["nombre"] == data['ana'].nombre
    assert inscripcion["visitante"]["dni"] == data['ana'].dni

def test_inscripcion_falla_si_nombre_visitante_vacio(db_session):
    """Verificar que la inscripción falle si el visitante tiene un nombre vacío"""
    data = build_test_data(db_session)
    
    visitante_nombre_vacio = {'nombre': '', 'dni': 12345679, 'edad': 25, 'talle': 'M'}

    svc = InscripcionService(db_session)

    # Verificar que se lanza la excepción al intentar inscribir con nombre vacío
    with pytest.raises(ValueError) as exc_info:
        svc.inscripcion_actividad(
            id_horario=data['horario_tirolesa'].id,
            visitantes=[visitante_nombre_vacio],
            acepta_terminos=True
        )

    assert f"datos inválidos para : nombre" in str(exc_info.value).lower()

def test_inscripcion_falla_si_edad_no_es_numero(db_session):
    """Verificar que la inscripción falle si la edad del visitante no es un número entre razonable"""
    data = build_test_data(db_session)

    visitante_edad_no_numero = {'nombre': 'Test User', 'dni': 12345680, 'edad': 121321312, 'talle': 'M'}

    svc = InscripcionService(db_session)

    # Verificar que se lanza la excepción al intentar inscribir con edad no numérica
    with pytest.raises(ValueError) as exc_info:
        svc.inscripcion_actividad(
            id_horario=data['horario_tirolesa'].id,
            visitantes=[visitante_edad_no_numero],
            acepta_terminos=True
        )

    assert "datos inválidos" in str(exc_info.value).lower() and "edad" in str(exc_info.value).lower()

def test_inscripcion_falla_si_datos_visitante_nuevo_incompletos(db_session):
    """Verificar que la inscripción falle si los datos de un visitante nuevo están incompletos"""
    data = build_test_data(db_session)
    
    visitante_incompleto = {'nombre': 'Incomplete User', 'dni': None, 'edad': 25, 'talle': 'M'}

    svc = InscripcionService(db_session)

    # Verificar que se lanza la excepción al intentar inscribir con datos incompletos
    with pytest.raises(ValueError) as exc_info:
        svc.inscripcion_actividad(
            id_horario=data['horario_tirolesa'].id,
            visitantes=[visitante_incompleto],
            acepta_terminos=True
        )

    assert "datos inválidos para incomplete user: dni" in str(exc_info.value).lower()

def test_inscripcion_exitosa_con_cupo_exacto_restante(db_session):
    """Verificar que se puede inscribir cuando el cupo restante es exacto al número de visitantes"""
    data = build_test_data(db_session)
    
    # Ajustar el cupo del horario para que quede 3 disponibles
    horario = db_session.query(Horario).filter(Horario.id == data['horario_safari'].id).first()
    horario.cupo_total = 5
    horario.cupo_ocupado = 2  # Quedan 3 disponibles
    db_session.commit()

    visitantes = [
        {'nombre': 'Visitante 1', 'dni': 55555555, 'edad': 30, 'talle': 'M'},
        {'nombre': 'Visitante 2', 'dni': 66666666, 'edad': 28, 'talle': 'L'},
        {'nombre': 'Visitante 3', 'dni': 77777777, 'edad': 35, 'talle': 'XL'}
    ]

    svc = InscripcionService(db_session)

    # Realizar inscripción grupal
    resultado = svc.inscripcion_actividad(
        id_horario=data['horario_safari'].id,
        visitantes=visitantes,
        acepta_terminos=True
    )

    # Verificar resultado - devuelve lista de objetos Inscripcion
    assert isinstance(resultado, list)
    assert len(resultado) == 3

    # Verificar que el cupo se ha llenado completamente
    horario_actualizado = db_session.query(Horario).filter(Horario.id == data['horario_safari'].id).first()
    assert horario_actualizado.cupo_ocupado == 5  # Ahora está lleno


def test_inscripcion_falla_si_visitante_tiene_dni_duplicado_en_lista(db_session):
    """Verificar que la inscripción falle si hay DNIs duplicados en la lista de visitantes a crear"""
    data = build_test_data(db_session)
    
    visitante_duplicado = {'nombre': 'Duplicated User', 'dni': 12345678, 'edad': 25, 'talle': 'M'}  # DNI de Ana

    svc = InscripcionService(db_session)

    # Verificar que se lanza la excepción al intentar inscribir con DNI duplicado
    with pytest.raises(DnisDuplicadosEnListaError) as exc_info:
        svc.inscripcion_actividad(
            id_horario=data['horario_tirolesa'].id,
            visitantes=[visitante_duplicado, visitante_duplicado],  # Mismo visitante dos veces
            acepta_terminos=True
        )

    assert exc_info.value.dni_duplicado == 12345678

def test_inscripcion_exitosa_con_edad_minima_exacta(db_session):
    """
    Verifica que la inscripción funciona cuando la edad del visitante es exactamente la mínima requerida.
    """
    # Preparar los datos de prueba
    data = build_test_data(db_session)

    # Crear un visitante con edad exactamente igual a la mínima para la Tirolesa (requiere 12 años)
    visitante_exacto = Visitante(nombre="Exacto", dni=88888888, edad=12, talle="M")
    db_session.add(visitante_exacto)
    db_session.commit()

    visitantes = visitante_a_lista(db_session, visitante_exacto.id)

    svc = InscripcionService(db_session)

    # La inscripción debería funcionar porque cumple con la edad mínima exacta
    resultado = svc.inscripcion_actividad(
        id_horario=data['horario_tirolesa'].id,  # Tirolesa requiere edad mínima 12
        visitantes=visitantes,
        acepta_terminos=True
    )

    # Verificar que la inscripción se realizó correctamente
    assert len(resultado) == 1
    assert resultado[0].id_horario == data['horario_tirolesa'].id
    assert resultado[0].id_visitante == visitante_exacto.id

def test_inscripcion_falla_si_lista_visitantes_vacia(db_session):
    """Verificar que la inscripción falle si la lista de visitantes está vacía"""
    data = build_test_data(db_session)

    svc = InscripcionService(db_session)

    # Verificar que se lanza la excepción al intentar inscribir con lista vacía
    with pytest.raises(ListaVisitantesVaciaError) as exc_info:
        svc.inscripcion_actividad(
            id_horario=data['horario_tirolesa'].id,
            visitantes=[],  # Lista vacía
            acepta_terminos=True
        )

    assert "la lista de visitantes no puede estar vacía" in str(exc_info.value).lower()

def test_inscripcion_falla_si_edad_menor_y_requiere_edad_minima_tirolesa(db_session):
    """
    Verifica que la inscripción falle si la actividad requiere una edad mínima y el visitante es menor para una actividad que requiera edad minima.
    """
    # Preparar los datos de prueba
    data = build_test_data(db_session)

    # Crear un visitante menor de edad para la Tirolesa (requiere 12 años)
    visitante_menor = Visitante(nombre="Pequeño", dni=99999999, edad=8, talle="S")
    db_session.add(visitante_menor)
    db_session.commit()

    visitantes = visitante_a_lista(db_session, visitante_menor.id)

    svc = InscripcionService(db_session)

    # Verificar que se lanza la excepción al intentar inscribir con edad insuficiente
    with pytest.raises(EdadMinimaRequeridaError) as exc_info:
        svc.inscripcion_actividad(
            id_horario=data['horario_tirolesa'].id,  # Tirolesa requiere edad mínima 12
            visitantes=visitantes,
            acepta_terminos=True
        )

    # Validar que el error menciona la actividad y las edades
    assert exc_info.value.nombre_actividad == "Tirolesa"
    assert exc_info.value.edad_visitante == 8
    assert exc_info.value.edad_minima == 12

def test_inscripcion_falla_si_edad_menor_y_requiere_edad_minima_palestra(db_session):
    """
    Verifica que la inscripción falle si la actividad requiere una edad mínima y el visitante es menor.
    """
    # Preparar los datos de prueba
    data = build_test_data(db_session)

    # Crear un visitante menor de edad para el Palestra (requiere 8 años)
    visitante_menor = Visitante(nombre="Chiquito", dni=10101010, edad=3, talle="XS")
    db_session.add(visitante_menor)
    db_session.commit()

    visitantes = visitante_a_lista(db_session, visitante_menor.id)

    svc = InscripcionService(db_session)

    # Verificar que se lanza la excepción al intentar inscribir con edad insuficiente
    with pytest.raises(EdadMinimaRequeridaError) as exc_info:
        svc.inscripcion_actividad(
            id_horario=data['horario_palestra_2'].id,  # Palestra requiere edad mínima 8
            visitantes=visitantes,
            acepta_terminos=True
        )

    # Validar que el error menciona la actividad y las edades
    assert exc_info.value.nombre_actividad == "Palestra"
    assert exc_info.value.edad_visitante == 3
    assert exc_info.value.edad_minima == 8

def test_inscripcion_falla_si_edad_cumple_pero_no_hay_talle_palestra(db_session):
    """
    Verifica que la inscripción falle si la actividad requiere talle y el visitante no tiene talle asignado.
    """
    # Preparar los datos de prueba
    data = build_test_data(db_session)

    visitante_sin_talle = Visitante(nombre="SinTalle", dni=12121212, edad=10, talle=None)
    db_session.add(visitante_sin_talle)
    db_session.commit()

    visitantes = visitante_a_lista(db_session, visitante_sin_talle.id)

    svc = InscripcionService(db_session)

    # Verificar que se lanza la excepción al intentar inscribir sin talle
    with pytest.raises(TalleRequeridoError) as exc_info:
        svc.inscripcion_actividad(
            id_horario=data['horario_palestra_2'].id,  # Palestra requiere talle
            visitantes=visitantes,
            acepta_terminos=True
        )

    # Validar que el error menciona la actividad que requiere talle
    assert exc_info.value.nombre_actividad == "Palestra"