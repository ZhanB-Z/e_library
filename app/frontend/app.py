import asyncio
import time
import flet as ft

from loguru import logger

from app.backend.client import BackendClient
from app.frontend.tabs.main_tab import MainTabBuilder
from app.frontend.ui_components import UIComponents
from app.frontend.tab_manager import TabManager
from app.frontend.assets.theme import AppColors, AppTypography, AppSpacing, AppTabs


class FletApp():
    def __init__(
        self,
        page: ft.Page,
        dev_mode: bool,
        flet_host: str,
        flet_port: int,
        flet_slug: str,
        flet_secret_key: str,
        app_prod_host: str,
        download_server_url: str,
        assets_dir: str,
        backend_client: BackendClient,
    ) -> None:
        self.page = page
        self.page.scroll = "auto"
        self.page.bgcolor = AppColors.BACKGROUND
        self.dev_mode = dev_mode
        self.assets_dir = assets_dir
        self.backend_client = backend_client
        self.ui_builder = UIComponents(page=self.page)
        self.dialog = ft.AlertDialog(open=False)

        # Init TabManager and pass tab_handlers
        self.tab_manager = TabManager(
            page=self.page,
            tab_titles=["Welcome", "About me"],
            tab_handlers={
                0: self.create_main_tab,
                1: self.create_aboutme_tab,
            }
        )
        
        # Create main tab builder
        self.main_tab_builder = MainTabBuilder(
            self.page, 
            self.assets_dir,
            self.ui_builder,
            self.backend_client
        )
        
        # Set up the page
        self.page.title = "Flet Application"
        self.page.vertical_alignment = ft.MainAxisAlignment.START
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        
        # Add tabs to the page with proper spacing
        tabs_container = ft.Container(
            content=self.tab_manager.tabs,
            height=AppTabs.HEIGHT,
            margin=ft.margin.only(bottom=AppTabs.MARGIN_BOTTOM),
            padding=0,
        )
        self.page.add(tabs_container)
        
        # Trigger the initial tab (Welcome)
        self.tab_manager.select_tab(0)
    
    def create_main_tab(self):
        """Create content for the main tab"""
        # Get the layout and add it to the page
        main_layout = self.main_tab_builder.create_tab()
        self.page.add(main_layout)
        self.page.update()
    
    
    def create_aboutme_tab(self):
        """Creates content for the About Me tab"""
        about_me_header = self.ui_builder.create_text_field(
            value="About Me",
            text_size=AppTypography.HEADER_SIZE,
            color=AppColors.TEXT_PRIMARY
        )
        
        about_me_form = ft.Column(
            [   
                self.ui_builder.create_text_field(
                    value="Name: Bauyrzhan Zhanuzakov"
                    ),
                self.ui_builder.create_text_field(
                    value="Position: Python Developer"
                    ),
                self.ui_builder.create_text_field(
                    value="Hobbies: programming, football, books"
                    ),
                self.ui_builder.create_text_field(
                    value="Email: bauyrzhan@zhanuzakov.com"
                    ),
                self.ui_builder.create_button(
                    text="Back",
                    on_click=self.back_handler,
                    bgcolor=AppColors.PRIMARY,
                    color=AppColors.TEXT_PRIMARY
                )
            ], 
            spacing=AppSpacing.MEDIUM,
            alignment=ft.MainAxisAlignment.CENTER
        )
        
        self.ui_builder.add_elements_to_page(
            about_me_header,
            about_me_form
        )
        self.page.update()
    
        
    def back_handler(self, e: ft.ControlEvent) -> None:
        """Handles back button click"""
        success = self.tab_manager.back_to_previous()
        if not success:
            # Show message if already at the first tab
            self.snack_bar = ft.SnackBar(
                content=ft.Text("Already at the first tab"),
                action="OK"
            )
            self.page.add(self.snack_bar)
            self.snack_bar.open = True
            self.page.update()
            

def get_flet_app(
    page: ft.Page,
    dev_mode: bool,
    flet_host: str,
    flet_port: int,
    flet_slug: str,
    flet_secret_key: str,
    flet_prod_host: str,
    download_server_url: str,
    backend_client: BackendClient,
    assets_dir: str
) -> FletApp:
    app = FletApp(
        page=page,
        dev_mode=dev_mode,
        flet_host=flet_host,
        flet_port=flet_port,
        flet_slug=flet_slug,
        flet_secret_key=flet_secret_key,
        app_prod_host=flet_prod_host,
        download_server_url=download_server_url,
        backend_client=backend_client,
        assets_dir=assets_dir,
    )

    return app