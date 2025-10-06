def get_style(enable_colorful_output: bool = True) -> type:
    """
    Returns a style class for logging or terminal output, optionally using colors.

    If `enable_colorful_output` is True, the returned class uses `colorama` colors.
    Otherwise, it uses simple text symbols.

    Attributes:
        success: Style for success messages (green or '[√]')
        info: Style for informational messages (blue or '[I]')
        warning: Style for warnings (yellow or '[!]')
        error: Style for errors (red or '[x]')

    Args:
        enable_colorful_output (bool): Whether to enable colored output. Default is True.

    Returns:
        Style class: A class with the above attributes that can be accessed like
                     `Style.success`, `Style.info`, etc.
    """
    
    if enable_colorful_output:
        import colorama
        colorama.init()  # enable color output support

        class Style:
            success = colorama.Fore.GREEN + '<>' + colorama.Fore.RESET
            infomation = colorama.Fore.BLUE + '<>' + colorama.Fore.RESET
            warning = colorama.Fore.YELLOW + '<>' + colorama.Fore.RESET
            error = colorama.Fore.RED + '<>' + colorama.Fore.RESET

    else:
        class Style:
            success = '[√]'
            infomation = '[I]'
            warning = '[!]'
            error = '[x]'

    return Style
