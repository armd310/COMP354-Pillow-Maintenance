"""
GUI Interface for Pillow CLI - Comprehensive Image Processing Tool
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

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

    def browse_input(self):
        """Browse for input image file"""
        filename = filedialog.askopenfilename(
            title="Select Input Image",
            filetypes=[
                ("Image files", "*.jpg *.jpeg *.png *.bmp *.gif *.tiff *.webp"),
                ("All files", "*.*")
            ]
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
                ("All files", "*.*")
            ]
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
            ttk.Label(self.params_frame, text="Width:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=2)
            ttk.Entry(self.params_frame, textvariable=self.width_var, width=10).grid(row=row, column=1, padx=5, pady=2)
            ttk.Label(self.params_frame, text="Height:").grid(row=row, column=2, sticky=tk.W, padx=5, pady=2)
            ttk.Entry(self.params_frame, textvariable=self.height_var, width=10).grid(row=row, column=3, padx=5, pady=2)
            row += 1
            ttk.Checkbutton(self.params_frame, text="Maintain aspect ratio",
                            variable=self.maintain_aspect_var).grid(row=row, column=0, columnspan=2, sticky=tk.W,
                                                                    padx=5, pady=2)

        elif operation in ["Blur", "Sharpen", "Edge Enhance", "Emboss", "Find Edges", "Smooth", "Contour", "Detail"]:
            ttk.Label(self.params_frame, text="Filter Type:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=2)
            filter_combo = ttk.Combobox(self.params_frame, textvariable=self.filter_type_var, width=15,
                                        values=["blur", "sharpen", "edge_enhance", "emboss", "find_edges",
                                                "smooth", "contour", "detail", "gaussian_blur", "unsharp_mask"],
                                        state="readonly")
            filter_combo.grid(row=row, column=1, padx=5, pady=2)
            filter_combo.set(operation.lower().replace(" ", "_"))

        elif operation == "Adjust":
            ttk.Label(self.params_frame, text="Brightness:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=2)
            ttk.Entry(self.params_frame, textvariable=self.brightness_var, width=8).grid(row=row, column=1, padx=5,
                                                                                         pady=2)
            ttk.Label(self.params_frame, text="Contrast:").grid(row=row, column=2, sticky=tk.W, padx=5, pady=2)
            ttk.Entry(self.params_frame, textvariable=self.contrast_var, width=8).grid(row=row, column=3, padx=5,
                                                                                       pady=2)
            row += 1
            ttk.Label(self.params_frame, text="Saturation:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=2)
            ttk.Entry(self.params_frame, textvariable=self.saturation_var, width=8).grid(row=row, column=1, padx=5,
                                                                                         pady=2)
            ttk.Label(self.params_frame, text="Sharpness:").grid(row=row, column=2, sticky=tk.W, padx=5, pady=2)
            ttk.Entry(self.params_frame, textvariable=self.sharpness_var, width=8).grid(row=row, column=3, padx=5,
                                                                                        pady=2)

        elif operation == "Crop":
            ttk.Label(self.params_frame, text="X:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=2)
            ttk.Entry(self.params_frame, textvariable=self.crop_x_var, width=8).grid(row=row, column=1, padx=5, pady=2)
            ttk.Label(self.params_frame, text="Y:").grid(row=row, column=2, sticky=tk.W, padx=5, pady=2)
            ttk.Entry(self.params_frame, textvariable=self.crop_y_var, width=8).grid(row=row, column=3, padx=5, pady=2)
            row += 1
            ttk.Label(self.params_frame, text="Width:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=2)
            ttk.Entry(self.params_frame, textvariable=self.crop_width_var, width=8).grid(row=row, column=1, padx=5,
                                                                                         pady=2)
            ttk.Label(self.params_frame, text="Height:").grid(row=row, column=2, sticky=tk.W, padx=5, pady=2)
            ttk.Entry(self.params_frame, textvariable=self.crop_height_var, width=8).grid(row=row, column=3, padx=5,
                                                                                          pady=2)

        elif operation == "Rotate":
            ttk.Label(self.params_frame, text="Angle:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=2)
            ttk.Entry(self.params_frame, textvariable=self.angle_var, width=10).grid(row=row, column=1, padx=5, pady=2)
            ttk.Checkbutton(self.params_frame, text="Expand canvas",
                            variable=self.expand_var).grid(row=row, column=2, columnspan=2, sticky=tk.W, padx=5, pady=2)

        elif operation == "Flip":
            ttk.Label(self.params_frame, text="Direction:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=2)
            direction_combo = ttk.Combobox(self.params_frame, textvariable=self.direction_var, width=12,
                                           values=["horizontal", "vertical"], state="readonly")
            direction_combo.grid(row=row, column=1, padx=5, pady=2)
            direction_combo.set("horizontal")

        elif operation == "Watermark":
            ttk.Label(self.params_frame, text="Text:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=2)
            ttk.Entry(self.params_frame, textvariable=self.watermark_text_var, width=20).grid(row=row, column=1,
                                                                                              columnspan=2, padx=5,
                                                                                              pady=2)
            row += 1
            ttk.Label(self.params_frame, text="Position:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=2)
            pos_combo = ttk.Combobox(self.params_frame, textvariable=self.watermark_pos_var, width=12,
                                     values=["top-left", "top-right", "bottom-left", "bottom-right", "center"],
                                     state="readonly")
            pos_combo.grid(row=row, column=1, padx=5, pady=2)
            pos_combo.set("bottom-right")
            ttk.Label(self.params_frame, text="Opacity:").grid(row=row, column=2, sticky=tk.W, padx=5, pady=2)
            ttk.Entry(self.params_frame, textvariable=self.opacity_var, width=8).grid(row=row, column=3, padx=5, pady=2)

        elif operation == "Border":
            ttk.Label(self.params_frame, text="Width:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=2)
            ttk.Entry(self.params_frame, textvariable=self.border_width_var, width=8).grid(row=row, column=1, padx=5,
                                                                                           pady=2)
            ttk.Label(self.params_frame, text="Color:").grid(row=row, column=2, sticky=tk.W, padx=5, pady=2)
            color_combo = ttk.Combobox(self.params_frame, textvariable=self.border_color_var, width=10,
                                       values=["black", "white", "red", "green", "blue"], state="readonly")
            color_combo.grid(row=row, column=3, padx=5, pady=2)
            color_combo.set("black")

        elif operation == "Vignette":
            ttk.Label(self.params_frame, text="Strength:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=2)
            ttk.Entry(self.params_frame, textvariable=self.vignette_strength_var, width=8).grid(row=row, column=1,
                                                                                                padx=5, pady=2)
            ttk.Label(self.params_frame, text="(0.0 - 1.0)").grid(row=row, column=2, sticky=tk.W, padx=5, pady=2)

        elif operation in ["Sepia", "Grayscale", "Invert", "Posterize", "Solarize"]:
            ttk.Label(self.params_frame, text="Effect Type:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=2)
            effect_combo = ttk.Combobox(self.params_frame, textvariable=self.effect_type_var, width=12,
                                        values=["sepia", "grayscale", "invert", "posterize", "solarize"],
                                        state="readonly")
            effect_combo.grid(row=row, column=1, padx=5, pady=2)
            effect_combo.set(operation.lower())

        elif operation == "Thumbnail":
            ttk.Label(self.params_frame, text="Size:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=2)
            ttk.Entry(self.params_frame, textvariable=self.thumb_size_var, width=12).grid(row=row, column=1, padx=5,
                                                                                          pady=2)
            ttk.Label(self.params_frame, text="(e.g., 128,128)").grid(row=row, column=2, sticky=tk.W, padx=5, pady=2)

    def process_image(self):
        """Process the image based on selected operation and parameters"""
        input_file = self.input_var.get()
        output_file = self.output_var.get()
        operation = self.operation_var.get()

        if not input_file or not output_file:
            self.status_var.set("Please select input and output files")
            return

        try:
            if operation == "Resize":
                width = int(self.width_var.get()) if self.width_var.get() else None
                height = int(self.height_var.get()) if self.height_var.get() else None
                maintain_aspect = self.maintain_aspect_var.get()
                self.cli.resize_image(input_file, output_file, width=width, height=height,
                                      maintain_aspect=maintain_aspect)

            elif operation in ["Blur", "Sharpen", "Edge Enhance", "Emboss", "Find Edges", "Smooth", "Contour",
                               "Detail"]:
                filter_type = self.filter_type_var.get()
                self.cli.apply_filters(input_file, output_file, filter_type)

            elif operation == "Adjust":
                brightness = float(self.brightness_var.get()) if self.brightness_var.get() else 1.0
                contrast = float(self.contrast_var.get()) if self.contrast_var.get() else 1.0
                saturation = float(self.saturation_var.get()) if self.saturation_var.get() else 1.0
                sharpness = float(self.sharpness_var.get()) if self.sharpness_var.get() else 1.0
                self.cli.adjust_image(input_file, output_file, brightness, contrast, saturation, sharpness)

            elif operation == "Crop":
                x = int(self.crop_x_var.get()) if self.crop_x_var.get() else 0
                y = int(self.crop_y_var.get()) if self.crop_y_var.get() else 0
                width = int(self.crop_width_var.get()) if self.crop_width_var.get() else 100
                height = int(self.crop_height_var.get()) if self.crop_height_var.get() else 100
                self.cli.crop_image(input_file, output_file, x, y, width, height)

            elif operation == "Rotate":
                angle = float(self.angle_var.get()) if self.angle_var.get() else 0
                expand = self.expand_var.get()
                self.cli.rotate_image(input_file, output_file, angle, expand)

            elif operation == "Flip":
                direction = self.direction_var.get()
                self.cli.flip_image(input_file, output_file, direction)

            elif operation == "Watermark":
                text = self.watermark_text_var.get()
                position = self.watermark_pos_var.get()
                opacity = int(self.opacity_var.get()) if self.opacity_var.get() else 128
                self.cli.add_watermark(input_file, output_file, text, position, opacity)

            elif operation == "Border":
                width = int(self.border_width_var.get()) if self.border_width_var.get() else 10
                color = self.border_color_var.get()
                self.cli.create_border(input_file, output_file, width, color)

            elif operation == "Vignette":
                strength = float(self.vignette_strength_var.get()) if self.vignette_strength_var.get() else 0.5
                self.cli.apply_vignette(input_file, output_file, strength)

            elif operation in ["Sepia", "Grayscale", "Invert", "Posterize", "Solarize"]:
                effect = self.effect_type_var.get()
                self.cli.apply_artistic_effects(input_file, output_file, effect)

            elif operation == "Thumbnail":
                size_str = self.thumb_size_var.get() or "128,128"
                size = tuple(map(int, size_str.split(',')))
                self.cli.create_thumbnail(input_file, output_file, size)

            self.status_var.set(f"Success! Processed image saved to {output_file}")
            messagebox.showinfo("Success", f"Image processed successfully!\nSaved to: {output_file}")
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
        self.root.geometry("800x700")
        self.root.resizable(True, True)

        # Initialize variables
        self.initialize_variables()

        # Create main frame with scrollable canvas
        main_canvas = tk.Canvas(self.root)
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=main_canvas.yview)
        scrollable_frame = ttk.Frame(main_canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all"))
        )

        main_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        main_canvas.configure(yscrollcommand=scrollbar.set)

        main_frame = ttk.Frame(scrollable_frame, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Input file selection
        ttk.Label(main_frame, text="Input Image:").pack(anchor=tk.W, pady=5)
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=5)
        ttk.Entry(input_frame, textvariable=self.input_var, width=50).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(input_frame, text="Browse", command=self.browse_input).pack(side=tk.RIGHT, padx=(5, 0))

        # Output file selection
        ttk.Label(main_frame, text="Output Image:").pack(anchor=tk.W, pady=5)
        output_frame = ttk.Frame(main_frame)
        output_frame.pack(fill=tk.X, pady=5)
        ttk.Entry(output_frame, textvariable=self.output_var, width=50).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(output_frame, text="Browse", command=self.browse_output).pack(side=tk.RIGHT, padx=(5, 0))

        # Operation selection
        ttk.Label(main_frame, text="Operation:").pack(anchor=tk.W, pady=5)
        operation_combo = ttk.Combobox(main_frame, textvariable=self.operation_var, width=20,
                                       values=["Resize", "Blur", "Sharpen", "Edge Enhance", "Emboss", "Find Edges",
                                               "Smooth", "Contour", "Detail", "Adjust", "Crop", "Rotate", "Flip",
                                               "Watermark", "Border", "Vignette", "Sepia", "Grayscale", "Invert",
                                               "Posterize", "Solarize", "Thumbnail"],
                                       state="readonly")
        operation_combo.pack(fill=tk.X, pady=5)
        operation_combo.bind('<<ComboboxSelected>>', self.on_operation_change)

        # Parameters frame
        self.params_frame = ttk.LabelFrame(main_frame, text="Parameters", padding="10")
        self.params_frame.pack(fill=tk.X, pady=10)

        # Process button
        ttk.Button(main_frame, text="Process Image", command=self.process_image).pack(pady=20)

        # Status
        ttk.Label(main_frame, text="Status:").pack(anchor=tk.W, pady=5)
        status_label = ttk.Label(main_frame, textvariable=self.status_var, foreground="blue")
        status_label.pack(anchor=tk.W, pady=5)

        # Pack canvas and scrollbar
        main_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Initialize with default operation
        self.on_operation_change()

        self.root.mainloop()


def launch_gui(cli_instance):
    """Convenience function to launch the GUI"""
    gui = PillowGUI(cli_instance)
    gui.launch()
