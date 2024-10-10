def get_color_tag(value):
    if value is None:
        return ()
    if value < 33:
        return ("low",)
    elif value < 67:
        return ("medium",)
    else:
        return ("high",)