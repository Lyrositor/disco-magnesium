# Disco Magnesium

> **+2 Encyclopedia:** A great democracy of creatures<br />
> **+2 Volition:** Good morning, Elysium

**Disco Magnesium** is a Python web app for browsing Disco Elysium conversations in a similar fashion to playing the game.

*Note:* the Disco Elysium conversation data is not included in this source code.

**License:** [Creative Commons CC0 1.0 Universal](https://github.com/Lyrositor/disco-magnesium/blob/main/LICENSE.md)

## Setup

### Requirements

Disco Magnesium requires **[Python 3.11](https://www.python.org/)** or higher.

You will also need **[Poetry](https://python-poetry.org/)** to install it. Refer to its installation documentation for instructions on how to set it up for your system: https://python-poetry.org/docs/

Finally, you will need to extract the conversation data from Disco Elysium. Instructions on how to do so are beyond the scope of this page.

### Installation

Once you have installed the requirements and checked out the repository, you will need to install all the Python dependencies:

```shell
poetry shell
poetry install
```

You will also need to add the extracted Disco Elysium dialogue data to `data/disco_elysium.json`.

### Running

You can run a development version of the server with the following command:

```shell
python disco_magnesium
```

For a production deployment, you'll probably want to use the gunicorn deployment by running:

```shell
gunicorn
```

You can use the provided `disco-magnesium.service` systemd file to register Disco Magnesium as a service that can run in the background and start automatically with your system.

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
