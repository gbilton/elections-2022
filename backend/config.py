from dynaconf import Dynaconf


settings = Dynaconf(
    settings_files=[".settings.toml"],
    env_switcher="APP_ENV",
    load_dotenv=True,
    environments=True,
)
