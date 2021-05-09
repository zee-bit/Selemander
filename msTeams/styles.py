def in_color(color: str, text: str) -> str:
    color_for_str = {
        'red': '1',
        'green': '2',
        'yellow': '3',
        'blue': '4',
        'purple': '5',
        'cyan': '6',
    }
    # We can use 3 instead of 9 if high-contrast is eg. less compatible?
    return f"\033[9{color_for_str[color]}m{text}\033[0m"


def styled_input(label: str, color: str='blue') -> str:
    return input(in_color(color, label))