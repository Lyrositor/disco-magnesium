# Disco Magnesium

<div style="display: flex; flex-direction: row; border-left: solid 5px; margin: 1em;">
<div style="padding: 0 1em; font-weight: bold;">
DISCO ELYSIUM CONVERSATION REPLAYER
</div>
<div style="padding: 0 1em;">
+2 <span style="color: #69c0c7;">Encylopedia</span>: A great democracy of creatures<br />
+2 <span style="color: #8067c2;">Volition</span>: Good morning, Elysium
</div> 
</div>

**Disco Magnesium** is a Python web app for browsing Disco Elysium conversations in a similar fashion to playing the game.

*Note:* the Disco Elysium conversation data is not included in this source code.

**License:** Creative Commons CC0 1.0 Universal (except for the )

## Known Issues

The following issues are known:

- The branching algorithm is too simplistic. It doesn't handle cases where player outgoing nodes are mixed in with non-player outgoing nodes, nor does it handle recursively constructed menus.
- The various day times' actual values have not yet been checked.
- The copotype/political affiliation-checking logic has not been checked.
- There is no mechanism for advancing thoughts in the thought cabinet - they are always considered to be completed on acquisition.
- The `IsHourBetween` Lua function needs to be checked to see how it handles boundaries.
- Advancing time automatically is not supported. This will not be fixed, in order to keep it convenient to browse through conversations.
- Variables relating to substance use aren't properly understood yet.
- The definition of "weird clothing" is unknown.
- Code that is explicitly marked as needing to fire once doesn't support checking if it has fired before.