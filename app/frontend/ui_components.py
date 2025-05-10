import os
from typing import Any, Callable, Dict, List, Optional

import flet as ft
from loguru import logger

from app.frontend.theme import AppColors, AppTypography, AppSpacing  # Import your theme classes

class UIComponents:
    """A collection of static methods for creating UI components in Flet applications."""
    def __init__(self, page: ft.Page = None):
        self.page = page
        
    @staticmethod
    def create_button(
        text: str,
        on_click: Callable[[ft.ControlEvent], Any],
        width: Optional[int] = 300,
        visible: bool = True,
        disabled: bool = False,
        adaptive: Optional[bool] = False,
        bgcolor: str = AppColors.PRIMARY,
        color: str = AppColors.CARD_BACKGROUND,
        text_size: int = AppTypography.BODY_SIZE,
        **kwargs
    ) -> ft.ElevatedButton:
        """
        Creates a button with specified text and click handler.

        Args:
            text: Text displayed on the button
            on_click: Function called when button is clicked
            width: Button width
            visible: Whether button is visible
            disabled: Whether button is disabled
            adaptive: Whether button should adapt to available space
            bgcolor: Background color
            color: Text color
            text_size: Font size for the button text
            **kwargs: Additional parameters for the button

        Returns:
            An ElevatedButton instance
        """
        return ft.ElevatedButton(
            width=width,
            text=text,
            on_click=on_click,
            visible=visible,
            disabled=disabled,
            bgcolor=bgcolor,
            color=color,
            adaptive=adaptive,
            content=ft.Row(
                [ft.Text(text)],
                alignment=ft.MainAxisAlignment.CENTER
            ),
            style=ft.ButtonStyle(text_style=ft.TextStyle(size=text_size)),
            **kwargs
        )

    @staticmethod
    def create_pop_up_window(
        dialog_name: str = "",
        text: str = "",
        close_text: str = "Close",
        on_close: Optional[Callable[[ft.ControlEvent], None]] = None,
        **kwargs
    ) -> ft.AlertDialog:
        """
        Creates a popup window with title, text and close button.

        Args:
            dialog_name: Dialog title
            text: Dialog content text
            close_text: Text on close button
            on_close: Function called when close button is clicked
            **kwargs: Additional parameters for the dialog

        Returns:
            An AlertDialog instance
        """
        return ft.AlertDialog(
            title=ft.Text(dialog_name),
            content=ft.Text(text, size=AppTypography.BODY_SIZE),
            actions=[
                ft.TextButton(
                    text=close_text,
                    on_click=on_close,
                ),
            ],
            **kwargs
        )

    @staticmethod
    def create_text_from_file(file_path: str, default_size: int = AppTypography.BODY_SIZE) -> Optional[ft.Column]:
        """
        Reads text from a file, adds formatting, and returns a list of text elements.

        Args:
            file_path: Path to the text file
            default_size: Default font size for text elements

        Returns:
            A Column containing formatted Text controls or None if file not found
        """
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                file_content = file.read()

            lines = file_content.split("\n")
            elements: List[ft.Text] = []

            for i, line in enumerate(lines):
                stripped_line = line.strip()

                if i == 0:
                    text_element = ft.Text(
                        line,
                        size=default_size,
                        weight=ft.FontWeight.BOLD,
                    )
                elif (
                    stripped_line and
                    stripped_line[0].isdigit() and
                    stripped_line[1] == "."
                ):
                    text_element = ft.Text(
                        line,
                        size=default_size - 2,
                        weight=ft.FontWeight.BOLD,
                    )
                else:
                    text_element = ft.Text(line, size=default_size)

                elements.append(text_element)
            return ft.Column(elements, alignment=ft.MainAxisAlignment.START)
        except FileNotFoundError:
            logger.error(f"Error: File {file_path} not found.")
            return ft.Column([], alignment=ft.MainAxisAlignment.START)
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            return ft.Column([], alignment=ft.MainAxisAlignment.START)

    @staticmethod
    def create_input_field(
        label: str,
        value: str = "",
        password: bool = False,
        width: int = 300,
        hint_text: str = "", 
        max_length: Optional[int] = None,
        multiline: bool = False, 
        visible: bool = True,
        read_only: bool = False, 
        min_lines: Optional[int] = None,
        max_lines: Optional[int] = None, 
        add_eye_icon: bool = False,
        **kwargs
    ) -> ft.TextField:
        """
        Creates a text input field with optional password visibility toggle.

        Args:
            label: Label text for the input field
            value: Initial value
            password: Whether to hide the text as a password
            width: Width of the field
            hint_text: Placeholder text shown when field is empty
            max_length: Maximum number of characters
            multiline: Whether field supports multiple lines
            visible: Whether field is visible
            read_only: Whether field is editable
            min_lines: Minimum number of lines for multiline fields
            max_lines: Maximum number of lines for multiline fields
            add_eye_icon: Whether to add password visibility toggle icon
            **kwargs: Additional parameters for the text field

        Returns:
            A TextField instance
        """
        text_field = ft.TextField(
            label=label, 
            value=value, 
            password=password, 
            width=width,
            hint_text=hint_text, 
            max_length=max_length, 
            multiline=multiline,
            visible=visible, 
            read_only=read_only, 
            min_lines=min_lines,
            max_lines=max_lines,
            **kwargs
        )

        if add_eye_icon:
            password_visible = False
            eye_button = ft.IconButton(
                icon=ft.icons.VISIBILITY if not password_visible else ft.icons.VISIBILITY_OFF,
                on_click=lambda e: UIComponents._toggle_password_visibility(text_field, eye_button),
            )
            text_field.suffix = eye_button

        return text_field
    
    @staticmethod
    def _toggle_password_visibility(text_field: ft.TextField, eye_button: ft.IconButton) -> None:
        """Helper method to toggle password visibility"""
        # Toggle password visibility state
        text_field.password = not text_field.password
        # Toggle icon
        eye_button.icon = ft.icons.VISIBILITY if text_field.password else ft.icons.VISIBILITY_OFF
        # Request update (needs page instance, should be handled by parent)

    @staticmethod
    def create_text_field(
            value: Optional[str] = None,
            color: Optional[str] = None,
            visible: Optional[bool] = None,
            width: Optional[float] = None,
            height: Optional[float] = None,
            text_size: Optional[int] = None,
            no_wrap: Optional[bool] = False,
            overflow: Optional[ft.TextOverflow]="visible",
            max_lines: Optional[int] = None,
            expand: bool = False,
            **kwargs
    ) -> ft.Text:
        """
        Creates a text element with specified properties.

        Args:
            value: Text to display
            color: Text color
            visible: Whether text is visible
            width: Width of text element
            height: Height of text element
            text_size: Font size
            expand: Whether text should expand to fill space
            **kwargs: Additional parameters for the text

        Returns:
            A Text instance
        """
        text_size = text_size if text_size is not None else AppTypography.BODY_SIZE

        return ft.Text(
            value=value,
            color=color,
            visible=visible,
            height=height,
            width=width,
            expand=expand,
            no_wrap=no_wrap,
            overflow=overflow,
            max_lines=max_lines,
            size=text_size,
            **kwargs
        )

    @staticmethod
    def create_radio_buttons(
        labels: list[dict[str, str]],
        on_change: Optional[Callable[[ft.ControlEvent], None]] = None,
        **kwargs
    ) -> ft.RadioGroup:
        """
        Creates a radio button group.

        Args:
            labels: List of dictionaries with labels
            on_change: Function called when selection changes
            **kwargs: Additional parameters for the radio group

        Returns:
            A RadioGroup instance
        """
        return ft.RadioGroup(
            content=ft.Row(
                [
                    ft.Radio(
                        value=label["label"],
                        label=label["label"],
                    )
                    for label in labels
                ],
            ),
            on_change=on_change,
            **kwargs
        )

    @staticmethod
    def create_checkbox(
        label: str,
        value: bool = False,
        on_change: Optional[Callable[[ft.ControlEvent], None]] = None,
        **kwargs
    ) -> ft.Checkbox:
        """
        Creates a checkbox with label.

        Args:
            label: Text shown next to checkbox
            value: Initial state (checked or not)
            on_change: Function called when state changes
            **kwargs: Additional parameters for the checkbox

        Returns:
            A Checkbox instance
        """
        return ft.Checkbox(
            label=label, 
            value=value, 
            on_change=on_change,
            **kwargs
        )

    @staticmethod
    def create_progress_ring(
        width: int = 40,
        height: int = 40,
        stroke_width: int = 4,
        visible: bool = False,
        **kwargs
    ) -> ft.ProgressRing:
        """
        Creates a spinning ring progress indicator.

        Args:
            width: Width of the indicator
            height: Height of the indicator
            stroke_width: Thickness of the ring
            visible: Whether indicator is visible
            **kwargs: Additional parameters for the progress ring

        Returns:
            A ProgressRing instance
        """
        return ft.ProgressRing(
            width=width,
            height=height,
            stroke_width=stroke_width,
            visible=visible,
            **kwargs
        )

    @staticmethod
    def create_progress_bar(
        width: int = 300,
        value: float = 0,
        visible: bool = False,
        **kwargs
    ) -> ft.ProgressBar:
        """
        Creates a horizontal progress bar.

        Args:
            width: Width of the progress bar
            value: Initial progress value (0-1)
            visible: Whether progress bar is visible
            **kwargs: Additional parameters for the progress bar

        Returns:
            A ProgressBar instance
        """
        return ft.ProgressBar(
            width=width, 
            value=value, 
            visible=visible,
            **kwargs
        )
        
    @staticmethod
    def create_card(
        content,
        width: Optional[int] = None,
        height: Optional[int] = None,
        padding: int = AppSpacing.MEDIUM,
        margin: int = AppSpacing.SMALL,
        **kwargs
    ) -> ft.Container:
        """
        Creates a card container with shadow effect.

        Args:
            content: Content to display inside the card
            width: Card width
            height: Card height
            padding: Internal padding
            margin: External margin
            **kwargs: Additional parameters for the container

        Returns:
            A Container instance styled as a card
        """
        return ft.Container(
            content=content,
            width=width,
            height=height,
            bgcolor=AppColors.CARD_BACKGROUND,
            border_radius=10,
            padding=padding,
            margin=margin,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=15,
                color=ft.colors.with_opacity(0.15, "000000"),
                offset=ft.Offset(0, 4),
            ),
            **kwargs
        )
        
    @staticmethod
    def create_divider(
        height: int = 1, 
        color: Optional[str] = None,
        **kwargs
    ) -> ft.Divider:
        """
        Creates a horizontal divider line.

        Args:
            height: Divider thickness
            color: Divider color
            **kwargs: Additional parameters for the divider

        Returns:
            A Divider instance
        """
        if color is None:
            color = ft.colors.with_opacity(0.2, AppColors.TEXT_SECONDARY)
            
        return ft.Divider(
            height=height,
            color=color,
            **kwargs
        )
    
    def add_elements_to_page(
        self, 
        *elements: Any, 
        horizontal_alignment: ft.MainAxisAlignment = ft.MainAxisAlignment.CENTER,
        vertical_alignment: ft.CrossAxisAlignment = ft.CrossAxisAlignment.CENTER
    ) -> None:
        """Adds UI elements to the page with customizable alignment"""
        column_content = ft.Column(
            controls=[],
            alignment=horizontal_alignment,
        )
        
        for element in elements:
            if isinstance(element, list):
                row = ft.Row(element, alignment=horizontal_alignment)
                column_content.controls.append(row)
            else:
                row = ft.Row([element], alignment=horizontal_alignment)
                column_content.controls.append(row)
                
        self.page.add(column_content)
        self.page.update()
        
    @staticmethod
    def truncate_text(text: str, max_length: int = 20) -> str:
        """
        Truncates text to the specified maximum length and adds ellipsis if needed.
        """
        if len(text) <= max_length:
            return text
        return text[:max_length - 3] + "..."