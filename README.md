# Plataforma EIRA Movimiento Rosa

**¿No programas? Lee primero la [Guía de uso](GUIA_DE_USO.md).**

Aplicación local-first (funciona sin internet) para el personal de EIRA: campañas, registro de pacientes atendidas con ID automático y verificación de personas repetidas, conteo de veces atendida e importación de fuentes CSV/Excel con semáforo de calidad. Uso exclusivo de médicos y administración.

## Iniciar

Requisitos: Python 3.10+. Solo se necesita internet la primera vez para instalar dependencias (o copia la carpeta `.venv` / wheels a la máquina sin conexión).

```bash
./iniciar.sh --demo          # Linux / macOS (Windows: iniciar.bat --demo)
# o manualmente
pip install -r requirements.txt
python run.py --demo         # http://127.0.0.1:8000
python run.py --red          # disponible para otros equipos de la red local
```

Sin `--demo`, crea la primera cuenta con `flask --app eira create-admin`.

Cuentas demo (datos ficticios): `admin / Admin-EIRA-2026`, `clinica / Clinica-EIRA-2026`. El registro abierto (`/registro`) crea solicitudes de acceso inactivas que Administración aprueba y a las que asigna rol.

## Roles

| Rol | Puede |
|---|---|
| Administración | Todo lo clínico + aprobar solicitudes y asignar roles, cerrar campañas, bitácora, importación CSV/XLSX |
| Médico / personal clínico | Crear campañas; registrar atenciones (servicio, quién atiende, datos generales, seguimiento); ID automático para pacientes nuevas; confirmar si una posible repetida es la misma persona; buscar y editar pacientes; indicadores |

## Protección de la información

- CURP, teléfono, correo, domicilio, contacto de emergencia, notas y detalles se guardan cifrados (Fernet). Búsqueda exacta por CURP/teléfono con HMAC, sin guardar el dato en claro.
- Datos enmascarados por defecto; verlos completos exige la **contraseña de paso** (inicial `EIRA_2026`, guardada con hash; Administración la cambia en Usuarios → Contraseña de paso o con `EIRA_CLAVE_PASO` antes del primer arranque). Cada acceso queda en la bitácora con el usuario; 5 intentos fallidos bloquean 15 min.
- Asistente de ayuda (botón «?» abajo a la derecha): responde dudas de uso sin internet, con reglas locales. Bloquea pedidos de datos sensibles (CURP, teléfonos, listas de pacientes, exportaciones, intentos de «ignora tus instrucciones») y pide la contraseña de paso; aun con ella solo da enlaces al expediente, nunca datos personales en el chat. Todo intento queda en la bitácora.
- Bitácora inalterable (triggers impiden editar/borrar), CSRF, bloqueo tras 5 intentos fallidos, sesiones de 20 min, cabeceras CSP/no-store.
- Sin exportación masiva de datos personales: solo indicadores agregados y bitácora (admin).
- Expedientes se desactivan, no se borran: triggers impiden `DELETE` en pacientes, atenciones, campañas y cuentas.
- **Registro de accesos con IP** (`access_log`, solo lectura por trigger): cada solicitud guarda fecha, IP, usuario, método, ruta, código de respuesta y navegador; no guarda parámetros de búsqueda ni mensajes del asistente. Administración lo consulta en Bitácora → Accesos por IP (`/admin/accesos`).
- **Respaldos automáticos** (`eira/respaldos.py`): copia consistente con la API de respaldo de SQLite al iniciar y cada hora, verificada con `PRAGMA integrity_check`; se conservan las 48 más recientes en `respaldos/` (o `EIRA_RESPALDOS`, idealmente otro disco). Si la base desaparece, al arrancar se restaura sola desde el respaldo más reciente y queda en la bitácora. Respaldo manual en `/admin/respaldos`; restauración manual con `python herramientas/restaurar_respaldo.py --ultimo` (con la plataforma detenida). Los respaldos conservan cifrados los datos sensibles, así que necesitan las mismas llaves de `instance/`.
- El modo offline (PWA) solo guarda estilos y la página "sin conexión"; nunca páginas con datos de pacientes.

Las llaves se generan en `instance/` (permiso 0600). En producción defínelas por variable de entorno (`EIRA_SESSION_KEY`, `EIRA_DATA_KEY`, `EIRA_INDEX_KEY`), respáldalas aparte de la base y usa HTTPS (`EIRA_HTTPS=1`). Perder `EIRA_DATA_KEY` hace ilegibles los datos cifrados.

## Cargar, limpiar e integrar bases CSV/Excel (administración)

`Administración → Importar`:

1. **Cargar:** uno o varios CSV/XLSX a la vez (cada hoja de Excel es una fuente; se ignoran títulos y filas vacías). Máximo 15 MB, 10 fuentes y 20 000 filas.
2. **Mapear:** columnas de cada fuente al diccionario común, incluidas las de campaña (campaña/brigada, tipo, lugar/sede, quién atendió, datos generales, notas de seguimiento): al integrar, cada atención queda ligada a su campaña (se crea si no existe). Se sugiere automáticamente por encabezado y por contenido (p. ej. una columna «Notas» que trae el tipo de registro). Admite nombre en una columna o separado en nombre(s) + apellidos, edad en lugar de fecha de nacimiento y folio de origen para trazabilidad.
3. **Limpiar y revisar:** limpieza automática con vista antes → después:
   - nombres y municipios con mayúsculas/espacios correctos; «N/A», «sin dato» se vacían;
   - fechas en cualquier formato común (incluye «15 de marzo de 1978», «15-mar-78» y fechas numéricas de Excel);
   - teléfonos a 10 dígitos (quita +52, 044…), CURP sin espacios; sexo y fecha de nacimiento desde la CURP si faltan;
   - programa, tipo de registro y municipio ajustados al catálogo.

   Semáforo: **Verde** listo · **Ámbar** posible duplicado con la base o entre fuentes, evento ya registrado o dato a revisar (vincular, crear u omitir; hay acciones masivas) · **Rojo** faltantes o formatos inválidos: se puede **corregir la fila en pantalla** y se reevalúa.
   El reporte de calidad (CSV) lista problemas por fila sin datos personales.
4. **Integrar:** crea expedientes, vincula a existentes completando solo campos vacíos, agrega registros sin duplicar eventos. Todo queda en la bitácora con fuente y fila.

### Modelo de calidad entrenado

Los diccionarios (variantes de municipios, actividades → tipo, tipo → programa, valores de tipo) y los umbrales de deduplicación están en `eira/modelo_calidad.json`. Se entrenan con datos etiquetados:

```bash
python herramientas/generar_sinteticos_rurales.py                    # regenera datos_rurales/
python herramientas/generar_sinteticos_rurales.py datos_rurales_ronda4 --semilla 2030 --serie R4   # ronda nueva
python herramientas/entrenar_calidad.py datos_entrenamiento datos_rurales datos_rurales_ronda1 datos_rurales_ronda2 datos_rurales_ronda3
```

`datos_rurales/` y `datos_rurales_rondaN/` son bases 100 % sintéticas de campañas en municipios rurales de Chiapas, Oaxaca y Guerrero (ver `diccionario_datos.md` de cada una). Cada ronda usa otra semilla (otras personas y campañas) y su propio prefijo de folios. El modelo se entrenó en 3 rondas acumulativas; los reportes de cada ronda están en `reportes_entrenamiento/`.

`run.py --demo` (base vacía) carga las cuentas demo y además integra todas esas fuentes con el flujo de importación, así que la plataforma arranca con los datos sintéticos ya cargados (1–2 minutos la primera vez).

Solo la partición `train` se usa para ajustar; `val` y `test` miden el resultado (`datos_entrenamiento/reporte_entrenamiento.md`). Con la base sintética del Reto 3 (10 000 filas): semáforo correcto en 99.7 % de test, 100 % de duplicados detectados y personas únicas estimadas 935 vs 932 reales.

Reglas: **Rojo** = dato faltante (nombre, fecha del evento, identidad) o formato inválido (CURP, fechas imposibles, edad, teléfono). **Ámbar** = duplicado probable (misma persona, mismo tipo, fechas a ±1 día, entre fuentes o contra la base) o discrepancia (edad/fecha vs CURP, evento futuro, edad improbable, edad distinta en otro registro de la misma persona). **Verde** = sin problemas (aunque se vincule a la misma persona en otro evento).

El tablero separa personas únicas de eventos con filtros por programa, periodo, municipio y tipo. Ejemplos en `ejemplos/` (incluye `fuente_desordenada.xlsx`).

## Laptops sin conexión + base general en línea

Cada laptop corre EIRA en modo local (sin internet) y sube lo que capturó a la base general (`python run.py --central`, o Docker: ver [DESPLIEGUE_CENTRAL.md](DESPLIEGUE_CENTRAL.md)). Solo sube; nunca descarga datos de otras laptops.

- **Vinculación:** la central genera un código por equipo (Equipos); en la laptop, Sincronizar → Vincular (exige `https://`). El código se guarda cifrado en la laptop y como hash SHA-256 en la central; se revoca por equipo.
- **Envío:** `POST /api/sync/subir` en lotes (100 pacientes / 400 atenciones), cada minuto si hay pendientes, o con «Sincronizar ahora». Cada fila lleva un `uuid`; reenviar no duplica. Pacientes editadas después de subir se reenvían y la central solo completa campos vacíos.
- **IDs:** con equipo vinculado, las pacientes nuevas tienen ID provisional `TMP-…`; la central responde con el ID definitivo `EIRA-…` y la laptop lo adopta.
- **Repetidas entre equipos:** misma CURP → mismo expediente; nombre parecido → bandeja «Repetidas» (`/admin/revision-repetidas`) para unir o separar. Misma campaña (nombre + lugar) y misma atención (persona, campaña, servicio, fecha) no se duplican.

## Eliminación de registros

En el expediente se marcan los registros y se pide la eliminación con motivo y **contraseña de paso**. Se envía un correo (SMTP configurable en Bitácora → Avisos por correo; cola con reintentos si no hay internet) a todas las cuentas de Administración, sin datos de pacientes. Solo se elimina cuando **todas** las cuentas de Administración activas aceptan en `/admin/eliminaciones`; un rechazo cancela. Lo eliminado se archiva cifrado en `records_eliminados` y un trigger impide cualquier otro `DELETE` sobre `records`.

## Pruebas

```bash
pip install -r requirements-dev.txt && python -m pytest -q
```
