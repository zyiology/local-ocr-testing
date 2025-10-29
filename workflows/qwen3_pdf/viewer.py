"""
OCR Results Viewer GUI

A simple tkinter-based GUI for browsing through OCR results folders.
Displays images and their corresponding OCR text side-by-side with keyboard navigation.
"""

import tkinter as tk
from tkinter import scrolledtext
from pathlib import Path
from typing import List
from PIL import Image, ImageTk
import argparse
import sys


class OCRViewer:
    """GUI viewer for browsing OCR results folders."""

    def __init__(self, output_dir: Path):
        """
        Initialize the OCR viewer.

        Args:
            output_dir: Path to the directory containing OCR result folders
        """
        self.output_dir = output_dir
        self.folders = self._get_valid_folders()
        self.current_index = 0

        if not self.folders:
            raise ValueError(f"No valid folders found in {output_dir}")

        # Initialize tkinter
        self.root = tk.Tk()
        self.root.title("OCR Results Viewer")
        self.root.geometry("1400x800")

        # Store current image reference to prevent garbage collection
        self.current_image = None

        self._create_gui()
        self._bind_keys()
        self._load_current_folder()

    def _get_valid_folders(self) -> List[Path]:
        """
        Recursively scan output directory and return sorted list of valid folders.

        Returns:
            List of folder paths that contain both image0.png and image0.txt
        """
        folders = []
        for folder in sorted(self.output_dir.rglob("*")):
            if folder.is_dir():
                image_file = folder / "image0.png"
                text_file = folder / "image0.txt"
                if image_file.exists() and text_file.exists():
                    folders.append(folder)
        return folders

    def _create_gui(self) -> None:
        """Create the GUI layout."""
        # Title bar
        self.title_label = tk.Label(
            self.root,
            text="",
            font=("Arial", 12, "bold"),
            bg="#2c3e50",
            fg="white",
            pady=10,
        )
        self.title_label.pack(fill=tk.X)

        # Main content frame
        content_frame = tk.Frame(self.root)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Left panel - Image
        left_frame = tk.Frame(content_frame, relief=tk.SUNKEN, borderwidth=2)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

        image_label = tk.Label(left_frame, text="Image", font=("Arial", 10, "bold"))
        image_label.pack()

        self.image_canvas = tk.Canvas(left_frame, bg="white")
        self.image_canvas.pack(fill=tk.BOTH, expand=True)

        # Right panel - Text
        right_frame = tk.Frame(content_frame, relief=tk.SUNKEN, borderwidth=2)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))

        text_label = tk.Label(right_frame, text="OCR Text", font=("Arial", 10, "bold"))
        text_label.pack()

        self.text_widget = scrolledtext.ScrolledText(
            right_frame, wrap=tk.WORD, font=("Courier", 10)
        )
        self.text_widget.pack(fill=tk.BOTH, expand=True)

        # Status bar
        self.status_label = tk.Label(
            self.root,
            text="Use ← → arrow keys (or A/D) to navigate | Home/End to jump | Q to quit",
            font=("Arial", 9),
            bg="#34495e",
            fg="white",
            pady=5,
        )
        self.status_label.pack(fill=tk.X)

    def _bind_keys(self) -> None:
        """Bind keyboard shortcuts."""
        self.root.bind("<Left>", lambda e: self._navigate(-1))
        self.root.bind("<Right>", lambda e: self._navigate(1))
        self.root.bind("<a>", lambda e: self._navigate(-1))
        self.root.bind("<d>", lambda e: self._navigate(1))
        self.root.bind("<A>", lambda e: self._navigate(-1))
        self.root.bind("<D>", lambda e: self._navigate(1))
        self.root.bind("<Home>", lambda e: self._jump_to(0))
        self.root.bind("<End>", lambda e: self._jump_to(len(self.folders) - 1))
        self.root.bind("<q>", lambda e: self.root.quit())
        self.root.bind("<Q>", lambda e: self.root.quit())

    def _navigate(self, direction: int) -> None:
        """
        Navigate to next or previous folder.

        Args:
            direction: -1 for previous, 1 for next
        """
        new_index = self.current_index + direction

        # Wrap around at boundaries
        if new_index < 0:
            new_index = len(self.folders) - 1
        elif new_index >= len(self.folders):
            new_index = 0

        self.current_index = new_index
        self._load_current_folder()

    def _jump_to(self, index: int) -> None:
        """
        Jump to specific folder index.

        Args:
            index: Folder index to jump to
        """
        self.current_index = index
        self._load_current_folder()

    def _load_current_folder(self) -> None:
        """Load and display the current folder's image and text."""
        folder = self.folders[self.current_index]
        folder_name = folder.relative_to(self.output_dir)

        # Update title
        title = f"Folder {self.current_index + 1}/{len(self.folders)}: {folder_name}"
        self.title_label.config(text=title)

        # Load and display image
        self._load_image(folder / "image0.png")

        # Load and display text
        self._load_text(folder / "image0.txt")

    def _load_image(self, image_path: Path) -> None:
        """
        Load and display image, scaled to fit canvas.

        Args:
            image_path: Path to the image file
        """
        canvas_width = self.image_canvas.winfo_width()
        canvas_height = self.image_canvas.winfo_height()

        try:
            # Open image
            image = Image.open(image_path)

            # Get canvas dimensions
            self.root.update()  # Ensure canvas size is updated

            # Calculate scaling to fit canvas while maintaining aspect ratio
            if canvas_width > 1 and canvas_height > 1:  # Valid dimensions
                image_width, image_height = image.size
                scale_width = canvas_width / image_width
                scale_height = canvas_height / image_height
                scale = min(scale_width, scale_height, 1.0)  # Don't upscale

                new_width = int(image_width * scale)
                new_height = int(image_height * scale)

                image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)

            # Convert to PhotoImage
            self.current_image = ImageTk.PhotoImage(image)

            # Clear canvas and display image
            self.image_canvas.delete("all")
            self.image_canvas.create_image(
                canvas_width // 2,
                canvas_height // 2,
                image=self.current_image,
                anchor=tk.CENTER,
            )

        except Exception as e:
            # Display error message on canvas
            self.image_canvas.delete("all")
            self.image_canvas.create_text(
                canvas_width // 2,
                canvas_height // 2,
                text=f"Error loading image:\n{str(e)}",
                fill="red",
                font=("Arial", 12),
            )

    def _load_text(self, text_path: Path) -> None:
        """
        Load and display OCR text.

        Args:
            text_path: Path to the text file
        """
        try:
            # Read text file
            text_content = text_path.read_text(encoding="utf-8")

            # Clear and update text widget
            self.text_widget.delete(1.0, tk.END)
            self.text_widget.insert(1.0, text_content)

        except Exception as e:
            # Display error message
            self.text_widget.delete(1.0, tk.END)
            self.text_widget.insert(1.0, f"Error loading text:\n{str(e)}")

    def run(self) -> None:
        """Start the GUI event loop."""
        self.root.mainloop()


def main() -> None:
    """Main entry point for the viewer."""
    parser = argparse.ArgumentParser(
        description="View OCR results from batch PDF processing"
    )
    parser.add_argument(
        "output_dir",
        type=Path,
        nargs="?",  # Make it optional
        default=None,
        help="Path to the output directory containing OCR results",
    )
    parser.add_argument(
        "--default",
        action="store_true",
        help="Use default path (../../data/output/)",
    )

    args = parser.parse_args()

    # Determine output directory
    if args.output_dir:
        output_dir = args.output_dir.resolve()
    else:
        # Default to ../../data/output relative to this script
        script_dir = Path(__file__).parent
        output_dir = (script_dir / "../../data/output").resolve()

    # Check if directory exists
    if not output_dir.exists():
        print(f"Error: Output directory not found: {output_dir}")
        print("\nPlease ensure you've run pdf_workflow.py first to generate results.")
        print("\nUsage:")
        print(f"  python viewer.py                    # Use default: {output_dir}")
        print("  python viewer.py <path>             # Use custom path")
        print("  python viewer.py --help             # Show help")
        sys.exit(1)

    # Check if directory has any valid folders (search recursively)
    valid_folders = []
    for folder in output_dir.rglob("*"):
        if folder.is_dir():
            if (folder / "image0.png").exists() and (folder / "image0.txt").exists():
                valid_folders.append(folder)

    if not valid_folders:
        print(f"Error: No valid OCR result folders found in: {output_dir}")
        print("\nValid folders should contain both 'image0.png' and 'image0.txt'")
        print("Please run pdf_workflow.py first to generate results.")
        sys.exit(1)

    print(f"Loading OCR results from: {output_dir}")
    print(f"Found {len(valid_folders)} result folder(s)\n")

    print("Valid result folders:")
    # print out list of all result folders
    for folder in valid_folders:
        print(f"{folder.relative_to(output_dir)}")

    try:
        viewer = OCRViewer(output_dir)
        viewer.run()
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nViewer closed by user")


if __name__ == "__main__":
    main()
