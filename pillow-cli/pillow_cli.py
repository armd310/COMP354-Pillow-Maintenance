#!/usr/bin/env python3
import argparse
import os
import sys
from pathlib import Path
import json
from PIL import Image, ImageFilter, ImageEnhance, ImageDraw, ImageFont, ImageOps
from PIL.ExifTags import TAGS
from color_analysis import analyze_histogram, extract_color_palette, split_channels
from image_processors import (
    ResizeProcessor,
    FilterProcessor,
    AdjustmentProcessor,
    CropProcessor,
    RotateProcessor,
    FlipProcessor,
    FormatProcessor,
    ThumbnailProcessor,
    WatermarkProcessor,
    EffectProcessor,
    BorderProcessor,
    VignetteProcessor,
)
from image_operations import (
    CollageCreator,
    ImageCompositor,
    ContactSheetCreator,
    BatchProcessor,
)

try:
    from PIL import ImageTk
    import tkinter as tk
    from tkinter import ttk

    GUI_AVAILABLE = True
except ImportError:
    GUI_AVAILABLE = False


class PillowCLI:
    """Main CLI class for image processing operations"""

    def __init__(self):
        self.supported_formats = {
            ".jpg",
            ".jpeg",
            ".png",
            ".bmp",
            ".gif",
            ".tiff",
            ".webp",
        }
        self._initialize_processors()

    def create_collage(self, input_paths, output_path, cols=2, padding=10):
        """Create a collage from multiple images"""
        if not input_paths:
            raise ValueError("No input images provided")

        images = [self.load_image(path) for path in input_paths]
        collage_creator = CollageCreator()
        collage = collage_creator.create_collage(images, cols, padding)
        self.save_image(collage, output_path)
        print(
            f"Created collage with {len(images)} images ({(len(images) + cols - 1) // cols}x{cols} grid)"
        )

    def create_composite(
        self,
        background_path: str,
        overlay_path: str,
        output_path: str,
        position=(0, 0),
        opacity=1.0,
    ):
        """Composite two images together"""
        compositor = ImageCompositor()
        background = self.load_image(background_path)
        overlay = self.load_image(overlay_path)
        composite = compositor.create_composite(background, overlay, position, opacity)
        self.save_image(composite, output_path)
        print(f"Created composite image at position {position} with opacity {opacity}")

    def create_contact_sheet(
        self, input_paths: list, output_path: str, sheet_width=1200, margin=10
    ):
        """Create a contact sheet from multiple images"""
        if not input_paths:
            raise ValueError("No input images provided")

        images = [self.load_image(path) for path in input_paths]
        contact_sheet_creator = ContactSheetCreator()
        contact_sheet = contact_sheet_creator.create_contact_sheet(
            images, sheet_width, margin
        )
        self.save_image(contact_sheet, output_path)
        print(f"Created contact sheet with {len(images)} images")

    def batch_process(self, input_dir: str, output_dir: str, operation: str, **kwargs):
        """Process multiple images in a directory"""
        batch_processor = BatchProcessor(self)
        return batch_processor.process_directory(
            input_dir, output_dir, operation, **kwargs
        )

    def _initialize_processors(self):
        """Initialize all image processors"""
        self.processors = {
            "resize": ResizeProcessor(),
            "filter": FilterProcessor(),
            "adjust": AdjustmentProcessor(),
            "crop": CropProcessor(),
            "rotate": RotateProcessor(),
            "flip": FlipProcessor(),
            "format": FormatProcessor(),
            "thumbnail": ThumbnailProcessor(),
            "watermark": WatermarkProcessor(),
            "effect": EffectProcessor(),
            "border": BorderProcessor(),
            "vignette": VignetteProcessor(),
        }

    def validate_image_path(self, path: str) -> bool:
        """Validate if the path is a valid image file"""
        if not os.path.exists(path):
            raise FileNotFoundError(f"Image file not found: {path}")

        if not Path(path).suffix.lower() in self.supported_formats:
            raise ValueError(
                f"Unsupported image format. Supported: {', '.join(self.supported_formats)}"
            )

        return True

    def load_image(self, path: str) -> Image.Image:
        """Load an image from file path"""
        self.validate_image_path(path)
        return Image.open(path)

    def save_image(self, image: Image.Image, output_path: str, quality=95):
        """Save image to file with specified quality"""
        # Ensure output directory exists
        os.makedirs(
            os.path.dirname(output_path) if os.path.dirname(output_path) else ".",
            exist_ok=True,
        )

        # Convert RGBA to RGB if saving as JPEG
        if (
            Path(output_path).suffix.lower() in [".jpg", ".jpeg"]
            and image.mode == "RGBA"
        ):
            background = Image.new("RGB", image.size, (255, 255, 255))
            background.paste(image, mask=image.split()[-1])
            image = background

        image.save(output_path, quality=quality, optimize=True)
        print(f"Image saved to: {output_path}")

    def process_image(
        self, input_path: str, output_path: str, processor_name: str, **kwargs
    ) -> Image.Image:
        """Generic method to process image using specified processor"""
        if processor_name not in self.processors:
            raise ValueError(f"Unsupported processor: {processor_name}")
        image = self.load_image(input_path)
        processor = self.processors[processor_name]
        result = processor.process(image, **kwargs)
        self.save_image(result, output_path)
        return result

    # Keep same API as before
    def resize_image(
        self,
        input_path: str,
        output_path: str,
        width=None,
        height=None,
        maintain_aspect=True,
    ):
        """Resize image with optional aspect ratio preservation"""
        return self.process_image(
            input_path,
            output_path,
            "resize",
            width=width,
            height=height,
            maintain_aspect=maintain_aspect,
        )

    def apply_filters(self, input_path: str, output_path: str, filter_type: str):
        """Apply various filters to the image"""
        return self.process_image(
            input_path, output_path, "filter", filter_type=filter_type
        )

    def adjust_image(
        self,
        input_path: str,
        output_path: str,
        brightness=1.0,
        contrast=1.0,
        saturation=1.0,
        sharpness=1.0,
    ):
        """Adjust image brightness, contrast, saturation, and sharpness"""
        return self.process_image(
            input_path,
            output_path,
            "adjust",
            brightness=brightness,
            contrast=contrast,
            saturation=saturation,
            sharpness=sharpness,
        )

    def crop_image(
        self, input_path: str, output_path: str, x: int, y: int, width: int, height: int
    ):
        """Crop image to specified dimensions"""
        return self.process_image(
            input_path, output_path, "crop", x=x, y=y, width=width, height=height
        )

    def rotate_image(
        self, input_path: str, output_path: str, angle: float, expand=True
    ):
        """Rotate image by specified angle"""
        return self.process_image(
            input_path, output_path, "rotate", angle=angle, expand=expand
        )

    def flip_image(self, input_path: str, output_path: str, direction="horizontal"):
        """Flip image horizontally or vertically"""
        return self.process_image(input_path, output_path, "flip", direction=direction)

    def convert_format(self, input_path: str, output_path: str, format_type="PNG"):
        """Convert image to different format"""
        return self.process_image(
            input_path, output_path, "format", format_type=format_type
        )

    def create_thumbnail(self, input_path: str, output_path: str, size=(128, 128)):
        """Create thumbnail of the image"""
        return self.process_image(input_path, output_path, "thumbnail", size=size)

    def add_watermark(
        self,
        input_path: str,
        output_path: str,
        watermark_text: str,
        position="bottom-right",
        opacity=128,
    ):
        """Add text watermark to image"""
        return self.process_image(
            input_path,
            output_path,
            "watermark",
            watermark_text=watermark_text,
            position=position,
            opacity=opacity,
        )

    def apply_artistic_effects(self, input_path: str, output_path: str, effect="sepia"):
        """Apply artistic effects to the image"""
        return self.process_image(input_path, output_path, "effect", effect=effect)

    def create_border(
        self, input_path: str, output_path: str, border_width=10, border_color="black"
    ):
        """Add border around image"""
        return self.process_image(
            input_path,
            output_path,
            "border",
            border_width=border_width,
            border_color=border_color,
        )

    def apply_vignette(self, input_path: str, output_path: str, strength=0.5):
        """Apply vignette effect to image"""
        return self.process_image(
            input_path, output_path, "vignette", strength=strength
        )

    def extract_metadata(self, input_path):
        """Extract and display image metadata"""
        image = self.load_image(input_path)

        metadata = {
            "filename": os.path.basename(input_path),
            "format": image.format,
            "mode": image.mode,
            "size": image.size,
            "width": image.width,
            "height": image.height,
        }

        # Extract EXIF data if available
        exif_data = {}
        if hasattr(image, "_getexif") and image._getexif():
            exif = image._getexif()
            for tag_id, value in exif.items():
                tag = TAGS.get(tag_id, tag_id)
                exif_data[tag] = value

        if exif_data:
            metadata["exif"] = exif_data

        print(json.dumps(metadata, indent=2, default=str))
        return metadata

    def create_collage(self, input_paths, output_path, cols=2, padding=10):
        """Create a collage from multiple images"""
        if not input_paths:
            raise ValueError("No input images provided")

        images = [self.load_image(path) for path in input_paths]
        collage_creator = CollageCreator()
        collage = collage_creator.create_collage(images, cols, padding)
        self.save_image(collage, output_path)
        print(
            f"Created collage with {len(images)} images ({(len(images) + cols - 1) // cols}x{cols} grid)"
        )

    def create_composite(
        self,
        background_path: str,
        overlay_path: str,
        output_path: str,
        position=(0, 0),
        opacity=1.0,
    ):
        """Composite two images together"""
        compositor = ImageCompositor()
        background = self.load_image(background_path)
        overlay = self.load_image(overlay_path)
        composite = compositor.create_composite(background, overlay, position, opacity)
        self.save_image(composite, output_path)
        print(f"Created composite image at position {position} with opacity {opacity}")

    def create_contact_sheet(
        self, input_paths: list, output_path: str, sheet_width=1200, margin=10
    ):
        """Create a contact sheet from multiple images"""
        if not input_paths:
            raise ValueError("No input images provided")

        images = [self.load_image(path) for path in input_paths]
        contact_sheet_creator = ContactSheetCreator()
        contact_sheet = contact_sheet_creator.create_contact_sheet(
            images, sheet_width, margin
        )
        self.save_image(contact_sheet, output_path)
        print(f"Created contact sheet with {len(images)} images")

    # Color analysis methods (using external module)
    def analyze_histogram(self, input_path: str, output_path=None):
        """Analyze and optionally save image histogram"""
        image = self.load_image(input_path)
        return analyze_histogram(image, input_path, output_path)

    def extract_color_palette(self, input_path: str, num_colors=5):
        """Extract dominant colors from image"""
        image = self.load_image(input_path)
        return extract_color_palette(image, input_path, num_colors)

    def split_channels(self, input_path: str, output_dir: str):
        """Split image into separate color channels"""
        image = self.load_image(input_path)
        return split_channels(image, input_path, output_dir)

    def batch_process(self, input_dir: str, output_dir: str, operation: str, **kwargs):
        """Process multiple images in a directory"""
        batch_processor = BatchProcessor(self)
        return batch_processor.process_directory(
            input_dir, output_dir, operation, **kwargs
        )

    def simple_gui(self):
        """Launch a simple GUI for image processing"""
        from pillow_gui import launch_gui

        launch_gui(self)


def main():
    """Main function to handle command line arguments"""
    parser = argparse.ArgumentParser(
        description="Pillow CLI - Comprehensive Image Processing Tool"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Resize command
    resize_parser = subparsers.add_parser("resize", help="Resize image")
    resize_parser.add_argument("input", help="Input image path")
    resize_parser.add_argument("output", help="Output image path")
    resize_parser.add_argument("--width", type=int, help="Target width")
    resize_parser.add_argument("--height", type=int, help="Target height")
    resize_parser.add_argument(
        "--no-aspect", action="store_true", help="Don't maintain aspect ratio"
    )

    # Filter command
    filter_parser = subparsers.add_parser("filter", help="Apply filter to image")
    filter_parser.add_argument("input", help="Input image path")
    filter_parser.add_argument("output", help="Output image path")
    filter_parser.add_argument(
        "type",
        choices=[
            "blur",
            "contour",
            "detail",
            "edge_enhance",
            "edge_enhance_more",
            "emboss",
            "find_edges",
            "sharpen",
            "smooth",
            "smooth_more",
            "gaussian_blur",
            "unsharp_mask",
        ],
        help="Filter type",
    )

    # Adjust command
    adjust_parser = subparsers.add_parser("adjust", help="Adjust image properties")
    adjust_parser.add_argument("input", help="Input image path")
    adjust_parser.add_argument("output", help="Output image path")
    adjust_parser.add_argument(
        "--brightness", type=float, default=1.0, help="Brightness factor (default: 1.0)"
    )
    adjust_parser.add_argument(
        "--contrast", type=float, default=1.0, help="Contrast factor (default: 1.0)"
    )
    adjust_parser.add_argument(
        "--saturation", type=float, default=1.0, help="Saturation factor (default: 1.0)"
    )
    adjust_parser.add_argument(
        "--sharpness", type=float, default=1.0, help="Sharpness factor (default: 1.0)"
    )

    # Crop command
    crop_parser = subparsers.add_parser("crop", help="Crop image")
    crop_parser.add_argument("input", help="Input image path")
    crop_parser.add_argument("output", help="Output image path")
    crop_parser.add_argument("x", type=int, help="X coordinate")
    crop_parser.add_argument("y", type=int, help="Y coordinate")
    crop_parser.add_argument("width", type=int, help="Crop width")
    crop_parser.add_argument("height", type=int, help="Crop height")

    # Rotate command
    rotate_parser = subparsers.add_parser("rotate", help="Rotate image")
    rotate_parser.add_argument("input", help="Input image path")
    rotate_parser.add_argument("output", help="Output image path")
    rotate_parser.add_argument("angle", type=float, help="Rotation angle in degrees")
    rotate_parser.add_argument(
        "--no-expand", action="store_true", help="Don't expand canvas"
    )

    # Flip command
    flip_parser = subparsers.add_parser("flip", help="Flip image")
    flip_parser.add_argument("input", help="Input image path")
    flip_parser.add_argument("output", help="Output image path")
    flip_parser.add_argument(
        "direction", choices=["horizontal", "vertical"], help="Flip direction"
    )

    # Convert command
    convert_parser = subparsers.add_parser("convert", help="Convert image format")
    convert_parser.add_argument("input", help="Input image path")
    convert_parser.add_argument("output", help="Output image path")
    convert_parser.add_argument(
        "--format", default="PNG", help="Target format (default: PNG)"
    )

    # Thumbnail command
    thumbnail_parser = subparsers.add_parser("thumbnail", help="Create thumbnail")
    thumbnail_parser.add_argument("input", help="Input image path")
    thumbnail_parser.add_argument("output", help="Output image path")
    thumbnail_parser.add_argument(
        "--size",
        type=int,
        nargs=2,
        default=[128, 128],
        help="Thumbnail size (width height)",
    )

    # Watermark command
    watermark_parser = subparsers.add_parser("watermark", help="Add watermark")
    watermark_parser.add_argument("input", help="Input image path")
    watermark_parser.add_argument("output", help="Output image path")
    watermark_parser.add_argument("text", help="Watermark text")
    watermark_parser.add_argument(
        "--position",
        choices=["top-left", "top-right", "bottom-left", "bottom-right", "center"],
        default="bottom-right",
        help="Watermark position",
    )
    watermark_parser.add_argument(
        "--opacity", type=int, default=128, help="Watermark opacity (0-255)"
    )

    # Metadata command
    metadata_parser = subparsers.add_parser("metadata", help="Extract image metadata")
    metadata_parser.add_argument("input", help="Input image path")

    # Collage command
    collage_parser = subparsers.add_parser(
        "collage", help="Create collage from multiple images"
    )
    collage_parser.add_argument("output", help="Output image path")
    collage_parser.add_argument("inputs", nargs="+", help="Input image paths")
    collage_parser.add_argument("--cols", type=int, default=2, help="Number of columns")
    collage_parser.add_argument(
        "--padding", type=int, default=10, help="Padding between images"
    )

    # Effect command
    effect_parser = subparsers.add_parser("effect", help="Apply artistic effects")
    effect_parser.add_argument("input", help="Input image path")
    effect_parser.add_argument("output", help="Output image path")
    effect_parser.add_argument(
        "type",
        choices=["sepia", "grayscale", "invert", "posterize", "solarize"],
        help="Effect type",
    )

    # Batch command
    batch_parser = subparsers.add_parser("batch", help="Batch process images")
    batch_parser.add_argument("input_dir", help="Input directory")
    batch_parser.add_argument("output_dir", help="Output directory")
    batch_parser.add_argument(
        "operation",
        choices=["resize", "filter", "adjust", "effect", "thumbnail"],
        help="Batch operation",
    )
    batch_parser.add_argument("--width", type=int, help="Width for resize operation")
    batch_parser.add_argument("--height", type=int, help="Height for resize operation")
    batch_parser.add_argument("--filter-type", help="Filter type for filter operation")
    batch_parser.add_argument("--effect-type", help="Effect type for effect operation")
    batch_parser.add_argument(
        "--size",
        type=int,
        nargs=2,
        default=[128, 128],
        help="Size for thumbnail operation",
    )

    # GUI command
    gui_parser = subparsers.add_parser("gui", help="Launch simple GUI")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    cli = PillowCLI()

    try:
        match args.command:
            case "resize":
                cli.resize_image(
                    args.input,
                    args.output,
                    args.width,
                    args.height,
                    maintain_aspect=not args.no_aspect,
                )

            case "filter":
                cli.apply_filters(args.input, args.output, args.type)

            case "adjust":
                cli.adjust_image(
                    args.input,
                    args.output,
                    args.brightness,
                    args.contrast,
                    args.saturation,
                    args.sharpness,
                )

            case "crop":
                cli.crop_image(
                    args.input, args.output, args.x, args.y, args.width, args.height
                )

            case "rotate":
                cli.rotate_image(
                    args.input, args.output, args.angle, expand=not args.no_expand
                )

            case "flip":
                cli.flip_image(args.input, args.output, args.direction)

            case "convert":
                cli.convert_format(args.input, args.output, args.format)

            case "thumbnail":
                cli.create_thumbnail(args.input, args.output, tuple(args.size))

            case "watermark":
                cli.add_watermark(
                    args.input, args.output, args.text, args.position, args.opacity
                )

            case "metadata":
                cli.extract_metadata(args.input)

            case "collage":
                cli.create_collage(args.inputs, args.output, args.cols, args.padding)

            case "effect":
                cli.apply_artistic_effects(args.input, args.output, args.type)

            case "batch":
                kwargs = {}
                if args.operation == "resize":
                    kwargs = {"width": args.width, "height": args.height}
                elif args.operation == "filter":
                    kwargs = {"filter_type": args.filter_type}
                elif args.operation == "effect":
                    kwargs = {"effect": args.effect_type}
                elif args.operation == "thumbnail":
                    kwargs = {"size": tuple(args.size)}

                cli.batch_process(
                    args.input_dir, args.output_dir, args.operation, **kwargs
                )

            case "gui":
                cli.simple_gui()

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
