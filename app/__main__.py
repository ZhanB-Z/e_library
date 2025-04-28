import flet as ft

from app.backend.client import get_backend_client
from app.frontend.app import get_flet_app
from app.logger import setup_logger
from app.settings import Settings, get_settings

def main() -> None:
    setup_logger()
    # Get settings
    settings = get_settings()
    
    # Init backend client
    backend_client = get_backend_client()
    
    # Init the app
    ft.app( 
        target=lambda page: get_flet_app(
            page=page,
            dev_mode=settings.dev_mode,
            flet_host=settings.flet_host,
            flet_port=settings.flet_port,
            flet_slug=settings.flet_slug,
            flet_secret_key=settings.flet_secret_key,
            flet_prod_host=settings.flet_prod_host,
            download_server_url=settings.download_server_url,
            backend_client=backend_client,
        ),
        host=settings.flet_host,
        port=settings.flet_port,
        view=None
    )
    
if __name__ == "__main__":
    main()