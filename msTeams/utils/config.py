"""
This is a configuration module, that provides methods for creating/reading
private $HOME/.[]rc file to store config(account) settings for Selemander
apps. The logic is partly borrowed from zulip/zulip-terminal.
"""
import os
import stat
import configparser

from typing import Any, Dict
from styles.pretty_print import in_color

SELEMRC_DEST = "~/.selemrc"


def _is_initialized() -> bool:
    """
    Checks if the user is running Selemander for the first time
    """
    selemrc_path = os.path.expanduser(SELEMRC_DEST)
    return os.path.exists(selemrc_path)


def _write_selemrc(login_id: str, passwd: str) -> str:
    """
    Writes a selemrc file, returning a non-empty error string on failure
    Only creates new private files; errors if file already exists
    """
    try:
        to_path = os.path.expanduser(SELEMRC_DEST)
        with open(os.open(to_path,
                          os.O_CREAT | os.O_WRONLY | os.O_EXCL,
                          0o600),
                  'w') as f:
            f.write(
                f"[msteam]\nemail={login_id}\npasswd={passwd}"
            )
        return (f"selemrc successfully created at {SELEMRC_DEST}\n"
                f"File permission set to 600.")
    except FileExistsError as ex:
        return f"selemrc already exists at {SELEMRC_DEST}"
    except OSError as ex:
        return (f"{ex.__class__.__name__}: "
                f"selemrc could not be created at {SELEMRC_DEST}")


def _parse_selemrc() -> Dict[str, Any]:
    """
    Parses selemrc if present else print appropriate error message
    and exits.
    """
    selemrc_path = os.path.expanduser(SELEMRC_DEST)
    mode = os.stat(selemrc_path).st_mode
    is_readable_by_go = mode & (stat.S_IRWXG | stat.S_IRWXO)

    if is_readable_by_go:
        print(in_color(
            'red',
            "ERROR: Please ensure your selemrc is NOT publicly accessible:\n"
            "  {0}\n"
            "(it currently has permissions '{1}')\n"
            "This can often be achieved with a command such as:\n"
            "  chmod og-rwx {0}\n".format(selemrc_path, stat.filemode(mode))
        ))
        sys.exit(1)
    
    parsed_selemrc = configparser.ConfigParser()

    try:
        res = parsed_selemrc.read(selemrc_path)
        if len(res) == 0:
            exit_with_error(f"Could not access selemrc file at {selemrc_path}")
    except configparser.MissingSectionHeaderError:
        exit_with_error(f"Failed to parse selemrc file at {selemrc_path}")

    settings = {}
    if 'msteam' in parsed_selemrc:
        config = parsed_selemrc['msteam']
        for conf in config:
            settings[conf] = config[conf]
    
    return settings
