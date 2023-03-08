import logging
import os.path
import pickle

import sentry_sdk
import toml
from fastapi import FastAPI, Depends
from starlette.staticfiles import StaticFiles

from disco_magnesium.config import config
from disco_magnesium.importer.source import convert_source_dialogue, import_dialogue_from_raw_json_file
from disco_magnesium.model.dialogue import Dialogue

log = logging.getLogger(__name__)

dialogue: Dialogue | None = None
conversations_metadata: None = None

get_dialogue = Depends(lambda: dialogue)
get_conversations_metadata = Depends(lambda: conversations_metadata)


def setup_app() -> FastAPI:
    from disco_magnesium.api.routes import router

    setup_sentry()

    app = FastAPI()
    app.include_router(router, prefix="/api")
    app.mount("/", StaticFiles(directory="static", html=True), name="static")
    app.add_event_handler("startup", on_startup)

    return app


def setup_sentry():
    if config.sentry_dsn:
        sentry_sdk.init(dsn=config.sentry_dsn)


def on_startup() -> None:
    global dialogue
    global conversations_metadata

    log.info("Loading dialogue metadata")
    dialogue_metadata_path = os.path.abspath(config.dialogue_metadata_path)
    with open(dialogue_metadata_path) as f:
        toml_data = toml.load(f)
        additional_variables = toml_data["additional_variables"]
        conversations_metadata = {conversation["id"]: conversation for conversation in toml_data["conversation"]}

    log.info("Loading dialogue")
    cache_path = os.path.abspath(config.source_json_path + ".cache")
    if os.path.exists(cache_path):
        with open(cache_path, "rb") as f:
            source_dialogue = pickle.load(f)
    else:
        source_dialogue = import_dialogue_from_raw_json_file(os.path.abspath(config.source_json_path))
        with open(cache_path, "wb") as f:
            pickle.dump(source_dialogue, f)
    dialogue = convert_source_dialogue(source_dialogue, additional_variables, conversations_metadata)

    log.info("Start-up complete")
