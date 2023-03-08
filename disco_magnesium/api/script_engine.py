import logging
from typing import Any

from lupa import LuaRuntime, LuaError

from disco_magnesium.api.models.state import State
from disco_magnesium.config import config
from disco_magnesium.model.dialogue import Dialogue

log = logging.getLogger(__name__)


class ScriptEngine:
    dialogue: Dialogue
    state: State
    lua: LuaRuntime

    def __init__(self, dialogue: Dialogue, state: State):
        self.dialogue = dialogue
        self.state = state
        self.lua = LuaRuntime()
        self.lua.execute(lua_script)

    def eval_condition(self, condition: str) -> bool:
        self._setup_lua()
        try:
            return bool(self.lua.eval(condition))
        except LuaError as e:
            log.exception("Failed to evaluate condition", exc_info=e)
            return False

    def run_user_script(self, user_script: str) -> Any:
        self._setup_lua()
        try:
            return self.lua.execute(user_script)
        except LuaError as e:
            log.exception("Failed to run user script", exc_info=e)
            return None

    def _setup_lua(self) -> None:
        lua_globals = self.lua.globals()
        lua_globals.Logger = log
        lua_globals.ItemGroups = {
            name: item.group.value if item.group else None for name, item in self.dialogue.items.items()
        }
        lua_globals.ItemTypes = {
            name: item.type.value for name, item in self.dialogue.items.items()
        }
        lua_globals.State = self.state
        lua_globals.Variable = self.lua.table_from(
            {
                **{name: variable.initial_value for name, variable in self.dialogue.variables.items()},
                **self.state.variables,
            }
        )


def load_lua_script() -> str:
    with open(config.lua_script_path) as f:
        return f.read()


lua_script = load_lua_script()
