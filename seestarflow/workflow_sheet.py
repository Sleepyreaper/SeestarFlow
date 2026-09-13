from __future__ import annotations

import json
import math
import textwrap
from pathlib import Path


def _font(ImageFont, size: int, bold: bool = False):
    names = (
        ("C:/Windows/Fonts/arialbd.ttf", "C:/Windows/Fonts/arial.ttf")
        if bold else
        ("C:/Windows/Fonts/arial.ttf", "C:/Windows/Fonts/arialbd.ttf")
    )
    for name in names + ("DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf",):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def build_workflow_sheet(spec_path: Path, output_path: Path | None = None) -> Path:
    """Render a branded processing-step sheet from exported stage images."""
    try:
        from PIL import Image, ImageDraw, ImageFont, ImageOps
    except ImportError as exc:
        raise RuntimeError("Workflow sheets require Pillow: python -m pip install '.[media]'") from exc

    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    stages = spec.get("stages", [])
    if not 1 <= len(stages) <= 30:
        raise ValueError("workflow sheet requires between 1 and 30 stages")

    base = spec_path.parent
    resolved = []
    for index, stage in enumerate(stages, start=1):
        if not stage.get("label") or not stage.get("image"):
            raise ValueError(f"stage {index} requires label and image")
        image_path = Path(stage["image"])
        if not image_path.is_absolute():
            image_path = base / image_path
        if not image_path.exists():
            raise FileNotFoundError(image_path)
        resolved.append((stage, image_path))

    columns = int(spec.get("columns", 4))
    if columns not in (3, 4, 5):
        raise ValueError("columns must be 3, 4, or 5")
    width = int(spec.get("width", 1800))
    margin = 54
    gap = 28
    title_h = 174
    footer_h = 72
    card_w = (width - margin * 2 - gap * (columns - 1)) // columns
    image_h = round(card_w * 0.60)
    text_h = 100
    card_h = image_h + text_h
    rows = math.ceil(len(stages) / columns)
    height = title_h + rows * card_h + (rows - 1) * gap + footer_h

    background = (7, 10, 16)
    surface = (17, 23, 33)
    foreground = (242, 246, 252)
    muted = (163, 174, 190)
    accent = tuple(spec.get("accent_rgb", [73, 191, 225]))
    canvas = Image.new("RGB", (width, height), background)
    draw = ImageDraw.Draw(canvas)
    title_font = _font(ImageFont, 50, bold=True)
    subtitle_font = _font(ImageFont, 24)
    step_font = _font(ImageFont, 24, bold=True)
    label_font = _font(ImageFont, 23, bold=True)
    detail_font = _font(ImageFont, 19)
    footer_font = _font(ImageFont, 18)

    title = spec.get("title", "Astrophotography workflow")
    subtitle = spec.get("subtitle", "Authentic photons • reproducible processing • layered finish")
    draw.text((width // 2, 38), title, font=title_font, fill=foreground, anchor="ma")
    draw.text((width // 2, 106), subtitle, font=subtitle_font, fill=accent, anchor="ma")

    for position, (stage, image_path) in enumerate(resolved):
        row, column = divmod(position, columns)
        x = margin + column * (card_w + gap)
        y = title_h + row * (card_h + gap)
        draw.rounded_rectangle((x, y, x + card_w, y + card_h), radius=20, fill=surface)

        with Image.open(image_path) as source:
            source = ImageOps.exif_transpose(source).convert("RGB")
            thumb = ImageOps.fit(source, (card_w, image_h), method=Image.Resampling.LANCZOS)
            mask = Image.new("L", thumb.size, 0)
            ImageDraw.Draw(mask).rounded_rectangle((0, 0, card_w, image_h + 20), radius=20, fill=255)
            canvas.paste(thumb, (x, y), mask)

        step_number = stage.get("step", position + 1)
        draw.text((x + 18, y + image_h + 14), f"{step_number}", font=step_font, fill=accent)
        draw.text((x + 62, y + image_h + 15), stage["label"], font=label_font, fill=foreground)
        detail = str(stage.get("detail", ""))
        if detail:
            wrapped = textwrap.fill(detail, width=max(24, card_w // 18), max_lines=2, placeholder="…")
            draw.multiline_text((x + 18, y + image_h + 51), wrapped, font=detail_font, fill=muted, spacing=4)

    footer = spec.get("footer", "SeestarFlow • no generated astronomical content")
    draw.text((width // 2, height - 36), footer, font=footer_font, fill=muted, anchor="mm")
    destination = output_path or (base / spec.get("output", "workflow-sheet.png"))
    destination.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(destination, format="PNG", optimize=True)
    return destination
