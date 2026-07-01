"""OpsCenter configuration — pydantic-settings, reads OPS_ prefixed env vars."""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_config = {"env_prefix": "OPS_", "env_file": ".env", "env_file_encoding": "utf-8", "extra": "ignore"}

    secret_key: str = "dev-secret-change-in-production"
    encryption_key: str = ""  # Fernet key for encrypting secret config values
    db_path: str = "data/config.db"
    config_output_dir: str = "data/configs"
    orchestrator_feature_gates_path: str = "data/configs/orchestrator/feature_gates.yaml"
    # JWT: share secret with orchestrator
    jwt_secret: str = ""  # Empty = fall back to secret_key
    jwt_algorithm: str = "HS256"

    def get_jwt_secret(self) -> str:
        """Get JWT secret, falling back to secret_key if jwt_secret not set."""
        return self.jwt_secret or self.secret_key
    cors_origins: str = "*"


settings = Settings()
