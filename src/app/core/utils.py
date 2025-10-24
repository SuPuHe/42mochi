# app/core/utils.py
def adjust_brightness(hex_color: str, steps: int) -> str:
    hex_color = hex_color.lstrip("#")
    r = max(0, min(255, int(hex_color[0:2], 16) + steps))
    g = max(0, min(255, int(hex_color[2:4], 16) + steps))
    b = max(0, min(255, int(hex_color[4:6], 16) + steps))
    return f"#{r:02x}{g:02x}{b:02x}"
