def resize_for_aspect_ratio(width: int, height: int, aspect_ratio: float) -> tuple[int, int]:
    if width / height < aspect_ratio:
        height = int(width / aspect_ratio)
    elif width / height > aspect_ratio:
        width = int(height * aspect_ratio)
    return width, height