import time
from typing import Callable, Optional
import flet as ft
from loguru import logger
import asyncio

from app.frontend.theme import AppSpacing, AppTypography
from app.frontend.ui_components import UIComponents
from app.models.models import BookSchema

class BookForm:
    """
    A class to manage the Book form UI, validation, and data collection.
    This handles the creation and display of a book form dialog,
    as well as collecting and validating user input.
    """

    def __init__(
        self,
        page: ft.Page,
        ui_builder: UIComponents,
        on_save_callback: Callable[[BookSchema], None],
        book_to_edit: Optional[BookSchema] = None
    ) -> None:
        self.page = page
        self.ui_builder = ui_builder
        self.on_save_callback = on_save_callback
        self.book_to_edit = book_to_edit
        self.dialog = None
        
        self.title_field = None
        self.author_field = None
        self.year_published_field = None
        self.year_read_field = None
        self.cover_image_field = None
        self.summary_field = None
        self.rating_field = None
        self.genres_field = None

    def create_form(self) -> ft.Column:
        """
        Create all form fields and layout for the book form.
        If editing an existing book, pre-fill the fields with the book's data.
        """
        # Create input fields for the book form
        self.title_field = self.ui_builder.create_input_field(
            label="Title",
            hint_text="Enter book title",
            width=400,
            value=self.book_to_edit.title if self.book_to_edit else ""
        )
        
        self.author_field = self.ui_builder.create_input_field(
            label="Author",
            hint_text="Enter author's name",
            width=400,
            value=self.book_to_edit.author if self.book_to_edit else ""
        )
        
        self.year_published_field = self.ui_builder.create_input_field(
            label="Year Published",
            hint_text="Enter publication year",
            width=190,
            value=str(self.book_to_edit.year_published) if self.book_to_edit and self.book_to_edit.year_published else ""
        )
        
        self.year_read_field = self.ui_builder.create_input_field(
            label="Year Read",
            hint_text="Enter year you read it",
            width=190,
            value=str(self.book_to_edit.year_read) if self.book_to_edit and self.book_to_edit.year_read else ""
        )
        
        self.cover_image_field = self.ui_builder.create_input_field(
            label="Cover Image Path",
            hint_text="Enter path to cover image",
            width=400,
            value=self.book_to_edit.cover_image_path if self.book_to_edit else ""
        )
        
        self.summary_field = self.ui_builder.create_input_field(
            label="Summary",
            hint_text="Write a summary of the book",
            width=400,
            multiline=True,
            min_lines=3,
            max_lines=5,
            value=self.book_to_edit.summary if self.book_to_edit and self.book_to_edit.summary else ""
        )
        
        self.rating_field = self.ui_builder.create_input_field(
            label="Rating (1-5)",
            hint_text="Rate the book from 1 to 5",
            width=190,
            value=str(self.book_to_edit.rating) if self.book_to_edit and self.book_to_edit.rating else ""
        )
        
        # Join the genres list into a comma-separated string if editing a book
        genres_value = ""
        if self.book_to_edit and self.book_to_edit.genres:
            genres_value = ", ".join(self.book_to_edit.genres)
            
        self.genres_field = self.ui_builder.create_input_field(
            label="Genres",
            hint_text="Enter genres, separated by commas",
            width=400,
            value=genres_value
        )
        
        # Create form layout
        form_layout = ft.Column(
            controls=[
                ft.Text("Book Information", size=AppTypography.SUBHEADER_SIZE, weight=ft.FontWeight.BOLD),
                self.title_field,
                self.author_field,
                ft.Row([self.year_published_field, self.year_read_field], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                self.cover_image_field,
                self.summary_field,
                ft.Row([self.rating_field], alignment=ft.MainAxisAlignment.START),
                self.genres_field,
            ],
            spacing=AppSpacing.SMALL,
            width=400,
        )
        
        return form_layout
    
    def validate_form(self) -> tuple[bool, str]:
        """
        Validates the form inputs.
        """
        # Check required fields
        if not self.title_field.value or not self.title_field.value.strip():
            return False, "Title is required"
        
        if not self.author_field.value or not self.author_field.value.strip():
            return False, "Author is required"
        
        # Validate years (if provided) are valid integers
        if self.year_published_field.value:
            try:
                year_published = int(self.year_published_field.value)
                # Simple range check - books weren't printed before 1450 (Gutenberg press)
                # and can't be published in the future
                current_year = 2025  # You could import datetime and use datetime.now().year
                if year_published < 1450 or year_published > current_year:
                    return False, f"Publication year must be between 1450 and {current_year}"
            except ValueError:
                return False, "Publication year must be a valid number"
        
        if self.year_read_field.value:
            try:
                year_read = int(self.year_read_field.value)
                current_year = 2025
                if year_read < 1900 or year_read > current_year:
                    return False, f"Year read must be between 1900 and {current_year}"
            except ValueError:
                return False, "Year read must be a valid number"
        
        # Validate rating is between 1-5 if provided
        if self.rating_field.value:
            try:
                rating = int(self.rating_field.value)
                if rating < 1 or rating > 5:
                    return False, "Rating must be between 1 and 5"
            except ValueError:
                return False, "Rating must be a valid number"
        
        # If we get here, all validations passed
        logger.info(f"VALIDATE FORM: TRUE")
        return True, ""
    
    def collect_form_data(self) -> Optional[BookSchema]:
        """
        Collect data from the form and create a Book object.
        Validation should be done before calling this method.
        
        Returns:
            Optional[Book]: A Book object if successful, None if there was an error
        """
        try:
            # Process genres (split by comma)
            genres = []
            if self.genres_field.value:
                genres = [g.strip() for g in self.genres_field.value.split(",") if g.strip()]
            
            # Convert numeric fields, handling empty inputs
            year_published = None
            if self.year_published_field.value:
                year_published = int(self.year_published_field.value)
                
            year_read = None
            if self.year_read_field.value:
                year_read = int(self.year_read_field.value)
                
            rating = None
            if self.rating_field.value:
                rating = int(self.rating_field.value)
            
            # Create book kwargs dict
            book_data = {
                "title": self.title_field.value.strip(),
                "author": self.author_field.value.strip(),
                "year_published": year_published,
                "year_read": year_read,
                "cover_image_path": self.cover_image_field.value.strip(),
                "summary": self.summary_field.value.strip() if self.summary_field.value else None,
                "rating": rating,
                "genres": genres,
                "cover_image": None,  # This would be handled separately
                "is_remote_image": False
            }
            # Only include ID if editing an existing book
            if self.book_to_edit:
                book_data["id"] = self.book_to_edit.id
            
            # Create the Book object
            book = BookSchema(**book_data)
            
            return book
        except Exception as e:
            logger.error(f"Error creating book: {str(e)}")
            return None
    
    async def handle_save_click(self, e: ft.ControlEvent) -> None:
        """Handle the Save button click"""
        # First validate the form
        is_valid, error_message = self.validate_form()
        
        if not is_valid:
            # Show error message
            self.snack_bar = ft.SnackBar(
                content=ft.Text(error_message),
                action="OK",
            )
            self.page.add(self.snack_bar)
            self.snack_bar.open = True
            self.page.update()
            return
        
        # If valid, collect the data
        book = self.collect_form_data()
        
        if book:
            # Close the dialog
            await self.close_dialog()
            
            # Call the callback with the book
            await asyncio.sleep(0.3)
            await self.on_save_callback(book)
            
            # No page update here - callback will handle it
            logger.info(f"HANDLE SAVE CLICK WORKED AND AD IS CLOSED")
        else:
            # Show generic error if book creation failed
            self.snack_bar = ft.SnackBar(
                content=ft.Text("Error creating book. Please check your inputs."),
                action="OK",
            )
            self.page.add(self.snack_bar)
            self.snack_bar.open = True
            self.page.update()
        
    def show_dialog(self):
        """
        Create and show the book form dialog.
        This method creates the form, sets up the dialog and displays it.
        """
        # Create the form layout
        form_layout = self.create_form()
        
        # Determine title based on whether we're editing or creating
        dialog_title = "Edit Book" if self.book_to_edit else "Add New Book"
        
        # Create the dialog
        self.dialog = ft.AlertDialog(
            modal=False,  # Allows clicking outside to dismiss
            title=ft.Text(dialog_title),
            content=ft.Container(
                content=form_layout,
                padding=10,
            ),
            actions=[
                ft.TextButton("Cancel", on_click=self.close_dialog),
                ft.TextButton("Save", on_click=self.handle_save_click),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            open=True,
            scrollable=True,
            on_dismiss=lambda e: logger.info("Modal dialog dismissed!"),
        )
        
        self.page.open(self.dialog)
        self.page.update()
    
    async def close_dialog(self, e=None):
        """Close the dialog"""
        if self.dialog:
            # Close the alert dialog
            self.page.close(self.dialog)
            # Update overlay
            self.page.update()
            # Small delay to ensure close animation completes
            await asyncio.sleep(0.3)