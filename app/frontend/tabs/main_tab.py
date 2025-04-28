import flet as ft
from app.frontend.ui_components import UIComponents
from app.frontend.theme import AppColors, AppTypography, AppSpacing

class MainTabBuilder:
    def __init__(self, page: ft.Page, ui_builder: UIComponents):
        self.page = page
        self.ui_builder = ui_builder
        
    def create_tab(self, on_add_book):
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
        
        # Main layout
        main_layout = ft.Column([
            # Centered header section
            ft.Container(
                content=ft.Column([header, description], spacing=AppSpacing.SMALL),
                alignment=ft.alignment.center
            ),
            
            ft.Container(height=AppSpacing.LARGE),  # Spacer
            
            # Right-aligned button 
            ft.Container(
                content=add_button,
                alignment=ft.alignment.bottom_right
            ),
            
            # Book grid would go here
        ])
        
        return main_layout