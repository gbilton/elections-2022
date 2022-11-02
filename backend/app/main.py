from fastapi import FastAPI


def create_app() -> FastAPI:
    """Main application factory function.

    Returns:
        FastAPI: Returns the application instance.
    """

    from backend.app import routes
    from .extensions import middleware

    app: FastAPI = FastAPI()

    middleware.init_app(app)
    routes.init_app(app)

    @app.get("/")
    async def check_api_health():
        return {"Health": "OK!"}

    return app
