from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.api.schemas import PolishRequest, PolishResponse
from app.errors import AIServiceError, ConfigurationError
from app.services.ai_service import generate_polish_result


app = FastAPI(title="Message Polisher API", version="1.0.0")


@app.get("/health")
def health_check() -> dict:
    return {"status": "ok"}


@app.post("/api/v1/polish", response_model=PolishResponse)
def polish_message(request: PolishRequest) -> dict:
    result = generate_polish_result(
        original_message=request.original_message,
        recipient_type=request.recipient_type,
        tone=request.tone,
        purpose=request.purpose,
        language=request.language,
        source_language=request.source_language,
        detail_level=request.detail_level,
    )
    return result


@app.exception_handler(ConfigurationError)
def handle_configuration_error(_, exc: ConfigurationError):
    return JSONResponse(status_code=500, content={"error_code": "CONFIGURATION_ERROR", "message": str(exc)})


@app.exception_handler(AIServiceError)
def handle_ai_service_error(_, exc: AIServiceError):
    status_code = exc.status_code or 500
    return JSONResponse(status_code=status_code, content={"error_code": "AI_SERVICE_ERROR", "message": str(exc)})
