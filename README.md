# Legal Intake AI

Demo sencilla de triaje preliminar para consultas legales. Recibe un caso escrito, minimiza identificadores directos y devuelve un análisis estructurado con posibles servicios de Ático34.

Puede funcionar de dos maneras:

- **Mock:** offline, determinista y sin credenciales.
- **Gemini:** llamada real con salida estructurada validada por Pydantic.

> Es una herramienta de demostración. No sustituye la revisión profesional ni constituye asesoramiento legal definitivo.

## Flujo

```text
Formulario web
  -> FastAPI
  -> minimización de email, teléfono, DNI/NIE e IBAN
  -> provider mock o Gemini
  -> respuesta validada con Pydantic
  -> resultado en el navegador
```

Las recomendaciones de Gemini se limitan a los servicios definidos en `docs/atico34_knowledge.md`.

## Stack

- Python 3.12
- FastAPI y Uvicorn
- Pydantic v2
- Google GenAI SDK
- HTML, CSS y JavaScript vanilla
- pytest
- Docker y Docker Compose

## Ejecución local

Instala las dependencias:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Crea la configuración local:

```powershell
Copy-Item .env.example .env
```

Para utilizar el modo mock:

```ini
DEMO_MODE=true
```

Arranca la aplicación:

```powershell
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Abre <http://localhost:8000>.

## Modo Gemini

Configura `.env` sin publicar la clave:

```ini
DEMO_MODE=false
GEMINI_API_KEY=<tu-clave>
GEMINI_MODEL=gemini-2.5-flash-lite
```

Reinicia la aplicación después de cambiar la configuración. Si Gemini no está disponible, vuelve a `DEMO_MODE=true` para usar la demo offline.

## Docker

```powershell
docker compose up --build
```

La aplicación estará disponible en <http://localhost:8000>.

## Endpoints

| Método | Ruta | Descripción |
|---|---|---|
| `GET` | `/` | Interfaz web. |
| `GET` | `/health` | Comprobación de disponibilidad. |
| `POST` | `/api/demo/messages` | Analiza un mensaje. |
| `GET` | `/docs` | Documentación interactiva de la API. |
| `GET` | `/openapi.json` | Esquema OpenAPI. |

## Pruebas

```powershell
python -m pytest -q
```

Las pruebas utilizan el provider mock y no realizan llamadas reales a Gemini.

## Estructura

```text
app/
├── api/         # Endpoints FastAPI
├── core/        # Configuración
├── models/      # Contratos Pydantic
├── services/    # Privacidad y providers
└── static/      # Interfaz web

tests/           # Pruebas automatizadas
docs/            # Conocimiento y documentación
specs/           # Especificación del proyecto
```

La implementación actual es una demo síncrona y sin persistencia, autenticación ni integración con Twilio.
