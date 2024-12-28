import sys,os,subprocess
def is_color_supported():
    if not sys.stdout.isatty():
        return False

    term = os.getenv('TERM', '').lower()
    colorterm = os.getenv('COLORTERM', '').lower()

    if "color" in term or "256color" in term or "truecolor" in colorterm:
        return True
    try:
        colors = int(subprocess.check_output(['tput', 'colors']))
        if colors > 0:
            return True

    except subprocess.CalledProcessError:
        pass

    return False