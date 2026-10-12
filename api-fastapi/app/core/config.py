"""Configuración de la aplicación leída desde variables de entorno (.env)."""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Configuracion(BaseSettings):
    DATABASE_URL: str = "postgresql+psycopg2://prestamos:prestamos@localhost:5432/prestamos"
    SECRET_KEY: str = "cambie-esta-clave-secreta"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    CORS_ORIGINS: str = "*"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def url_bd(self) -> str:
        # Render/Railway entregan "postgres://" o "postgresql://"; SQLAlchemy necesita el driver
        url = self.DATABASE_URL
        if url.startswith("postgres://"):
            url = url.replace("postgres://", "postgresql+psycopg2://", 1)
        elif url.startswith("postgresql://"):
            url = url.replace("postgresql://", "postgresql+psycopg2://", 1)
        return url


config = Configuracion()
