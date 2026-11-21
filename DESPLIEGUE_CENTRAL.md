# Base general en línea (modo central)

Cada laptop trabaja **sin internet** con su propia copia de EIRA. Cuando hay conexión, sube sola sus pacientes, campañas y atenciones a la **base general**, que vive en un servidor en internet. Las laptops **solo suben**: ninguna descarga datos de otras, así que una laptop perdida solo contiene lo que ella capturó.

```
 Laptop brigada 1 ─┐
 Laptop brigada 2 ─┼──(HTTPS, cuando hay internet)──►  Base general (servidor)
 Laptop brigada 3 ─┘                                    · une a la misma persona por CURP
                                                        · deja dudas en «Repetidas»
                                                        · asigna el ID definitivo EIRA-<programa>-xxxxxx
```

## Lo que la empresa tiene que contratar

| Concepto | Para qué | Costo aproximado* |
|---|---|---|
| Servidor virtual (VPS) Linux, 1 vCPU, 1–2 GB RAM, 25 GB de disco | Donde corre la base general | 5 a 12 USD al mes (DigitalOcean, Linode/Akamai, Hetzner, Vultr, AWS Lightsail…) |
| Dominio (p. ej. `eira-movimientorosa.org`) | Dirección fija y certificado HTTPS | 10 a 20 USD al año |
| Correo de salida (SMTP) | Avisos de eliminación a Administración | 0 USD con una cuenta Gmail/Workspace existente |
| Copia externa de respaldos (opcional) | Guardar respaldos fuera del servidor | 0 a 5 USD al mes |

\*Precios de referencia de noviembre de 2026; confírmalos con el proveedor. El certificado HTTPS es gratuito (Let's Encrypt, automático).

Con unas decenas de laptops y decenas de miles de atenciones, el servidor más pequeño es suficiente.

## Instalación en el servidor (la hace una persona técnica, ~30 minutos)

1. Crea el servidor con Ubuntu e instala Docker (`curl -fsSL https://get.docker.com | sh`).
2. En el proveedor del dominio, crea un registro **A** que apunte el dominio a la IP del servidor.
3. Copia la carpeta de EIRA al servidor y, dentro de ella, crea el archivo `.env`:
   ```
   EIRA_DOMINIO=eira.tu-dominio.org
   ```
4. Inicia: `docker compose up -d --build`. En unos minutos `https://eira.tu-dominio.org` muestra el inicio de sesión (Caddy obtiene el certificado solo).
5. Crea la cuenta de Administración de la central: `docker compose exec eira flask --app eira create-admin`.

La base y las llaves de cifrado quedan en el volumen `eira_instance`, y los respaldos automáticos (cada hora) en `eira_respaldos`. **Respalda las llaves** (`docker compose cp eira:/app/instance ./llaves-eira`) y guárdalas fuera del servidor.

## Vincular cada laptop

1. En la base general: **Equipos → Crear código de vinculación** (por ejemplo «Laptop brigada Chiapas 1»). Copia el código; solo se muestra una vez.
2. En la laptop, como Administración: **Sincronizar → Vincular**, escribe la dirección `https://eira.tu-dominio.org` y el código.
3. Listo. Lo pendiente sube cada minuto en cuanto hay internet; también hay un botón «Sincronizar ahora».

Si una laptop se pierde o la roban: **Equipos → Revocar**. Desde ese momento su código ya no sirve.

## Cómo se evitan duplicados entre laptops

- Cada paciente, campaña y atención lleva un identificador único; si se reenvía (por ejemplo, porque se cortó la conexión), la central no la duplica.
- **Misma CURP** → se une sola al mismo expediente.
- **Nombre parecido sin CURP** → se crea el expediente y aparece en **Repetidas** para que Administración elija «Es la misma persona» (se suman las atenciones) o «Personas diferentes».
- La misma campaña (nombre + lugar) capturada en varias laptops queda como una sola campaña.
- La misma atención (persona, campaña, servicio y fecha) desde dos laptops cuenta una sola vez.

## Seguridad

- Solo HTTPS (las laptops rechazan direcciones `http://`, salvo el mismo equipo para pruebas).
- Cada laptop usa su propio código; en la central solo se guarda su huella (hash).
- La central vuelve a cifrar los datos sensibles con sus propias llaves.
- Cada envío queda en la bitácora con el equipo y su IP; 20 intentos fallidos desde una IP la bloquean 15 minutos.
- Antes de usar datos reales, publica un aviso de privacidad conforme a la LFPDPPP (datos de salud = datos sensibles).

## Probar sin servidor (en una sola computadora)

```bash
python run.py --central --puerto 8100 --sin-navegador   # base general de prueba
python run.py                                           # laptop (puerto 8000)
```
En la central de prueba crea un equipo; en la laptop vincúlala con `http://localhost:8100`.
