from pydantic import BaseSettings


class Config(BaseSettings):
    source_json_path: str = "data/disco_elysium.json"
    dialogue_metadata_path: str = "data/dialogue_metadata.toml"
    lua_script_path: str = "data/script.lua"

    sentry_dsn: str | None = None


config = Config()
