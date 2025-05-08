from typing import Callable, List
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
        ui_builder: UIComponents,
        backend_client: BackendClient
    ):
        self.page = page
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
        for i in range(0, len(books), 5):
            row_books = books[i:i+5]
            row = ft.Row(
                [self.create_book_card(book, on_edit_book) for book in row_books],
                alignment=ft.MainAxisAlignment.START,
                spacing=AppSpacing.MEDIUM
            )
            book_cards.append(row)
        
        return ft.Column(book_cards, spacing=AppSpacing.LARGE)
    
    def create_book_card(self, book: BookSchema, on_edit_book: Callable):
        """Create a card for a single book"""
        # Title Container
        title_container = ft.Container(
            content=self.ui_builder.create_text_field(
                value=self.ui_builder.truncate_text(book.title, max_length=25),
                text_size=AppTypography.SUBHEADER_SIZE,
                color=AppColors.TEXT_PRIMARY,
                # tooltip=book.title,  # Show full title on hover
                overflow=ft.TextOverflow.ELLIPSIS,
                no_wrap=True,  
            ),
            height=40,  # Fixed height for title container
            width=260,  # Fixed width
            alignment=ft.alignment.center_left 
        )
            
        # Title and author
        title = self.ui_builder.create_text_field(
            value=title_container,
            text_size=AppTypography.SUBHEADER_SIZE,
            color=AppColors.TEXT_PRIMARY
        )
        
        author = self.ui_builder.create_text_field(
            value=f"by {book.author}",
            text_size=AppTypography.BODY_SIZE,
            color=AppColors.TEXT_SECONDARY
        )
        
        # Publication info
        pub_info = ""
        if book.year_published:
            pub_info += f"Published: {book.year_published}"
        if book.year_read:
            if pub_info:
                pub_info += " | "
            pub_info += f"Read: {book.year_read}"
            
        pub_info_text = self.ui_builder.create_text_field(
            value=pub_info,
            text_size=AppTypography.BODY_SIZE - 2,
            color=AppColors.TEXT_SECONDARY
        )
        
        # Rating stars
        rating_row = ft.Row([])
        if book.rating:
            for i in range(5):
                icon = ft.icons.STAR if i < book.rating else ft.icons.STAR_BORDER
                rating_row.controls.append(ft.Icon(icon, color=AppColors.ACCENT, size=18))
        
        # Genres
        genres_text = ""
        if book.genres:
            genres_text = ", ".join(book.genres)
            
        genres = self.ui_builder.create_text_field(
            value=genres_text,
            text_size=AppTypography.BODY_SIZE - 2,
            color=AppColors.TEXT_SECONDARY
        )
        
        # Edit button
        edit_button = self.ui_builder.create_button(
            text="Edit",
            on_click=lambda e, b=book: on_edit_book(e, b),
            width=100,
            bgcolor=AppColors.SECONDARY,
            color=AppColors.TEXT_PRIMARY,
        )
        
        # Delete button
        delete_button = self.ui_builder.create_button(
            text="Delete",
            on_click=lambda e, b=book: self.handle_delete_book(e, b),
            width=100,
            bgcolor=AppColors.ERROR,
            color=AppColors.TEXT_PRIMARY
        )
        
        # Book card content
        content = ft.Column([
            title_container,
            author,
            pub_info_text,
            rating_row,
            genres,
            ft.Container(height=AppSpacing.MEDIUM),  # Spacer
            ft.Row([
                edit_button,
                delete_button
                ], 
                spacing=AppSpacing.SMALL,
                alignment=ft.MainAxisAlignment.END
            )
        ], spacing=AppSpacing.SMALL)
        
        # Create and return the card
        return self.ui_builder.create_card(
            content=content,
            width=300,
            height=None  # Let height adjust to content
        )
        
    def handle_delete_book(self, e: ft.ControlEvent, book: BookSchema) -> None:
        """Handle deletion of a book"""
        def confirm_delete(e: ft.ControlEvent) -> None:
            # Delete the book
            success = self.backend_client.delete_book(book.id)
            
            # Close the dialog
            if self.confirm_dialog in self.page.controls:
                self.page.controls.remove(self.confirm_dialog)
            
            if hasattr(self.page, 'overlay') and self.confirm_dialog in self.page.overlay:
                self.page.overlay.remove(self.confirm_dialog)
                
            self.confirm_dialog.open = False
            self.page.update()
            
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
        
        def cancel_delete(e: ft.ControlEvent) -> None:
            # Close the dialog without deleting
            if self.confirm_dialog in self.page.controls:
                self.page.controls.remove(self.confirm_dialog)
                
            if hasattr(self.page, 'overlay') and self.confirm_dialog in self.page.overlay:
                self.page.overlay.remove(self.confirm_dialog)
                
            self.confirm_dialog.open = False
            self.page.update()
        
        # Create confirmation dialog
        self.confirm_dialog = ft.AlertDialog(
            title=ft.Text("Confirm Delete"),
            content=ft.Text(f"Are you sure you want to delete '{book.title}'?"),
            actions=[
                ft.TextButton("Cancel", on_click=cancel_delete),
                ft.TextButton("Delete", on_click=confirm_delete)
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            open=True
        )
        
        # Show the dialog by adding it to the page
        self.page.add(self.confirm_dialog)
        self.page.update()
    
    
    def update_book_grid(self, on_edit_book: Callable) -> ft.Column:
        """
        Update the book grid with fresh data from the backend.
        Returns the updated book grid component.
        """
        logger.info("UPDATE_BOOK_GRID: Fetching updated books")
        
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
                    logger.info("UPDATE_BOOK_GRID: Grid replaced in main layout")
                    break
        
        return updated_grid


