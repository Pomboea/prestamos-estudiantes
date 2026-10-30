"""Pruebas de la API principal: JWT, permisos, CRUD, borrado lógico, auditoría y flujo completo."""
import time
from datetime import date, timedelta

from tests.conftest import token

TABLAS = ["rol", "modulo", "moduloxrol", "facultad", "programa_academico", "usuario", "categoria_objeto",
          "condicion_objeto", "objeto", "imagen_objeto", "estado_solicitud", "solicitud_prestamo",
          "prestamo", "devolucion", "calificacion", "notificacion", "sancion"]


# ---------- Estructura de la BD ----------
def test_minimo_12_tablas(sql):
    filas = sql("SELECT count(*) n FROM information_schema.tables WHERE table_schema='public' AND table_type='BASE TABLE'")
    assert filas[0]["n"] >= 12


def test_todas_las_tablas_cumplen_requisitos(sql):
    for t in TABLAS:
        cols = {r["column_name"]: r for r in sql(
            "SELECT column_name, data_type, column_default FROM information_schema.columns WHERE table_name=:t", t=t)}
        assert cols["estado"]["data_type"] == "boolean" and "true" in cols["estado"]["column_default"], t
        assert "creado" in cols and "actualizado" in cols, t
        tipos = {r["constraint_type"] for r in sql(
            "SELECT constraint_type FROM information_schema.table_constraints WHERE table_name=:t", t=t)}
        assert {"PRIMARY KEY", "UNIQUE"} <= tipos, t
        assert sql("SELECT 1 FROM information_schema.triggers WHERE event_object_table=:t", t=t), t


# ---------- Autenticación ----------
def test_registro_y_login_json(cliente):
    r = cliente.post("/api/auth/registro", json={"nombres": "Laura", "apellidos": "Ruiz", "correo": "laura@uni.edu.co",
                                             "codigo_estudiantil": "2021999", "contrasena": "Clave123*", "id_programa": 1})
    assert r.status_code == 201, r.text
    assert "contrasena_hash" not in r.json() and r.json()["estado"] is True
    r = cliente.post("/api/auth/login-json", json={"correo": "laura@uni.edu.co", "contrasena": "Clave123*"})
    assert r.status_code == 200 and r.json()["rol"] == "estudiante"


def test_registro_duplicado_409(cliente):
    r = cliente.post("/api/auth/registro", json={"nombres": "Ana", "apellidos": "Xu", "correo": "ana@uni.edu.co",
                                             "codigo_estudiantil": "XYZ1", "contrasena": "Clave123*"})
    assert r.status_code == 409


def test_login_incorrecto_401(cliente):
    assert cliente.post("/api/auth/login", data={"username": "ana@uni.edu.co", "password": "mala"}).status_code == 401


def test_sin_token_401(cliente):
    assert cliente.get("/api/objetos").status_code == 401
    assert cliente.get("/api/roles", headers={"Authorization": "Bearer token.falso.x"}).status_code == 401


def test_rol_sin_permiso_403(cliente, ana):
    assert cliente.get("/api/roles", headers=ana).status_code == 403
    assert cliente.post("/api/categorias", json={"nombre": "Prohibida"}, headers=ana).status_code == 403


def test_yo(cliente, ana):
    assert cliente.get("/api/auth/yo", headers=ana).json()["correo"] == "ana@uni.edu.co"


# ---------- CRUD + borrado lógico + auditoría ----------
def test_crud_borrado_logico_y_auditoria(cliente, admin, sql):
    r = cliente.post("/api/categorias", json={"nombre": "Tablets", "descripcion": "Tabletas"}, headers=admin)
    assert r.status_code == 201
    cat = r.json(); idc = cat["id_categoria"]
    assert cat["estado"] is True and cat["creado"] and cat["actualizado"]
    time.sleep(1.1)
    r = cliente.put(f"/api/categorias/{idc}", json={"descripcion": "Tabletas y iPads"}, headers=admin)
    act = r.json()
    assert act["creado"] == cat["creado"]            # creado no cambia
    assert act["actualizado"] > cat["actualizado"]   # actualizado se renueva (trigger)
    r = cliente.delete(f"/api/categorias/{idc}", headers=admin)
    assert r.status_code == 200 and r.json()["estado"] is False
    ids = [c["id_categoria"] for c in cliente.get("/api/categorias", headers=admin).json()]
    assert idc not in ids                             # oculto en el listado
    fila = sql("SELECT estado FROM categoria_objeto WHERE id_categoria=:i", i=idc)
    assert fila and fila[0]["estado"] is False        # el registro sigue físicamente
    todos = cliente.get("/api/categorias?incluir_inactivos=true", headers=admin).json()
    assert idc in [c["id_categoria"] for c in todos]
    r = cliente.put(f"/api/categorias/{idc}", json={"estado": True}, headers=admin)  # reactivar
    assert r.json()["estado"] is True


def test_creado_no_modificable_por_sql(sql):
    from app.db.session import motor
    from sqlalchemy import text
    with motor.begin() as c:
        antes = c.execute(text("SELECT creado FROM rol WHERE id_rol=1")).scalar()
        c.execute(text("UPDATE rol SET creado='2000-01-01', descripcion='x' WHERE id_rol=1"))
        despues = c.execute(text("SELECT creado FROM rol WHERE id_rol=1")).scalar()
    assert antes == despues


def test_crud_todas_las_tablas_listan(cliente, admin):
    for ruta in ["/roles", "/modulos", "/moduloxrol", "/usuarios", "/facultades", "/programas", "/categorias",
                 "/condiciones", "/objetos", "/imagenes", "/estados-solicitud", "/solicitudes", "/prestamos",
                 "/devoluciones", "/calificaciones", "/notificaciones", "/sanciones"]:
        r = cliente.get("/api" + ruta + "/", headers=admin)
        assert r.status_code == 200, ruta


def test_404(cliente, admin):
    assert cliente.get("/api/objetos/99999", headers=admin).status_code == 404


def test_estudiante_no_edita_objeto_ajeno(cliente, carlos):
    # objeto 1 pertenece a Ana
    assert cliente.put("/api/objetos/1", json={"nombre": "Hackeado"}, headers=carlos).status_code == 403
    assert cliente.delete("/api/objetos/1", headers=carlos).status_code == 403


def test_usuario_crud_admin_hashea(cliente, admin):
    r = cliente.post("/api/usuarios", json={"nombres": "Pedro", "apellidos": "Díaz", "correo": "pedro@uni.edu.co",
                                        "codigo_estudiantil": "2021555", "contrasena": "Pedro123*", "id_rol": 2}, headers=admin)
    assert r.status_code == 201
    token(cliente, "pedro@uni.edu.co", "Pedro123*")


# ---------- Flujo completo ----------
def test_flujo_completo(cliente, ana, carlos, sql):
    # 1. Ana publica
    r = cliente.post("/api/flujo/publicar-objeto", json={"codigo": "OBJ-9001", "nombre": "Calculadora TI-84",
                                                     "id_categoria": 1, "id_condicion": 1}, headers=ana)
    assert r.status_code == 201; obj = r.json()
    assert obj["disponible"] is True
    # 2. Carlos solicita
    hoy = date.today()
    r = cliente.post("/api/flujo/solicitar", json={"id_objeto": obj["id_objeto"], "fecha_inicio_deseada": str(hoy),
                                               "fecha_fin_deseada": str(hoy + timedelta(days=5)), "mensaje": "Para parcial"}, headers=carlos)
    assert r.status_code == 201; sol = r.json()
    assert sol["codigo"].startswith("SOL-")
    # Ana no puede solicitar su propio objeto
    assert cliente.post("/api/flujo/solicitar", json={"id_objeto": obj["id_objeto"], "fecha_inicio_deseada": str(hoy),
                                                  "fecha_fin_deseada": str(hoy)}, headers=ana).status_code == 400
    # 3. Carlos no puede aprobar (no es dueño); Ana aprueba
    assert cliente.post(f"/api/flujo/solicitudes/{sol['id_solicitud']}/decision", json={"aprobar": True}, headers=carlos).status_code == 403
    r = cliente.post(f"/api/flujo/solicitudes/{sol['id_solicitud']}/decision", json={"aprobar": True}, headers=ana)
    assert r.status_code == 200
    # 4. Ana registra el préstamo -> objeto no disponible
    r = cliente.post(f"/api/flujo/solicitudes/{sol['id_solicitud']}/prestar", json={}, headers=ana)
    assert r.status_code == 201; prestamo = r.json()
    assert cliente.get(f"/api/objetos/{obj['id_objeto']}", headers=ana).json()["disponible"] is False
    disponibles = [o["id_objeto"] for o in cliente.get("/api/flujo/objetos-disponibles", headers=carlos).json()]
    assert obj["id_objeto"] not in disponibles
    mis = cliente.get("/api/flujo/mis-prestamos", headers=carlos).json()
    assert any(p["id_prestamo"] == prestamo["id_prestamo"] and p["rol_en_prestamo"] == "prestatario" for p in mis)
    # El estudiante no puede crear préstamos saltándose el flujo
    assert cliente.post("/api/prestamos", json={"id_solicitud": sol["id_solicitud"], "fecha_devolucion_esperada": str(hoy),
                                            "id_condicion_entrega": 1}, headers=carlos).status_code == 403
    # 5. Devolución -> disponible y condición registrada
    r = cliente.post(f"/api/flujo/prestamos/{prestamo['id_prestamo']}/devolver",
                     json={"id_condicion_devolucion": 2, "observaciones": "Leve rayón"}, headers=ana)
    assert r.status_code == 201
    o = cliente.get(f"/api/objetos/{obj['id_objeto']}", headers=ana).json()
    assert o["disponible"] is True and o["id_condicion"] == 2
    assert cliente.post(f"/api/flujo/prestamos/{prestamo['id_prestamo']}/devolver",
                        json={"id_condicion_devolucion": 2}, headers=ana).status_code == 409
    # 6. Calificación y notificaciones
    r = cliente.post("/api/calificaciones", json={"id_prestamo": prestamo["id_prestamo"], "id_evaluado": 5, "puntaje": 5,
                                              "comentario": "Puntual"}, headers=ana)
    assert r.status_code == 201
    assert len(cliente.get("/api/flujo/mis-notificaciones", headers=carlos).json()) >= 3


def test_rechazo_solicitud(cliente, ana, carlos):
    hoy = str(date.today())
    obj = cliente.post("/api/flujo/publicar-objeto", json={"codigo": "OBJ-RECHAZO", "nombre": "Regla T", "id_categoria": 1,
                                                           "id_condicion": 1}, headers=ana).json()
    sol = cliente.post("/api/flujo/solicitar", json={"id_objeto": obj["id_objeto"], "fecha_inicio_deseada": hoy, "fecha_fin_deseada": hoy},
                       headers=carlos).json()
    r = cliente.post(f"/api/flujo/solicitudes/{sol['id_solicitud']}/decision", json={"aprobar": False}, headers=ana)
    assert r.status_code == 200 and r.json()["id_estado_solicitud"] == 3
    # no se puede prestar una solicitud rechazada
    assert cliente.post(f"/api/flujo/solicitudes/{sol['id_solicitud']}/prestar", json={}, headers=ana).status_code == 409
