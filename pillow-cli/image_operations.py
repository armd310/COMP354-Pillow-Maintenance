"""
Image operation classes for complex multi-image processing
"""

from pathlib import Path
from PIL import Image


class CollageCreator:
    """Handles collage creation logic"""

    def create_collage(self, images: list, cols: int, padding: int) -> Image.Image:
        rows = (len(images) + cols - 1) // cols
        max_width = max(img.width for img in images)
        max_height = max(img.height for img in images)

        resized_images = [
            img.resize((max_width, max_height), Image.Resampling.LANCZOS)
            for img in images
        ]

        collage_width = cols * max_width + (cols + 1) * padding
        collage_height = rows * max_height + (rows + 1) * padding
        collage = Image.new("RGB", (collage_width, collage_height), "white")

        for i, img in enumerate(resized_images):
            row = i // cols
            col = i % cols
            x = col * (max_width + padding) + padding
            y = row * (max_height + padding) + padding
            collage.paste(img, (x, y))

        return collage


class ImageCompositor:
    """Handles image composition logic"""

    def create_composite(
        self,
        background: Image.Image,
        overlay: Image.Image,
        position: tuple,
        opacity: float,
    ) -> Image.Image:
        background = background.convert("RGBA")
        overlay = overlay.convert("RGBA")

        if opacity < 1.0:
            overlay = overlay.copy()
            overlay.putalpha(int(255 * opacity))

        composite = Image.new("RGBA", background.size, (0, 0, 0, 0))
        composite.paste(background, (0, 0))
        composite.paste(overlay, position, overlay)

        return composite


class ContactSheetCreator:
    """Handles contact sheet creation logic"""

    def create_contact_sheet(
        self, images: list, sheet_width: int, margin: int
    ) -> Image.Image:
        cols = min(4, len(images))
        rows = (len(images) + cols - 1) // cols

        thumb_width = (sheet_width - margin * (cols + 1)) // cols
        thumb_height = thumb_width
        sheet_height = rows * thumb_height + margin * (rows + 1)

        contact_sheet = Image.new("RGB", (sheet_width, sheet_height), "white")

        for i, img in enumerate(images):
            img.thumbnail((thumb_width, thumb_height), Image.Resampling.LANCZOS)

            row = i // cols
            col = i % cols
            x = col * (thumb_width + margin) + margin
            y = row * (thumb_height + margin) + margin

            if img.width < thumb_width:
                x += (thumb_width - img.width) // 2
            if img.height < thumb_height:
                y += (thumb_height - img.height) // 2

            contact_sheet.paste(img, (x, y))

        return contact_sheet


class BatchProcessor:
    """Handles batch processing operations"""

    def __init__(self, cli_instance):
        self.cli = cli_instance

    def process_directory(
        self, input_dir: str, output_dir: str, operation: str, **kwargs
    ):
        input_path = Path(input_dir)
        output_path = Path(output_dir)

        if not input_path.exists():
            raise FileNotFoundError(f"Input directory not found: {input_dir}")

        output_path.mkdir(parents=True, exist_ok=True)

        image_files = self._find_image_files(input_path)
        if not image_files:
            print("No image files found in the input directory")
            return

        print(f"Processing {len(image_files)} images...")

        operation_map = {
            "resize": self.cli.resize_image,
            "filter": self.cli.apply_filters,
            "adjust": self.cli.adjust_image,
            "effect": self.cli.apply_artistic_effects,
            "thumbnail": self.cli.create_thumbnail,
        }

        if operation not in operation_map:
            print(f"Unknown batch operation: {operation}")
            return

        process_func = operation_map[operation]
        processed_count = 0

        for image_file in image_files:
            try:
                output_file = output_path / image_file.name
                process_func(str(image_file), str(output_file), **kwargs)
                processed_count += 1
            except Exception as e:
                print(f"Error processing {image_file.name}: {e}")

        print(f"Successfully processed {processed_count}/{len(image_files)} images")

    def _find_image_files(self, directory: Path):
        """Find all image files in directory"""
        supported_extensions = {
            ".jpg",
            ".jpeg",
            ".png",
            ".bmp",
            ".gif",
            ".tiff",
            ".webp",
        }
        image_files = []

        for file_path in directory.iterdir():
            if file_path.is_file() and file_path.suffix.lower() in supported_extensions:
                image_files.append(file_path)

        return sorted(image_files)
