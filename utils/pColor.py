"""
    Plusto Color Utils
"""

class pColor:
    # ANSI Escape Sequences for Colors
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    UNDERLINE = '\033[4m'
    REVERSED = '\033[7m'
    HIDDEN = '\033[8m'

    # Basic colors
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'

    # Bright colors
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'

    # Background colors
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'

    BG_BRIGHT_BLACK = '\033[100m'
    BG_BRIGHT_RED = '\033[101m'
    BG_BRIGHT_GREEN = '\033[102m'
    BG_BRIGHT_YELLOW = '\033[103m'
    BG_BRIGHT_BLUE = '\033[104m'
    BG_BRIGHT_MAGENTA = '\033[105m'
    BG_BRIGHT_CYAN = '\033[106m'
    BG_BRIGHT_WHITE = '\033[107m'

    @staticmethod
    def apply_color(text, color_code):
        """Apply color to the text."""
        return f"{color_code}{text}{pColor.RESET}"

    @staticmethod
    def colored(text, color):
        """Color the text with a given color."""
        color_map = {
            'black': pColor.BLACK,
            'red': pColor.RED,
            'green': pColor.GREEN,
            'yellow': pColor.YELLOW,
            'blue': pColor.BLUE,
            'magenta': pColor.MAGENTA,
            'cyan': pColor.CYAN,
            'white': pColor.WHITE,
            'bright_black': pColor.BRIGHT_BLACK,
            'bright_red': pColor.BRIGHT_RED,
            'bright_green': pColor.BRIGHT_GREEN,
            'bright_yellow': pColor.BRIGHT_YELLOW,
            'bright_blue': pColor.BRIGHT_BLUE,
            'bright_magenta': pColor.BRIGHT_MAGENTA,
            'bright_cyan': pColor.BRIGHT_CYAN,
            'bright_white': pColor.BRIGHT_WHITE,
            'bg_black': pColor.BG_BLACK,
            'bg_red': pColor.BG_RED,
            'bg_green': pColor.BG_GREEN,
            'bg_yellow': pColor.BG_YELLOW,
            'bg_blue': pColor.BG_BLUE,
            'bg_magenta': pColor.BG_MAGENTA,
            'bg_cyan': pColor.BG_CYAN,
            'bg_white': pColor.BG_WHITE,
            'bg_bright_black': pColor.BG_BRIGHT_BLACK,
            'bg_bright_red': pColor.BG_BRIGHT_RED,
            'bg_bright_green': pColor.BG_BRIGHT_GREEN,
            'bg_bright_yellow': pColor.BG_BRIGHT_YELLOW,
            'bg_bright_blue': pColor.BG_BRIGHT_BLUE,
            'bg_bright_magenta': pColor.BG_BRIGHT_MAGENTA,
            'bg_bright_cyan': pColor.BG_BRIGHT_CYAN,
            'bg_bright_white': pColor.BG_BRIGHT_WHITE
        }

        if color.lower() in color_map:
            return pColor.apply_color(text, color_map[color.lower()])
        else:
            raise ValueError(f"Color '{color}' is not a valid color.")

