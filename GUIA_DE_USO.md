# Guía de uso de EIRA (sin conocimientos de programación)

Esta guía explica, paso a paso, cómo instalar y usar la plataforma EIRA Movimiento Rosa en una computadora, sin necesidad de saber programar.

---

## 1. ¿Qué es EIRA?

Es una página web que funciona **en tu propia computadora**, incluso sin internet. Sirve para:

- organizar el trabajo por **campañas** (nombre, tipo, lugar y fechas);
- registrar en cada campaña a las pacientes atendidas, el servicio que recibieron, quién las atendió y las notas de seguimiento;
- dar un **ID** a cada paciente nueva y, si ya existía, sumar la atención a su expediente y contar cuántas veces se le ha atendido;
- cargar bases de datos de Excel o CSV, limpiarlas y juntarlas sin contar dos veces a la misma persona;
- ver indicadores (cuántas personas se atendieron, por programa, por municipio, etc.).

Los datos delicados (CURP, teléfono, notas) se guardan **cifrados**: aunque alguien copie el archivo de la base, no podrá leerlos.

---

## 2. Instalación (solo la primera vez)

### Paso 1. Instalar Python

EIRA necesita un programa gratuito llamado **Python**.

1. Entra a https://www.python.org/downloads/ y presiona el botón amarillo **Download Python**.
2. Abre el archivo descargado.
3. **Importante (Windows):** antes de presionar *Install Now*, marca la casilla **"Add python.exe to PATH"**.
4. Termina la instalación.

> En Mac también puedes instalarlo desde esa página. En Linux normalmente ya viene instalado.

### Paso 2. Descomprimir EIRA

1. Descarga el archivo `eira-plataforma.zip`.
2. Haz clic derecho → **Extraer todo** (Windows) o doble clic (Mac).
3. Se creará una carpeta llamada `eira-plataforma`.

La primera vez se necesita internet (unos 2 minutos) para descargar componentes. Después ya **no** hace falta internet.

---

## 3. Abrir la plataforma

| Sistema | Qué hacer |
|---|---|
| **Windows** | Abre la carpeta `eira-plataforma` y haz **doble clic en `iniciar.bat`** |
| **Mac / Linux** | Abre la aplicación *Terminal*, arrastra el archivo `iniciar.sh` a la ventana y presiona Enter |

Se abrirá una ventana negra con mensajes (no la cierres: es el "motor" de la plataforma) y, después de unos segundos, el navegador se abrirá solo en:

**http://localhost:8000**

Si el navegador no se abre solo, escribe esa dirección en Chrome, Edge o Firefox.

Para **apagar** la plataforma, cierra la ventana negra (o presiona `Ctrl + C` dentro de ella).

### ¿Quieres ver datos de ejemplo?

En Windows, abre la ventana *Símbolo del sistema* dentro de la carpeta y escribe `iniciar.bat --demo`. En Mac/Linux: `./iniciar.sh --demo`. Esto carga cuentas de prueba y **todos los datos sintéticos** (campañas rurales y bases de entrenamiento) para practicar; tarda 1 o 2 minutos la primera vez y solo funciona con una base vacía.

---

## 4. Cuentas y direcciones de cada rol

La plataforma es **solo para médicos, personal de campaña y administración**. Las pacientes no tienen cuenta: su información la registra el personal.

La primera vez que se abre, EIRA crea una cuenta de cada rol. Todas entran por **http://localhost:8000/login** y llegan a **Campañas** (http://localhost:8000/campanas/).

| Rol | Usuario | Contraseña inicial |
|---|---|---|
| Administración | `admin` | `Admin-EIRA-2026` |
| Médico / personal clínico | `clinica` | `Clinica-EIRA-2026` |

Al entrar por primera vez, la plataforma **pide cambiar la contraseña**. Hazlo y guárdala en un lugar seguro.

### Páginas principales

**Médico / personal clínico:**
- Campañas: `/campanas/` · Pacientes: `/clinica/pacientes` · Panel de indicadores: `/clinica/`

**Administración** (todo lo anterior, más):
- Usuarios, roles y solicitudes de acceso: `/admin/usuarios`
- Importar bases de Excel/CSV: `/admin/importar`
- Bitácora (quién hizo qué): `/admin/bitacora`
- Cerrar o reabrir una campaña.

Si alguien intenta abrir una página que no le corresponde, la plataforma lo bloquea.

---

## 5. Trabajar por campañas

### Crear una campaña
1. Menú **Campañas** → formulario **Nueva campaña**.
2. Escribe el **nombre**, elige el **tipo**, escribe el **lugar** (y municipio) y la fecha de inicio.
3. Presiona **Crear campaña**.

### Registrar a una paciente atendida
Dentro de la campaña, llena **Registrar paciente atendida**:
- **Nombre completo** (obligatorio). Si los tienes, fecha de nacimiento o edad, CURP, teléfono y municipio: ayudan a reconocer si la persona ya estaba registrada.
- **Servicio** que recibió (por ejemplo Mastografía); el tipo de servicio se llena solo.
- **Nombre de quien atiende**.
- **Datos generales** del servicio y **notas de seguimiento**.

Al presionar **Guardar atención** pueden pasar tres cosas:

| Situación | Qué hace la plataforma |
|---|---|
| La persona no está en la base | Crea su expediente y le **genera un ID** (por ejemplo `EIRA-2-006253`). |
| Hay registros parecidos | Muestra la pantalla **«¿Es la misma persona?»** con las coincidencias (nombre, edad, municipio, teléfono) y sus atenciones previas. |
| La CURP ya existe | La reconoce como la misma persona y agrega el servicio. |

En la pantalla de verificación:
- **«Es la misma: agregar servicio»**: el servicio se agrega a su expediente y aumenta el número de **veces atendida**. Si traía datos que faltaban (teléfono, CURP…), se completan.
- **«Es una persona diferente: generar ID nuevo»**: se crea otro expediente con su propio ID.

Si por error se guarda dos veces el mismo servicio, a la misma persona, en la misma campaña y fecha, la plataforma no lo duplica.

Las veces que se ha atendido a cada paciente aparecen en la lista de pacientes, en su expediente y en la tabla de atenciones de la campaña.

### Cómo leer el ID de una paciente

`EIRA-2-006253`: el número de en medio es el programa (1 Jornadas Médicas, 2 Detección Oportuna, 3 Acompañamiento Integral, 4 Apoyo en Especie, 5 Educación y Comunidad, 0 sin programa) y el último identifica a la persona. Si cambia su programa, solo cambia el número de en medio. En Pacientes puedes buscarla también sin ese número (`EIRA-006253`).

### Filtrar pacientes

En **Pacientes** puedes filtrar por programa, municipio, campaña, servicio recibido, sexo, rango de edad y expedientes activos o desactivados, y combinarlos. «Quitar filtros» vuelve a la lista completa.

### Solicitar acceso (personal nuevo)
1. En la página de inicio de sesión, presiona **«Solicita acceso»** (o entra a http://localhost:8000/registro).
2. Llena nombre, cargo, usuario y contraseña y presiona **Enviar solicitud**.
3. La cuenta queda **inactiva** hasta que Administración la apruebe.

### Aprobar solicitudes (solo Administración)
Menú **Usuarios** → pestaña **Solicitudes de acceso** → elige el rol (Médico / personal clínico o Administración) y presiona **Aprobar**, o **Rechazar**. Todo queda en la bitácora.

---

### Ver los datos sensibles de una paciente

Los datos como CURP, teléfono o domicilio aparecen ocultos (`••••`). Para verlos:

1. Abre el expediente de la paciente.
2. Presiona **Ver datos sensibles**.
3. Escribe la **contraseña de paso**. La inicial es `EIRA_2026`; el motivo es opcional.

Cada vez que alguien ve estos datos queda anotado en la bitácora con su usuario. Si se equivoca 5 veces, debe esperar 15 minutos.

**Administración debe cambiar la contraseña de paso** antes de usar datos reales: menú **Usuarios** → **Contraseña de paso**.

### Asistente de ayuda (botón «?» abajo a la derecha)

Pregúntale cosas como «¿cómo creo una campaña?», «¿qué hago si una persona sale repetida?» o «¿cómo importo un Excel?». Funciona sin internet.

Si alguien le pide datos de pacientes (por ejemplo «dame la CURP de…» o «lista de pacientes de…»), el asistente **bloquea la solicitud** y pide la contraseña de paso. Aun con la contraseña, solo muestra un enlace al expediente; nunca escribe datos personales en el chat.

### Respaldos y registro de accesos (solo Administración)

- **Respaldos automáticos:** la plataforma guarda una copia de la base al iniciar y otra cada hora en la carpeta `respaldos`, y conserva las 48 más recientes. Si alguien borra la base, basta con cerrar y volver a abrir EIRA: se recupera sola con la copia más reciente. También puedes crear una copia en Bitácora → Respaldos → «Crear respaldo ahora».
- **Nada se borra:** los expedientes, atenciones, campañas, cuentas y la bitácora no se pueden borrar ni desde la base.
- **Accesos por IP:** en Bitácora → «Accesos por IP» se ve cada entrada a la plataforma: fecha, IP del equipo, usuario, página y resultado. Puedes filtrar por IP o por usuario. Este registro tampoco se puede borrar.

### Eliminar registros (con aprobación de Administración)

1. Abre el expediente de la paciente y marca la casilla de los registros que quieres eliminar.
2. Abre «Eliminar registros seleccionados…», escribe el motivo y la **contraseña de paso**, y presiona «Solicitar eliminación».
3. Todas las cuentas de Administración reciben un correo. Cada una entra a **Eliminaciones** y presiona «Aceptar eliminación» o «Rechazar».
4. Los registros solo se eliminan cuando **todas** aceptan. Si una rechaza, no se elimina nada.

Para que lleguen los correos, Administración configura una vez **Bitácora → Avisos por correo** (servidor de correo y el correo de cada cuenta de Administración). Si no hay internet, los avisos esperan y se envían al volver la conexión.

### Subir lo capturado a la base general

Cada laptop trabaja sin internet. Cuando hay conexión, sube sola lo capturado a la base general; en **Sincronizar** ves cuánto falta por subir y puedes presionar «Sincronizar ahora». Las pacientes nuevas tienen un ID provisional (TMP-…) hasta que la base general les da el definitivo (EIRA-…). Cómo contratar e instalar la base general: `DESPLIEGUE_CENTRAL.md`.

## 6. Cargar y limpiar bases de Excel o CSV (Administración)

1. Menú **Importar** → elige uno o varios archivos (`.xlsx` o `.csv`) → **Cargar**.
2. **Mapear columnas:** la plataforma adivina qué es cada columna (nombre, edad, fecha, etc.). Revisa y corrige si hace falta → **Limpiar y evaluar con semáforo**.
3. **Revisar el semáforo:**
   - **Verde:** listo para guardar.
   - **Ámbar:** revisar (posible duplicado o dato que no cuadra, por ejemplo la edad no coincide con la CURP).
   - **Rojo:** falta un dato obligatorio o tiene un formato imposible. Presiona **Corregir fila**, arregla el dato y se vuelve a evaluar.
   - Puedes filtrar por tipo de problema con los botones de arriba de la tabla.
4. Presiona **Integrar a la base principal**. Las personas repetidas se juntan en un solo expediente y los eventos duplicados no se vuelven a contar.

También puedes descargar el **Reporte de calidad**, que lista los problemas fila por fila sin mostrar datos personales.

---

### Datos de prueba de zonas rurales

Las carpetas `datos_rurales` y `datos_rurales_ronda1` a `datos_rurales_ronda3` traen bases **inventadas** que simulan campañas de EIRA en comunidades rurales de Chiapas, Oaxaca y Guerrero (64 campañas cada una). Con `--demo` ya quedan cargadas en la plataforma; también sirven para practicar la importación:

- `fuente_C_campanas_rurales.csv` y `fuente_D_brigadas_rurales.xlsx` se cargan juntos en **Importar**.
- Al integrarlos se crean las campañas y cada atención queda ligada a la suya.

La plataforma ya viene entrenada con todos estos datos y con los del Reto 3, en 3 rondas (reportes en `reportes_entrenamiento`).

## 7. La base de datos en MySQL / MariaDB

En la carpeta `base_datos` está el archivo **`eira_mysql.sql`**: una copia de toda la base (pacientes, cuentas con su rol, campañas, registros de atención y bitácora) lista para abrir en MySQL o MariaDB. Contiene los datos de ejemplo del Reto 3 ya limpios e integrados.

### Cómo abrirla

**Con phpMyAdmin (XAMPP, hosting, etc.):**
1. Entra a phpMyAdmin → pestaña **Importar**.
2. Elige el archivo `eira_mysql.sql` → **Continuar**.
3. Aparecerá una base llamada `eira`.

**Con MySQL Workbench:** menú *Server* → *Data Import* → *Import from Self-Contained File* → elige `eira_mysql.sql` → *Start Import*.

### Qué contiene

| Tabla o vista | Qué tiene |
|---|---|
| `roles` | Los roles y lo que puede hacer cada uno |
| `usuarios` | Cuentas de acceso con su rol (la contraseña no se guarda, solo un código irreversible) |
| `pacientes` | Un expediente por persona única |
| `campanas` | Campañas: nombre, tipo, lugar y fechas |
| `registros` | Atenciones: servicio, campaña, quién atendió, datos generales, notas de seguimiento, archivo y folio de origen |
| `bitacora` | Historial de acciones (no se puede modificar ni borrar) |
| `v_personas_con_rol` | **Todas las personas con su rol** (personal y pacientes) |
| `v_registros_con_rol` | Cada registro con la paciente y el rol de quien lo capturó |
| `v_pacientes_veces_atendida` | Cuántas veces se ha atendido a cada paciente |
| `v_atenciones_campana` | Las atenciones de cada campaña |

Para ver todas las personas con su rol, ejecuta:

```sql
SELECT * FROM eira.v_personas_con_rol;
```

### Generar una copia nueva con tus propios datos

Con la plataforma apagada, abre una terminal en la carpeta y escribe:

```
.venv\Scripts\python.exe herramientas\exportar_mysql.py --cifrado      (Windows)
.venv/bin/python herramientas/exportar_mysql.py --cifrado              (Mac/Linux)
```

> **Con datos reales usa siempre `--cifrado`.** Sin esa opción, los datos sensibles quedan legibles en el archivo y cualquiera que lo tenga podría leerlos.

---

## 8. Problemas frecuentes

| Problema | Solución |
|---|---|
| "No se encontró Python" | Reinstala Python marcando **"Add python.exe to PATH"** (paso 2.1) |
| El navegador dice "No se puede acceder a este sitio" | Revisa que la ventana negra siga abierta. Usa la dirección que aparece en ella (puede ser `:8001` si el puerto 8000 estaba ocupado) |
| "El formulario expiró" | Recarga la página (F5) y vuelve a intentar |
| Olvidé mi contraseña | Una persona de Administración entra a **Usuarios** → **Restablecer contraseña** y te da una temporal |
| La cuenta se bloqueó | Tras 5 intentos fallidos se bloquea 15 minutos. Administración puede desbloquearla en **Usuarios** |
| Quiero usarla desde otras computadoras de la oficina | Inicia con `iniciar.bat --red`; la ventana negra mostrará la dirección para las demás computadoras de la misma red |

---

## 9. Cuidados importantes

- **Copia a una memoria USB** las carpetas `respaldos` e `instance` (esta última tiene las llaves de cifrado) y guárdala bajo llave. Sin las llaves, ni la base ni los respaldos se pueden leer.
- No compartas el archivo `eira_mysql.sql` si contiene datos reales sin cifrar.
- Cambia las contraseñas iniciales en cuanto entres.
- Si la vas a publicar en internet, pide a una persona técnica que active HTTPS (ver `README.md`).
