import time
from fastapi import FastAPI, Request
from aiologger import Logger
from starlette.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination
from app.config import DefaultSettings, get_settings
from app.db.connection import SessionManager
from app.schemas.exception import CommonException, InternalServerError
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.routers import list_of_routes


logger = Logger.with_default_handlers(name="my-logger")

origins = ["*"]


def bind_routes(application: FastAPI, setting: DefaultSettings) -> None:
    """
    Bind all routes to application.
    """
    for route in list_of_routes:
        application.include_router(route, prefix=setting.PATH_PREFIX)


def init_database() -> None:
    """
    Creates a reusable database connection.
    Check before launching the application that the database is available to it.
    """
    SessionManager()


def get_app() -> FastAPI:
    """
    Creates application and all dependable objects.
    """
    description = """Сервис, реализующий Голосового помощника Hack-Bit"""

    application = FastAPI(
        title="medvezhiy-ugol",
        description=description,
        docs_url="/swagger",
        openapi_url="/openapi",
        version="1.0.0",
    )
    settings = get_settings()
    bind_routes(application, settings)
    add_pagination(application)
    application.state.settings = settings
    init_database()
    return application


logger = Logger.with_default_handlers(name="my-logger")
app = get_app()


@app.on_event("startup")
async def startup() -> None:
    pass


@app.on_event("shutdown")
async def shutdown() -> None:
    await logger.shutdown()


@app.middleware("http")
async def log_requst(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    formatted_process_time = "{0:.5f}".format(process_time)
    await logger.info(
        f"""***INFO*** Date time: {time.ctime()}  path={request.url.path} Method {request.method}
                Completed_in = {formatted_process_time}s"""
    )
    return response


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_request, exc):
    await logger.error(f"***ERROR*** Status code 422 Message: {str(exc)}")
    return JSONResponse(status_code=422, content={"details": exc.errors()})


@app.exception_handler(StarletteHTTPException)
async def http_exception(_request, exc):
    await logger.error(
        f"***ERROR*** Status code {exc.status_code} Message: {exc.detail}"
    )
    return JSONResponse(
        content={"detail": exc.detail},
        status_code=exc.status_code,
    )


@app.exception_handler(Exception)
async def common_exception_handler(_request: Request, exception: Exception):
    error = InternalServerError(debug=str(exception))
    await logger.error(
        f"***ERROR*** Status code {error.status_code} Message: {error.message}"
    )
    return JSONResponse(status_code=error.status_code, content=error.to_json())


@app.exception_handler(CommonException)
async def unicorn_api_exception_handler(_request: Request, exc: CommonException):
    await logger.error(f"***ERROR*** Status code {exc.code} Message: {exc.error}")
    return JSONResponse(
        status_code=exc.code,
        content={"detail": exc.error},
    )


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
