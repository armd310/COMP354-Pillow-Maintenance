"""
GUI Interface for Pillow CLI - Comprehensive Image Processing Tool
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import os

# Check for GUI availability
try:
    import tkinter as tk
    from tkinter import ttk

    GUI_AVAILABLE = True
except ImportError:
    GUI_AVAILABLE = False


class PillowGUI:
    """GUI interface for the Pillow CLI tool"""

    def __init__(self, cli_instance):
        """Initialize GUI with reference to CLI instance"""
        self.cli = cli_instance
        self.root = None
        self.setup_variables()
        # Preview related attributes
        self.current_image = None
        self.preview_image = None
        self.original_label = None
        self.preview_label = None
        self.preview_enabled = True

    def setup_variables(self):
        """Initialize all tkinter variables"""
        # Common variables
        self.input_var = None
        self.output_var = None
        self.operation_var = None
        self.status_var = None

        # Resize parameters
        self.width_var = None
        self.height_var = None
        self.maintain_aspect_var = None

        # Filter parameters
        self.filter_type_var = None

        # Adjust parameters
        self.brightness_var = None
        self.contrast_var = None
        self.saturation_var = None
        self.sharpness_var = None

        # Crop parameters
        self.crop_x_var = None
        self.crop_y_var = None
        self.crop_width_var = None
        self.crop_height_var = None

        # Rotate parameters
        self.angle_var = None
        self.expand_var = None

        # Flip parameters
        self.direction_var = None

        # Watermark parameters
        self.watermark_text_var = None
        self.watermark_pos_var = None
        self.opacity_var = None

        # Border parameters
        self.border_width_var = None
        self.border_color_var = None

        # Vignette parameters
        self.vignette_strength_var = None

        # Effect parameters
        self.effect_type_var = None

        # Thumbnail parameters
        self.thumb_size_var = None

        # GUI components
        self.params_frame = None

    def initialize_variables(self):
        """Initialize tkinter variables with default values"""
        # Common variables
        self.input_var = tk.StringVar()
        self.output_var = tk.StringVar()
        self.operation_var = tk.StringVar(value="Resize")
        self.status_var = tk.StringVar(value="Ready")

        # Bind input variable to preview update
        self.input_var.trace("w", self.on_input_change)

        # Resize parameters
        self.width_var = tk.StringVar(value="300")
        self.height_var = tk.StringVar(value="300")
        self.maintain_aspect_var = tk.BooleanVar(value=True)

        # Filter parameters
        self.filter_type_var = tk.StringVar(value="blur")

        # Adjust parameters
        self.brightness_var = tk.StringVar(value="1.0")
        self.contrast_var = tk.StringVar(value="1.0")
        self.saturation_var = tk.StringVar(value="1.0")
        self.sharpness_var = tk.StringVar(value="1.0")

        # Crop parameters
        self.crop_x_var = tk.StringVar(value="0")
        self.crop_y_var = tk.StringVar(value="0")
        self.crop_width_var = tk.StringVar(value="100")
        self.crop_height_var = tk.StringVar(value="100")

        # Rotate parameters
        self.angle_var = tk.StringVar(value="90")
        self.expand_var = tk.BooleanVar(value=True)

        # Flip parameters
        self.direction_var = tk.StringVar(value="horizontal")

        # Watermark parameters
        self.watermark_text_var = tk.StringVar(value="Watermark")
        self.watermark_pos_var = tk.StringVar(value="bottom-right")
        self.opacity_var = tk.StringVar(value="128")

        # Border parameters
        self.border_width_var = tk.StringVar(value="10")
        self.border_color_var = tk.StringVar(value="black")

        # Vignette parameters
        self.vignette_strength_var = tk.StringVar(value="0.5")

        # Effect parameters
        self.effect_type_var = tk.StringVar(value="sepia")

        # Thumbnail parameters
        self.thumb_size_var = tk.StringVar(value="128,128")

    def get_operation_parameters(self):
        """Extract parameters for the current operation"""
        operation = self.operation_var.get()
        params = {}

        try:
            if operation == "Resize":
                params = {
                    "width": (
                        int(self.width_var.get()) if self.width_var.get() else None
                    ),
                    "height": (
                        int(self.height_var.get()) if self.height_var.get() else None
                    ),
                    "maintain_aspect": self.maintain_aspect_var.get(),
                }

            elif operation in [
                "Blur",
                "Sharpen",
                "Edge Enhance",
                "Emboss",
                "Find Edges",
                "Smooth",
                "Contour",
                "Detail",
            ]:
                params = {"filter_type": self.filter_type_var.get()}

            elif operation == "Adjust":
                params = {
                    "brightness": (
                        float(self.brightness_var.get())
                        if self.brightness_var.get()
                        else 1.0
                    ),
                    "contrast": (
                        float(self.contrast_var.get())
                        if self.contrast_var.get()
                        else 1.0
                    ),
                    "saturation": (
                        float(self.saturation_var.get())
                        if self.saturation_var.get()
                        else 1.0
                    ),
                    "sharpness": (
                        float(self.sharpness_var.get())
                        if self.sharpness_var.get()
                        else 1.0
                    ),
                }

            elif operation == "Crop":
                params = {
                    "x": int(self.crop_x_var.get()) if self.crop_x_var.get() else 0,
                    "y": int(self.crop_y_var.get()) if self.crop_y_var.get() else 0,
                    "width": (
                        int(self.crop_width_var.get())
                        if self.crop_width_var.get()
                        else 100
                    ),
                    "height": (
                        int(self.crop_height_var.get())
                        if self.crop_height_var.get()
                        else 100
                    ),
                }

            elif operation == "Rotate":
                params = {
                    "angle": float(self.angle_var.get()) if self.angle_var.get() else 0,
                    "expand": self.expand_var.get(),
                }

            elif operation == "Flip":
                params = {"direction": self.direction_var.get()}

            elif operation == "Watermark":
                params = {
                    "watermark_text": self.watermark_text_var.get(),
                    "position": self.watermark_pos_var.get(),
                    "opacity": (
                        int(self.opacity_var.get()) if self.opacity_var.get() else 128
                    ),
                }

            elif operation == "Border":
                params = {
                    "border_width": (
                        int(self.border_width_var.get())
                        if self.border_width_var.get()
                        else 10
                    ),
                    "border_color": self.border_color_var.get(),
                }

            elif operation == "Vignette":
                params = {
                    "strength": (
                        float(self.vignette_strength_var.get())
                        if self.vignette_strength_var.get()
                        else 0.5
                    )
                }

            elif operation in ["Sepia", "Grayscale", "Invert", "Posterize", "Solarize"]:
                params = {"effect": self.effect_type_var.get()}

            elif operation == "Thumbnail":
                size_str = self.thumb_size_var.get() or "128,128"
                params = {"size": tuple(map(int, size_str.split(",")))}

        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid parameter values: {str(e)}")

        return params

    def apply_operation_to_image(self, image, operation=None, for_preview=False):
        """Apply the current operation to an image using the processor classes directly"""
        if operation is None:
            operation = self.operation_var.get()

        params = self.get_operation_parameters()
        processed_image = image.copy()

        try:
            if operation == "Resize":
                processor = self.cli.processors["resize"]
                processed_image = processor.process(processed_image, **params)

            elif operation in [
                "Blur",
                "Sharpen",
                "Edge Enhance",
                "Emboss",
                "Find Edges",
                "Smooth",
                "Contour",
                "Detail",
            ]:
                processor = self.cli.processors["filter"]
                processed_image = processor.process(processed_image, **params)

            elif operation == "Adjust":
                processor = self.cli.processors["adjustment"]
                processed_image = processor.process(processed_image, **params)

            elif operation == "Crop":
                processor = self.cli.processors["crop"]
                processed_image = processor.process(processed_image, **params)

            elif operation == "Rotate":
                processor = self.cli.processors["rotate"]
                processed_image = processor.process(processed_image, **params)

            elif operation == "Flip":
                processor = self.cli.processors["flip"]
                processed_image = processor.process(processed_image, **params)

            elif operation == "Watermark":
                processor = self.cli.processors["watermark"]
                processed_image = processor.process(processed_image, **params)

            elif operation == "Border":
                processor = self.cli.processors["border"]
                processed_image = processor.process(processed_image, **params)

            elif operation == "Vignette":
                processor = self.cli.processors["vignette"]
                processed_image = processor.process(processed_image, **params)

            elif operation in ["Sepia", "Grayscale", "Invert", "Posterize", "Solarize"]:
                processor = self.cli.processors["effect"]
                processed_image = processor.process(processed_image, **params)

            elif operation == "Thumbnail":
                processor = self.cli.processors["thumbnail"]
                processed_image = processor.process(processed_image, **params)

        except Exception as e:
            if for_preview:
                raise  # Let preview handler deal with the error
            else:
                raise ValueError(f"Error applying {operation}: {str(e)}")

        return processed_image

    def resize_image_for_preview(self, image, max_size=(250, 250)):
        """Resize image to fit in preview while maintaining aspect ratio"""
        image.thumbnail(max_size, Image.Resampling.LANCZOS)
        return image

    def load_and_display_image(self, image_path):
        """Load image and display in original preview"""
        try:
            if not os.path.exists(image_path):
                return

            # Load and resize for preview
            image = Image.open(image_path)
            self.current_image = image.copy()

            # Create preview image
            preview_img = self.current_image.copy()
            preview_img = self.resize_image_for_preview(preview_img)

            # Convert to PhotoImage for tkinter
            photo = ImageTk.PhotoImage(preview_img)

            # Update original image label
            if self.original_label:
                self.original_label.configure(image=photo)
                self.original_label.image = photo  # Keep a reference

            # Clear preview when new image is loaded
            if self.preview_label:
                self.preview_label.configure(image="", text="Preview will appear here")
                self.preview_label.image = None

        except Exception as e:
            self.status_var.set(f"Error loading image: {str(e)}")

    def on_input_change(self, *args):
        """Called when input file path changes"""
        image_path = self.input_var.get()
        if image_path and os.path.exists(image_path):
            self.load_and_display_image(image_path)

    def update_preview(self):
        """Update the preview with the current operation applied"""
        if not self.current_image or not self.preview_enabled:
            return

        try:
            # Use the centralized operation handler
            processed_image = self.apply_operation_to_image(
                self.current_image, for_preview=True
            )

            # Resize for preview display
            preview_img = self.resize_image_for_preview(processed_image.copy())

            # Convert to PhotoImage for tkinter
            photo = ImageTk.PhotoImage(preview_img)

            # Update preview label
            if self.preview_label:
                self.preview_label.configure(image=photo, text="")
                self.preview_label.image = photo  # Keep a reference

        except Exception as e:
            if self.preview_label:
                self.preview_label.configure(image="", text=f"Preview error: {str(e)}")
                self.preview_label.image = None

    def browse_input(self):
        """Browse for input image file"""
        filename = filedialog.askopenfilename(
            title="Select Input Image",
            filetypes=[
                ("Image files", "*.jpg *.jpeg *.png *.bmp *.gif *.tiff *.webp"),
                ("All files", "*.*"),
            ],
        )
        if filename:
            self.input_var.set(filename)

    def browse_output(self):
        """Browse for output image file location"""
        filename = filedialog.asksaveasfilename(
            title="Save Output Image As",
            filetypes=[
                ("PNG files", "*.png"),
                ("JPEG files", "*.jpg"),
                ("All files", "*.*"),
            ],
        )
        if filename:
            self.output_var.set(filename)

    def on_operation_change(self, *args):
        """Update parameter fields based on selected operation"""
        operation = self.operation_var.get()

        # Clear all parameter widgets
        for widget in self.params_frame.winfo_children():
            widget.destroy()

        row = 0
        if operation == "Resize":
            ttk.Label(self.params_frame, text="Width:").grid(
                row=row, column=0, sticky=tk.W, padx=5, pady=2
            )
            width_entry = ttk.Entry(
                self.params_frame, textvariable=self.width_var, width=10
            )
            width_entry.grid(row=row, column=1, padx=5, pady=2)
            width_entry.bind(
                "<KeyRelease>", lambda e: self.root.after(500, self.update_preview)
            )

            ttk.Label(self.params_frame, text="Height:").grid(
                row=row, column=2, sticky=tk.W, padx=5, pady=2
            )
            height_entry = ttk.Entry(
                self.params_frame, textvariable=self.height_var, width=10
            )
            height_entry.grid(row=row, column=3, padx=5, pady=2)
            height_entry.bind(
                "<KeyRelease>", lambda e: self.root.after(500, self.update_preview)
            )

            row += 1
            aspect_check = ttk.Checkbutton(
                self.params_frame,
                text="Maintain aspect ratio",
                variable=self.maintain_aspect_var,
                command=lambda: self.root.after(100, self.update_preview),
            )
            aspect_check.grid(
                row=row, column=0, columnspan=2, sticky=tk.W, padx=5, pady=2
            )

        elif operation in [
            "Blur",
            "Sharpen",
            "Edge Enhance",
            "Emboss",
            "Find Edges",
            "Smooth",
            "Contour",
            "Detail",
        ]:
            ttk.Label(self.params_frame, text="Filter Type:").grid(
                row=row, column=0, sticky=tk.W, padx=5, pady=2
            )
            filter_combo = ttk.Combobox(
                self.params_frame,
                textvariable=self.filter_type_var,
                width=15,
                values=[
                    "blur",
                    "sharpen",
                    "edge_enhance",
                    "emboss",
                    "find_edges",
                    "smooth",
                    "contour",
                    "detail",
                    "gaussian_blur",
                    "unsharp_mask",
                ],
                state="readonly",
            )
            filter_combo.grid(row=row, column=1, padx=5, pady=2)
            filter_combo.set(operation.lower().replace(" ", "_"))
            filter_combo.bind("<<ComboboxSelected>>", lambda e: self.update_preview())

        elif operation == "Adjust":
            ttk.Label(self.params_frame, text="Brightness:").grid(
                row=row, column=0, sticky=tk.W, padx=5, pady=2
            )
            brightness_entry = ttk.Entry(
                self.params_frame, textvariable=self.brightness_var, width=8
            )
            brightness_entry.grid(row=row, column=1, padx=5, pady=2)
            brightness_entry.bind(
                "<KeyRelease>", lambda e: self.root.after(500, self.update_preview)
            )

            ttk.Label(self.params_frame, text="Contrast:").grid(
                row=row, column=2, sticky=tk.W, padx=5, pady=2
            )
            contrast_entry = ttk.Entry(
                self.params_frame, textvariable=self.contrast_var, width=8
            )
            contrast_entry.grid(row=row, column=3, padx=5, pady=2)
            contrast_entry.bind(
                "<KeyRelease>", lambda e: self.root.after(500, self.update_preview)
            )

            row += 1
            ttk.Label(self.params_frame, text="Saturation:").grid(
                row=row, column=0, sticky=tk.W, padx=5, pady=2
            )
            saturation_entry = ttk.Entry(
                self.params_frame, textvariable=self.saturation_var, width=8
            )
            saturation_entry.grid(row=row, column=1, padx=5, pady=2)
            saturation_entry.bind(
                "<KeyRelease>", lambda e: self.root.after(500, self.update_preview)
            )

            ttk.Label(self.params_frame, text="Sharpness:").grid(
                row=row, column=2, sticky=tk.W, padx=5, pady=2
            )
            sharpness_entry = ttk.Entry(
                self.params_frame, textvariable=self.sharpness_var, width=8
            )
            sharpness_entry.grid(row=row, column=3, padx=5, pady=2)
            sharpness_entry.bind(
                "<KeyRelease>", lambda e: self.root.after(500, self.update_preview)
            )

        elif operation == "Crop":
            ttk.Label(self.params_frame, text="X:").grid(
                row=row, column=0, sticky=tk.W, padx=5, pady=2
            )
            x_entry = ttk.Entry(
                self.params_frame, textvariable=self.crop_x_var, width=8
            )
            x_entry.grid(row=row, column=1, padx=5, pady=2)
            x_entry.bind(
                "<KeyRelease>", lambda e: self.root.after(500, self.update_preview)
            )

            ttk.Label(self.params_frame, text="Y:").grid(
                row=row, column=2, sticky=tk.W, padx=5, pady=2
            )
            y_entry = ttk.Entry(
                self.params_frame, textvariable=self.crop_y_var, width=8
            )
            y_entry.grid(row=row, column=3, padx=5, pady=2)
            y_entry.bind(
                "<KeyRelease>", lambda e: self.root.after(500, self.update_preview)
            )

            row += 1
            ttk.Label(self.params_frame, text="Width:").grid(
                row=row, column=0, sticky=tk.W, padx=5, pady=2
            )
            width_entry = ttk.Entry(
                self.params_frame, textvariable=self.crop_width_var, width=8
            )
            width_entry.grid(row=row, column=1, padx=5, pady=2)
            width_entry.bind(
                "<KeyRelease>", lambda e: self.root.after(500, self.update_preview)
            )

            ttk.Label(self.params_frame, text="Height:").grid(
                row=row, column=2, sticky=tk.W, padx=5, pady=2
            )
            height_entry = ttk.Entry(
                self.params_frame, textvariable=self.crop_height_var, width=8
            )
            height_entry.grid(row=row, column=3, padx=5, pady=2)
            height_entry.bind(
                "<KeyRelease>", lambda e: self.root.after(500, self.update_preview)
            )

        elif operation == "Rotate":
            ttk.Label(self.params_frame, text="Angle:").grid(
                row=row, column=0, sticky=tk.W, padx=5, pady=2
            )
            angle_entry = ttk.Entry(
                self.params_frame, textvariable=self.angle_var, width=10
            )
            angle_entry.grid(row=row, column=1, padx=5, pady=2)
            angle_entry.bind(
                "<KeyRelease>", lambda e: self.root.after(500, self.update_preview)
            )

            expand_check = ttk.Checkbutton(
                self.params_frame,
                text="Expand canvas",
                variable=self.expand_var,
                command=lambda: self.root.after(100, self.update_preview),
            )
            expand_check.grid(
                row=row, column=2, columnspan=2, sticky=tk.W, padx=5, pady=2
            )

        elif operation == "Flip":
            ttk.Label(self.params_frame, text="Direction:").grid(
                row=row, column=0, sticky=tk.W, padx=5, pady=2
            )
            direction_combo = ttk.Combobox(
                self.params_frame,
                textvariable=self.direction_var,
                width=12,
                values=["horizontal", "vertical"],
                state="readonly",
            )
            direction_combo.grid(row=row, column=1, padx=5, pady=2)
            direction_combo.set("horizontal")
            direction_combo.bind(
                "<<ComboboxSelected>>", lambda e: self.update_preview()
            )

        elif operation == "Watermark":
            ttk.Label(self.params_frame, text="Text:").grid(
                row=row, column=0, sticky=tk.W, padx=5, pady=2
            )
            text_entry = ttk.Entry(
                self.params_frame, textvariable=self.watermark_text_var, width=20
            )
            text_entry.grid(row=row, column=1, columnspan=2, padx=5, pady=2)
            text_entry.bind(
                "<KeyRelease>", lambda e: self.root.after(500, self.update_preview)
            )

            row += 1
            ttk.Label(self.params_frame, text="Position:").grid(
                row=row, column=0, sticky=tk.W, padx=5, pady=2
            )
            pos_combo = ttk.Combobox(
                self.params_frame,
                textvariable=self.watermark_pos_var,
                width=12,
                values=[
                    "top-left",
                    "top-right",
                    "bottom-left",
                    "bottom-right",
                    "center",
                ],
                state="readonly",
            )
            pos_combo.grid(row=row, column=1, padx=5, pady=2)
            pos_combo.set("bottom-right")
            pos_combo.bind("<<ComboboxSelected>>", lambda e: self.update_preview())

            ttk.Label(self.params_frame, text="Opacity:").grid(
                row=row, column=2, sticky=tk.W, padx=5, pady=2
            )
            opacity_entry = ttk.Entry(
                self.params_frame, textvariable=self.opacity_var, width=8
            )
            opacity_entry.grid(row=row, column=3, padx=5, pady=2)
            opacity_entry.bind(
                "<KeyRelease>", lambda e: self.root.after(500, self.update_preview)
            )

        elif operation == "Border":
            ttk.Label(self.params_frame, text="Width:").grid(
                row=row, column=0, sticky=tk.W, padx=5, pady=2
            )
            border_entry = ttk.Entry(
                self.params_frame, textvariable=self.border_width_var, width=8
            )
            border_entry.grid(row=row, column=1, padx=5, pady=2)
            border_entry.bind(
                "<KeyRelease>", lambda e: self.root.after(500, self.update_preview)
            )

            ttk.Label(self.params_frame, text="Color:").grid(
                row=row, column=2, sticky=tk.W, padx=5, pady=2
            )
            color_combo = ttk.Combobox(
                self.params_frame,
                textvariable=self.border_color_var,
                width=10,
                values=["black", "white", "red", "green", "blue"],
                state="readonly",
            )
            color_combo.grid(row=row, column=3, padx=5, pady=2)
            color_combo.set("black")
            color_combo.bind("<<ComboboxSelected>>", lambda e: self.update_preview())

        elif operation == "Vignette":
            ttk.Label(self.params_frame, text="Strength:").grid(
                row=row, column=0, sticky=tk.W, padx=5, pady=2
            )
            vignette_entry = ttk.Entry(
                self.params_frame, textvariable=self.vignette_strength_var, width=8
            )
            vignette_entry.grid(row=row, column=1, padx=5, pady=2)
            vignette_entry.bind(
                "<KeyRelease>", lambda e: self.root.after(500, self.update_preview)
            )

            ttk.Label(self.params_frame, text="(0.0 - 1.0)").grid(
                row=row, column=2, sticky=tk.W, padx=5, pady=2
            )

        elif operation in ["Sepia", "Grayscale", "Invert", "Posterize", "Solarize"]:
            ttk.Label(self.params_frame, text="Effect Type:").grid(
                row=row, column=0, sticky=tk.W, padx=5, pady=2
            )
            effect_combo = ttk.Combobox(
                self.params_frame,
                textvariable=self.effect_type_var,
                width=12,
                values=["sepia", "grayscale", "invert", "posterize", "solarize"],
                state="readonly",
            )
            effect_combo.grid(row=row, column=1, padx=5, pady=2)
            effect_combo.set(operation.lower())
            effect_combo.bind("<<ComboboxSelected>>", lambda e: self.update_preview())

        elif operation == "Thumbnail":
            ttk.Label(self.params_frame, text="Size:").grid(
                row=row, column=0, sticky=tk.W, padx=5, pady=2
            )
            thumb_entry = ttk.Entry(
                self.params_frame, textvariable=self.thumb_size_var, width=12
            )
            thumb_entry.grid(row=row, column=1, padx=5, pady=2)
            thumb_entry.bind(
                "<KeyRelease>", lambda e: self.root.after(500, self.update_preview)
            )

            ttk.Label(self.params_frame, text="(e.g., 128,128)").grid(
                row=row, column=2, sticky=tk.W, padx=5, pady=2
            )

        # Update preview after changing operation
        self.root.after(100, self.update_preview)

    def process_image(self):
        """Process the image based on selected operation and parameters"""
        input_file = self.input_var.get()
        output_file = self.output_var.get()

        if not input_file or not output_file:
            self.status_var.set("Please select input and output files")
            return

        try:
            # Load the input image
            input_image = self.cli.load_image(input_file)

            # Apply the operation using the centralized handler
            processed_image = self.apply_operation_to_image(input_image)

            # Save the processed image
            self.cli.save_image(processed_image, output_file)

            self.status_var.set(f"Success! Processed image saved to {output_file}")
            messagebox.showinfo(
                "Success", f"Image processed successfully!\nSaved to: {output_file}"
            )

        except Exception as e:
            error_msg = f"Error: {str(e)}"
            self.status_var.set(error_msg)
            messagebox.showerror("Error", error_msg)

    def launch(self):
        """Launch the GUI interface"""
        if not GUI_AVAILABLE:
            print("GUI not available. Install tkinter to use this feature.")
            return

        self.root = tk.Tk()
        self.root.title("Pillow CLI - Complete Image Editor")
        self.root.geometry("1200x800")
        self.root.resizable(True, True)

        # Initialize variables
        self.initialize_variables()

        # Create main container with horizontal split
        main_container = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Left frame for controls
        left_frame = ttk.Frame(main_container)
        main_container.add(left_frame, weight=1)

        # Right frame for preview
        right_frame = ttk.Frame(main_container)
        main_container.add(right_frame, weight=1)

        # Create scrollable area for controls
        canvas = tk.Canvas(left_frame)
        scrollbar = ttk.Scrollbar(left_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        control_frame = ttk.Frame(scrollable_frame, padding="10")
        control_frame.pack(fill=tk.BOTH, expand=True)

        # Input file selection
        ttk.Label(control_frame, text="Input Image:").pack(anchor=tk.W, pady=5)
        input_frame = ttk.Frame(control_frame)
        input_frame.pack(fill=tk.X, pady=5)
        ttk.Entry(input_frame, textvariable=self.input_var, width=40).pack(
            side=tk.LEFT, fill=tk.X, expand=True
        )
        ttk.Button(input_frame, text="Browse", command=self.browse_input).pack(
            side=tk.RIGHT, padx=(5, 0)
        )

        # Output file selection
        ttk.Label(control_frame, text="Output Image:").pack(anchor=tk.W, pady=5)
        output_frame = ttk.Frame(control_frame)
        output_frame.pack(fill=tk.X, pady=5)
        ttk.Entry(output_frame, textvariable=self.output_var, width=40).pack(
            side=tk.LEFT, fill=tk.X, expand=True
        )
        ttk.Button(output_frame, text="Browse", command=self.browse_output).pack(
            side=tk.RIGHT, padx=(5, 0)
        )

        # Operation selection
        ttk.Label(control_frame, text="Operation:").pack(anchor=tk.W, pady=5)
        operation_combo = ttk.Combobox(
            control_frame,
            textvariable=self.operation_var,
            width=20,
            values=[
                "Resize",
                "Blur",
                "Sharpen",
                "Edge Enhance",
                "Emboss",
                "Find Edges",
                "Smooth",
                "Contour",
                "Detail",
                "Adjust",
                "Crop",
                "Rotate",
                "Flip",
                "Watermark",
                "Border",
                "Vignette",
                "Sepia",
                "Grayscale",
                "Invert",
                "Posterize",
                "Solarize",
                "Thumbnail",
            ],
            state="readonly",
        )
        operation_combo.pack(fill=tk.X, pady=5)
        operation_combo.bind("<<ComboboxSelected>>", self.on_operation_change)

        # Parameters frame
        self.params_frame = ttk.LabelFrame(
            control_frame, text="Parameters", padding="10"
        )
        self.params_frame.pack(fill=tk.X, pady=10)

        # Process button
        ttk.Button(
            control_frame, text="Process Image", command=self.process_image
        ).pack(pady=20)

        # Status
        ttk.Label(control_frame, text="Status:").pack(anchor=tk.W, pady=5)
        status_label = ttk.Label(
            control_frame, textvariable=self.status_var, foreground="blue"
        )
        status_label.pack(anchor=tk.W, pady=5)

        # Pack canvas and scrollbar for left frame
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Preview frame on the right
        preview_frame = ttk.LabelFrame(right_frame, text="Image Preview", padding="10")
        preview_frame.pack(fill=tk.BOTH, expand=True)

        # Create notebook for original and preview tabs
        preview_notebook = ttk.Notebook(preview_frame)
        preview_notebook.pack(fill=tk.BOTH, expand=True)

        # Original image tab
        original_tab = ttk.Frame(preview_notebook)
        preview_notebook.add(original_tab, text="Original")

        self.original_label = ttk.Label(
            original_tab,
            text="Load an image to see preview",
            anchor="center",
            background="white",
        )
        self.original_label.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Preview tab
        preview_tab = ttk.Frame(preview_notebook)
        preview_notebook.add(preview_tab, text="Preview")

        self.preview_label = ttk.Label(
            preview_tab,
            text="Preview will appear here",
            anchor="center",
            background="white",
        )
        self.preview_label.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Preview controls
        preview_controls = ttk.Frame(preview_frame)
        preview_controls.pack(fill=tk.X, pady=(5, 0))

        ttk.Button(
            preview_controls, text="Refresh Preview", command=self.update_preview
        ).pack(side=tk.LEFT, padx=(0, 5))

        preview_check = ttk.Checkbutton(
            preview_controls, text="Auto Preview", variable=tk.BooleanVar(value=True)
        )
        preview_check.pack(side=tk.LEFT)

        # Initialize with default operation
        self.on_operation_change()

        self.root.mainloop()


def launch_gui(cli_instance):
    """Convenience function to launch the GUI"""
    gui = PillowGUI(cli_instance)
    gui.launch()
