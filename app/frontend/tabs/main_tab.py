import base64
import os
from typing import Callable, List, Optional
import flet as ft
from loguru import logger

from app.backend.client import BackendClient
from app.frontend.ui_components import UIComponents
from app.frontend.theme import AppColors, AppTypography, AppSpacing
from app.models.models import BookSchema

class MainTabBuilder:
    def __init__(
        self, 
        page: ft.Page,
        assets_dir: str,
        ui_builder: UIComponents,
        backend_client: BackendClient,
    ):
        self.page = page
        self.assets_dir = assets_dir
        self.ui_builder = ui_builder
        self.backend_client = backend_client
        
    def create_tab(
        self, 
        on_add_book, 
        on_edit_book):
        """Create and return the main tab layout"""
        
        # Header section (centered)
        header = self.ui_builder.create_text_field(
            value="My E-library",
            text_size=AppTypography.HEADER_SIZE,
            color=AppColors.TEXT_PRIMARY
        )
        
        description = self.ui_builder.create_text_field(
            value="This is the list of books that I was lucky (or not) to read :)",
            text_size=AppTypography.BODY_SIZE,
            color=AppColors.TEXT_SECONDARY
        )
        
        # Button (right-aligned)
        add_button = self.ui_builder.create_button(
            text="Add Book",
            on_click=on_add_book,
            bgcolor=AppColors.PRIMARY,
            color=AppColors.TEXT_PRIMARY
        )
        
        # Get books from backend
        books = self.backend_client.get_all_books()
        
        # Create book grid
        book_grid = self.create_book_grid(books, on_edit_book)
        
        # Main layout
        main_layout = ft.Column([
            # Right-aligned button 
            ft.Container(
                content=add_button,
                alignment=ft.alignment.bottom_right
            ),
            # Centered header section
            ft.Container(
                content=ft.Column([header, description], spacing=AppSpacing.SMALL),
                alignment=ft.alignment.center
            ),
            
            ft.Container(height=AppSpacing.LARGE),  # Spacer
            
            # Book grid would go here
            book_grid
        ])
        
        return main_layout

    def create_book_grid(
        self, 
        books: List[BookSchema], 
        on_edit_book: Callable
    ):
        """Create a grid of book cards"""
        if not books:
            return ft.Container(
                content=self.ui_builder.create_text_field(
                    value="No books yet. Add your first book!",
                    text_size=AppTypography.BODY_SIZE,
                    color=AppColors.TEXT_SECONDARY
                ),
                alignment=ft.alignment.center
            )
            
        book_cards = []
        
        # Create rows with 5 books per row
        # TODO: make this dynamic and adjustable to the size of the screen
        for i in range(0, len(books), 1):
            row_books = books[i:i+1]
            row = ft.Row(
                [self.create_book_card(book, on_edit_book) for book in row_books],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=AppSpacing.MEDIUM
            )
            book_cards.append(row)
        
        return ft.Column(book_cards, spacing=AppSpacing.LARGE)

    
    def create_book_card(self, book: BookSchema, on_edit_book: Callable):
        """Create a card for a single book with image display"""
        
        if book.cover_image_path and os.path.exists(book.cover_image_path):
            # If the book has a valid cover image path, use it
            img_src = f"file://{book.cover_image_path}"
        else:
            img_src = self.load_default_image()
        
        # Book cover image container (left side)
        cover_image = ft.Container(
            content=ft.Image(
                src=img_src,
                width=100,
                height=150,
                fit=ft.ImageFit.COVER,
                border_radius=ft.border_radius.all(8),
            ),
            width=120,
            height=180,
            margin=ft.margin.only(right=AppSpacing.MEDIUM),
        )
        
        # Book title
        title = self.ui_builder.create_text_field(
            value=self.ui_builder.truncate_text(book.title, max_length=40),
            text_size=AppTypography.SUBHEADER_SIZE,
            color=AppColors.TEXT_PRIMARY,
            overflow=ft.TextOverflow.ELLIPSIS,
            no_wrap=True,
        )
        
        # Author info
        author = self.ui_builder.create_text_field(
            value=f"by {book.author}",
            text_size=AppTypography.BODY_SIZE,
            color=AppColors.TEXT_SECONDARY,
        )
        
        # Publication info
        pub_info = self.ui_builder.create_text_field(
            value=self._format_publication_info(book),
            text_size=AppTypography.BODY_SIZE - 2,
            color=AppColors.TEXT_SECONDARY,
        )
            
        # Book summary 
        summary_text = self._format_book_summary(book)
        
        summary = self.ui_builder.create_text_field(
            value=summary_text,
            text_size=AppTypography.BODY_SIZE,
            color=AppColors.TEXT_PRIMARY,
            max_lines=2,
            width=600,
        )
        
        # Rating stars (top right)
        rating_stars = self._create_rating_stars(book.rating)
        
        # Genre info (under rating stars)
        genres = self.ui_builder.create_text_field(
            value=", ".join(book.genres) if book.genres else "",
            text_size=AppTypography.BODY_SIZE - 2,
            color=AppColors.TEXT_SECONDARY,
        )
        
        # Action buttons (bottom right)
        action_buttons = ft.Row([
            self.ui_builder.create_button(
                text="Edit",
                on_click=lambda e, b=book: on_edit_book(e, b),
                width=100,
                bgcolor=AppColors.SECONDARY,
                color=AppColors.TEXT_PRIMARY,
            ),
            self.ui_builder.create_button(
                text="Delete",
                on_click=lambda e, b=book: self.handle_delete_book(e, b),
                width=100,
                bgcolor=AppColors.ERROR,
                color=AppColors.TEXT_PRIMARY,
            ),
        ], 
        spacing=AppSpacing.SMALL,
        alignment=ft.MainAxisAlignment.END
        )
        
        # Create the layout with proper organization
        # First, create the top row with title and ratings/genre on opposite sides
        top_row = ft.Row([
            # Left side (title)
            ft.Column([title], expand=True),
            
            # Right side (rating and genre)
            ft.Column([
                rating_stars,
                genres
            ], horizontal_alignment=ft.CrossAxisAlignment.END)
        ])
        
        # Create the content layout
        card_content = ft.Row([
            # Left side: Book cover image
            cover_image,
            
            # Right side: Book details organized in a column
            ft.Column([
                top_row,             # Title, rating stars, and genre
                author,              # Author info
                pub_info,            # Publication info
                ft.Container(height=5),  # Small spacer
                summary,             # Book summary (first 2 lines)
                ft.Container(height=5),  # Small spacer
                action_buttons       # Buttons at the bottom
            ], 
            spacing=AppSpacing.SMALL,
            expand=True  # Make the column take up remaining width
            ),
        ])
        
        # Create and return the card with the new layout
        return self.ui_builder.create_card(
            content=card_content,
            width=800,  # Wider card to accommodate image and text
            height=None  # Let height adjust to content
        )
    
    # Helper methods for cleaner code
    def _format_publication_info(self, book: BookSchema):
        pub_info = ""
        if book.year_published:
            pub_info += f"Published: {book.year_published}"
        if book.year_read:
            if pub_info:
                pub_info += " | "
            pub_info += f"Read: {book.year_read}"
        return pub_info

    def _create_rating_stars(self, rating):
        rating_row = ft.Row([])
        if rating:
            for i in range(5):
                icon = ft.icons.STAR if i < rating else ft.icons.STAR_BORDER
                rating_row.controls.append(ft.Icon(icon, color=AppColors.ACCENT, size=18))
        return rating_row
    
    def handle_delete_book(self, e: ft.ControlEvent, book: BookSchema) -> None:
        """Handle deletion of a book"""
        def confirm_delete(e: ft.ControlEvent) -> None:
            # Delete the book
            success = self.backend_client.delete_book(book.id)
            
            # Close the dialog
            self.close_dialog()
            
            if success:
                # Show success message
                snack_bar = ft.SnackBar(
                    content=ft.Text(f"Book '{book.title}' deleted successfully!"),
                    action="OK"
                )
                self.page.add(snack_bar)
                snack_bar.open = True
                
                # Use the update_book_grid method to refresh just the grid
                self.update_book_grid(lambda e, b: self.page.app.edit_book(e, b))
            else:
                # Show error message
                snack_bar = ft.SnackBar(
                    content=ft.Text(f"Failed to delete book '{book.title}'"),
                    action="OK"
                )
                self.page.add(snack_bar)
                snack_bar.open = True
                
            self.page.update()
        
        # Create confirmation dialog
        self.confirm_dialog = ft.AlertDialog(
            title=ft.Text("Confirm Delete"),
            content=ft.Text(f"Are you sure you want to delete '{book.title}'?"),
            actions=[
                ft.TextButton("Cancel", on_click=self.close_dialog),
                ft.TextButton("Delete", on_click=confirm_delete)
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            open=True
        )
        
        # Show the dialog by adding it to the page
        self.page.add(self.confirm_dialog)
        self.page.update()
    
    def close_dialog(self, e: Optional[ft.ControlEvent] = None) -> None:
            """Close the dialog"""
            if self.confirm_dialog in self.page.controls:
                self.page.close(self.confirm_dialog)
            self.page.update()
    
    def update_book_grid(self, on_edit_book: Callable) -> ft.Column:
        """
        Update the book grid with fresh data from the backend.
        Returns the updated book grid component.
        """
        # Get fresh books data from backend
        books = self.backend_client.get_all_books()
        logger.info(f"UPDATE_BOOK_GRID: Got {len(books)} books")
        
        # Create new book grid with updated data
        updated_grid = self.create_book_grid(books, on_edit_book)
        
        # Find and replace the existing grid in the page
        for control in self.page.controls:
            if isinstance(control, ft.Column):  # Main layout is a Column
                # The book grid should be the last element in the main layout
                if len(control.controls) >= 4:  # We have at least 4 controls in the main layout
                    # Replace the book grid (last element)
                    control.controls[3] = updated_grid
                    break
        
        return updated_grid

    def load_default_image(self,):
        """
        Load the default book cover image as a base64 data URI.
        Returns a data URI string that can be used as an image source.
        """
        try:
            # Define the path to the default image
            image_path = f"{self.assets_dir}/default_book.png"
            
            # Check if the file exists
            if not os.path.exists(image_path):
                print(f"Warning: Default image not found at {image_path}")
                return ""
            
            # Load the image file and convert to base64
            with open(image_path, "rb") as img_file:
                img_data = base64.b64encode(img_file.read()).decode('utf-8')
                
            # Create and return a data URI
            return f"data:image/png;base64,{img_data}"
        
        except Exception as e:
            print(f"Error loading default image: {str(e)}")
            return ""  
        
    def get_book_image_path(self, book: BookSchema) -> str:
        """
        Get the path to the book cover image, 
        using default if none exists
        """
        if book.cover_image_path and os.path.exists(book.cover_image_path):
            return book.cover_image_path
        return f"{self.assets_dir}/default_book.png"

    
    def _format_book_summary(
        self, 
        book: BookSchema, 
        max_length: int = 150, 
        max_lines: int = 2
    ) -> str:
        """
        Format the book summary for display on the book card.
        """
        if not book.summary:
            return "No summary available."
            
        # Split summary into lines
        summary_lines = book.summary.split("\n")
        
        # If there are multiple lines, take the specified number
        if len(summary_lines) >= max_lines:
            summary_text = "\n".join(summary_lines[:max_lines])
        else:
            # Otherwise truncate to max_length
            summary_text = self.ui_builder.truncate_text(book.summary, max_length)
            
        # Add ellipsis if the summary was truncated
        if (len(summary_lines) > max_lines) or (len(book.summary) > max_length):
            summary_text += "..."
            
        return summary_text