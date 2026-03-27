# Mock Backend API con FastAPI

Este es un mock server implementado en **FastAPI** que expone endpoints con respuestas JSON hardcodeadas. Incluye un sistema de autenticación real basado en JSON Web Tokens (JWT) que genera un `access_token` y un `refresh_token`. El resto de los endpoints están protegidos y requieren el `access_token` para ser consumidos.

## Requisitos Previos

* Python 3.8+
* `pip3` para la instalación de paquetes.

## Instalación

1. Clona o ubícate en la carpeta raíz del proyecto.
2. (Opcional pero recomendado) Crea y activa un entorno virtual:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # En Mac/Linux
   # venv\Scripts\activate   # En Windows
   ```
3. Instala las dependencias necesarias leyendo el archivo `requirements.txt`:
   ```bash
   pip3 install -r requirements.txt
   ```

## Ejecución

Inicia el servidor en modo desarrollo utilizando `uvicorn`. Para permitir el acceso desde la red local (no solo localhost), usamos `--host 0.0.0.0`:

```bash
uvicorn main:app --host 0.0.0.0 --reload
```

O si prefieres, puedes ejecutar directamente el archivo script:
```bash
python main.py
```

La aplicación se levantará en `http://127.0.0.1:8000` y también será accesible a través de la dirección IP local de tu computadora (por ejemplo, `http://192.168.1.X:8000`).

## Documentación API Interactiva (Swagger)

FastAPI genera automáticamente documentación interactiva.
Ingresa a la siguiente URL en tu navegador:

👉 **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**

### ¿Cómo probarlo?

1. Ve a la documentación interactiva e interactúa con el endpoint `POST /api/v1/auth/login`. Envía el JSON predeterminado en el body para obtener un token de acceso.
2. Copia el valor de `access_token` devuelto.
3. Sube a la parte superior de la página y haz clic en el botón **`Authorize`**.
4. Pega tu token en el campo de texto y haz clic en "Authorize".
5. ¡Listo! Ahora puedes probar los demás endpoints (por ejemplo, el cálculo de tickets, pagos, validación de ingresos) presionando **`Try it out`** y luego **`Execute`**, y las peticiones enviarán automáticamente el encabezado de autenticación.
