"""
Image processor classes - each handling a specific type of operation
"""
from PIL import Image, ImageFilter, ImageEnhance, ImageDraw, ImageFont, ImageOps
from abc import ABC, abstractmethod


class BaseImageProcessor(ABC):
    """Base class for all image processors"""

    @abstractmethod
    def process(self, image: Image.Image, **kwargs) -> Image.Image:
        """Process the image and return result"""
        pass

    def log_operation(self, operation_name: str, **details):
        """Log the operation details"""
        print(f"{operation_name}: {details}")


class ResizeProcessor(BaseImageProcessor):
    """Handles image resizing operations"""

    def process(self, image: Image.Image, width=None, height=None, maintain_aspect=True) -> Image.Image:
        original_width, original_height = image.size

        if width and height:
            if maintain_aspect:
                aspect_ratio = original_width / original_height
                if width / height > aspect_ratio:
                    new_width = int(height * aspect_ratio)
                    new_height = height
                else:
                    new_width = width
                    new_height = int(width / aspect_ratio)
            else:
                new_width, new_height = width, height
            new_size = (new_width, new_height)
        elif width:
            aspect_ratio = original_height / original_width
            new_size = (width, int(width * aspect_ratio))
        elif height:
            aspect_ratio = original_width / original_height
            new_size = (int(height * aspect_ratio), height)
        else:
            raise ValueError("Must specify at least width or height")

        resized_image = image.resize(new_size, Image.Resampling.LANCZOS)
        self.log_operation("Resize",
                           original_size=f"{original_width}x{original_height}",
                           new_size=f"{new_size[0]}x{new_size[1]}")
        return resized_image


class FilterProcessor(BaseImageProcessor):
    """Handles image filtering operations"""

    def __init__(self):
        self.filters = {
            'blur': ImageFilter.BLUR,
            'contour': ImageFilter.CONTOUR,
            'detail': ImageFilter.DETAIL,
            'edge_enhance': ImageFilter.EDGE_ENHANCE,
            'edge_enhance_more': ImageFilter.EDGE_ENHANCE_MORE,
            'emboss': ImageFilter.EMBOSS,
            'find_edges': ImageFilter.FIND_EDGES,
            'sharpen': ImageFilter.SHARPEN,
            'smooth': ImageFilter.SMOOTH,
            'smooth_more': ImageFilter.SMOOTH_MORE,
            'gaussian_blur': ImageFilter.GaussianBlur(radius=2),
            'unsharp_mask': ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3)
        }

    def process(self, image: Image.Image, filter_type: str) -> Image.Image:
        if filter_type not in self.filters:
            raise ValueError(f"Unknown filter: {filter_type}. Available: {', '.join(self.filters.keys())}")

        filtered_image = image.filter(self.filters[filter_type])
        self.log_operation("Filter", filter_type=filter_type)
        return filtered_image


class AdjustmentProcessor(BaseImageProcessor):
    """Handles image adjustment operations"""

    def process(self, image: Image.Image, brightness=1.0, contrast=1.0, saturation=1.0, sharpness=1.0) -> Image.Image:
        result_image = image

        if brightness != 1.0:
            enhancer = ImageEnhance.Brightness(result_image)
            result_image = enhancer.enhance(brightness)

        if contrast != 1.0:
            enhancer = ImageEnhance.Contrast(result_image)
            result_image = enhancer.enhance(contrast)

        if saturation != 1.0:
            enhancer = ImageEnhance.Color(result_image)
            result_image = enhancer.enhance(saturation)

        if sharpness != 1.0:
            enhancer = ImageEnhance.Sharpness(result_image)
            result_image = enhancer.enhance(sharpness)

        self.log_operation("Adjustment",
                           brightness=brightness, contrast=contrast,
                           saturation=saturation, sharpness=sharpness)
        return result_image


class CropProcessor(BaseImageProcessor):
    """Handles image cropping operations"""

    def process(self, image: Image.Image, x: int, y: int, width: int, height: int) -> Image.Image:
        img_width, img_height = image.size
        if x + width > img_width or y + height > img_height:
            raise ValueError(f"Crop dimensions exceed image size ({img_width}x{img_height})")

        cropped_image = image.crop((x, y, x + width, y + height))
        self.log_operation("Crop",
                           position=f"({x}, {y})",
                           dimensions=f"{width}x{height}")
        return cropped_image


class RotateProcessor(BaseImageProcessor):
    """Handles image rotation operations"""

    def process(self, image: Image.Image, angle: float, expand: bool = True) -> Image.Image:
        rotated_image = image.rotate(angle, expand=expand, fillcolor='white')
        self.log_operation("Rotate", angle=angle, expand=expand)
        return rotated_image


class FlipProcessor(BaseImageProcessor):
    """Handles image flipping operations"""

    def process(self, image: Image.Image, direction: str = 'horizontal') -> Image.Image:
        if direction == 'horizontal':
            flipped_image = image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        elif direction == 'vertical':
            flipped_image = image.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
        else:
            raise ValueError("Direction must be 'horizontal' or 'vertical'")

        self.log_operation("Flip", direction=direction)
        return flipped_image


class FormatProcessor(BaseImageProcessor):
    """Handles image format conversion"""

    def process(self, image: Image.Image, format_type: str = 'PNG') -> Image.Image:
        if format_type.upper() == 'JPEG' and image.mode in ('RGBA', 'LA'):
            background = Image.new('RGB', image.size, (255, 255, 255))
            background.paste(image, mask=image.split()[-1] if image.mode == 'RGBA' else None)
            converted_image = background
        else:
            converted_image = image

        self.log_operation("Format Conversion", format=format_type.upper())
        return converted_image


class ThumbnailProcessor(BaseImageProcessor):
    """Handles thumbnail creation"""

    def process(self, image: Image.Image, size: tuple = (128, 128)) -> Image.Image:
        thumb_image = image.copy()
        thumb_image.thumbnail(size, Image.Resampling.LANCZOS)
        self.log_operation("Thumbnail", size=size)
        return thumb_image


class WatermarkProcessor(BaseImageProcessor):
    """Handles watermark addition"""

    def __init__(self):
        self.positions = {
            'top-left': self._calculate_top_left,
            'top-right': self._calculate_top_right,
            'bottom-left': self._calculate_bottom_left,
            'bottom-right': self._calculate_bottom_right,
            'center': self._calculate_center
        }

    def process(self, image: Image.Image, watermark_text: str,
                position: str = 'bottom-right', opacity: int = 128) -> Image.Image:
        overlay = Image.new('RGBA', image.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(overlay)

        font = self._get_font()
        bbox = draw.textbbox((0, 0), watermark_text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        if position not in self.positions:
            raise ValueError(f"Invalid position. Available: {', '.join(self.positions.keys())}")

        x, y = self.positions[position](image.size, text_width, text_height)

        # Draw text with semi-transparent background
        draw.rectangle([x - 5, y - 5, x + text_width + 5, y + text_height + 5], fill=(0, 0, 0, opacity // 2))
        draw.text((x, y), watermark_text, font=font, fill=(255, 255, 255, opacity))

        watermarked_image = Image.alpha_composite(image.convert('RGBA'), overlay)
        self.log_operation("Watermark", text=watermark_text, position=position, opacity=opacity)
        return watermarked_image

    def _get_font(self):
        """Get the best available font"""
        try:
            return ImageFont.truetype("arial.ttf", 36)
        except OSError:
            return ImageFont.load_default()

    def _calculate_top_left(self, img_size, text_width, text_height):
        return (10, 10)

    def _calculate_top_right(self, img_size, text_width, text_height):
        return (img_size[0] - text_width - 10, 10)

    def _calculate_bottom_left(self, img_size, text_width, text_height):
        return (10, img_size[1] - text_height - 10)

    def _calculate_bottom_right(self, img_size, text_width, text_height):
        return (img_size[0] - text_width - 10, img_size[1] - text_height - 10)

    def _calculate_center(self, img_size, text_width, text_height):
        return ((img_size[0] - text_width) // 2, (img_size[1] - text_height) // 2)


class EffectProcessor(BaseImageProcessor):
    """Handles artistic effects"""

    def __init__(self):
        self.effects = {
            'sepia': self._apply_sepia,
            'grayscale': self._apply_grayscale,
            'invert': self._apply_invert,
            'posterize': self._apply_posterize,
            'solarize': self._apply_solarize
        }

    def process(self, image: Image.Image, effect: str = 'sepia') -> Image.Image:
        if effect not in self.effects:
            raise ValueError(f"Unknown effect: {effect}. Available: {', '.join(self.effects.keys())}")

        processed_image = self.effects[effect](image.convert('RGB'))
        self.log_operation("Effect", effect=effect)
        return processed_image

    def _apply_sepia(self, image: Image.Image) -> Image.Image:
        pixels = image.load()
        for y in range(image.height):
            for x in range(image.width):
                r, g, b = pixels[x, y]
                tr = int(0.393 * r + 0.769 * g + 0.189 * b)
                tg = int(0.349 * r + 0.686 * g + 0.168 * b)
                tb = int(0.272 * r + 0.534 * g + 0.131 * b)
                pixels[x, y] = (min(255, tr), min(255, tg), min(255, tb))
        return image

    def _apply_grayscale(self, image: Image.Image) -> Image.Image:
        return ImageOps.grayscale(image)

    def _apply_invert(self, image: Image.Image) -> Image.Image:
        return ImageOps.invert(image)

    def _apply_posterize(self, image: Image.Image) -> Image.Image:
        return ImageOps.posterize(image, 4)

    def _apply_solarize(self, image: Image.Image) -> Image.Image:
        return ImageOps.solarize(image, threshold=128)


class BorderProcessor(BaseImageProcessor):
    """Handles border addition"""

    def __init__(self):
        self.color_map = {
            'black': (0, 0, 0),
            'white': (255, 255, 255),
            'red': (255, 0, 0),
            'green': (0, 255, 0),
            'blue': (0, 0, 255)
        }

    def process(self, image: Image.Image, border_width: int = 10, border_color='black') -> Image.Image:
        parsed_color = self._parse_color(border_color)
        bordered_image = ImageOps.expand(image, border=border_width, fill=parsed_color)
        self.log_operation("Border", width=border_width, color=parsed_color)
        return bordered_image

    def _parse_color(self, color):
        """Parse color from various formats"""
        if isinstance(color, str):
            if color.startswith('#'):
                return tuple(int(color[i:i + 2], 16) for i in (1, 3, 5))
            elif color in self.color_map:
                return self.color_map[color]
        return color


class VignetteProcessor(BaseImageProcessor):
    """Handles vignette effect"""

    def process(self, image: Image.Image, strength: float = 0.5) -> Image.Image:
        image = image.convert('RGBA')
        width, height = image.size

        mask = Image.new('L', (width, height), 0)
        mask_draw = ImageDraw.Draw(mask)

        center_x, center_y = width // 2, height // 2
        max_radius = min(center_x, center_y)

        steps = 100
        for i in range(steps):
            radius = max_radius * (i / steps)
            alpha = int(255 * (1 - strength * (i / steps)))
            mask_draw.ellipse([center_x - radius, center_y - radius,
                               center_x + radius, center_y + radius], fill=alpha)

        vignette_overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        vignette_overlay.putalpha(mask)

        result = Image.alpha_composite(image, vignette_overlay)
        self.log_operation("Vignette", strength=strength)
        return result
