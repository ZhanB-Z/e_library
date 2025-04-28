import flet as ft
from typing import Dict, List, Callable, Optional, Any, Union

class TabManager:
    """
    Manages tabs in a Flet application, including tab switching, access control,
    and content handling.
    """
    
    def __init__(
        self,
        page: ft.Page,
        tab_titles: List[str],
        tab_handlers: Dict[int, Callable[[], None]] = None,
        tab_number_after_authorization: Optional[int] = None,
        is_authorized: bool = False,
    ):
        """
        Initialize the tab manager.
        
        Args:
            page: The Flet page instance
            tab_titles: List of tab titles to display
            tab_handlers: Dictionary mapping tab indices to handler functions
            tab_number_after_authorization: Index after which tabs require authorization
            is_authorized: Whether the user is currently authorized
        """
        self.page = page
        self.tab_titles = tab_titles
        self.tab_handlers = tab_handlers or {}
        self.tab_number_after_authorization = tab_number_after_authorization
        self.is_authorized = is_authorized
        
        # Create the tabs control
        self.tabs = self._create_tabs()
        
        # Dictionary to store content for each tab
        self.tab_contents: Dict[int, Any] = {}
        
    def _create_tabs(self) -> ft.Tabs:
        """Create the tabs control with the specified titles."""
        tabs = ft.Tabs(
            selected_index=0,
            animation_duration=300,
            tabs=[ft.Tab(text=title) for title in self.tab_titles],
            on_change=self.handle_tab_change,
        )
        return tabs
    
    def handle_tab_change(self, e: ft.ControlEvent) -> None:
        """
        Handles tab changes with access control checks.
        If tab_number_after_authorization is set, tabs after that index
        will require authorization.
        
        Args:
            e: Flet control event for tab change
        """
        selected_index = e.control.selected_index
        
        # Check authorization requirements
        if self.tab_number_after_authorization is not None:
            # Check if user is trying to access a restricted tab without authorization
            if (
                selected_index >= self.tab_number_after_authorization
                and not self.is_authorized
            ):
                # Reset to previous tab
                self.tabs.selected_index = self.tabs.selected_index
                
                # Show error message
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text(
                        "Please authorize to access this tab.",
                    ),
                    duration=3000,
                )
                self.page.snack_bar.open = True
                self.page.update()
                return
        
        # Clear page content
        self._clear_page()
        
        # Call the appropriate tab handler if defined
        handler = self.tab_handlers.get(selected_index)
        if handler:
            handler()
    
    def _clear_page(self) -> None:
        """Clear the page content except for the tabs."""
        # Save tabs instance
        tabs_instance = self.tabs
        
        # Clear page
        self.page.clean()
        
        # Re-add tabs at the top
        self.page.add(
            ft.Container(
                content=tabs_instance,
                margin=ft.margin.only(bottom=20),
            )
        )
        self.page.update()
    
    def set_tab_content(self, tab_index: int, content: Union[ft.Control, List[ft.Control]]) -> None:
        """
        Set content for a specific tab.
        
        Args:
            tab_index: Index of the tab
            content: Content to display (control or list of controls)
        """
        if isinstance(content, list):
            self.tab_contents[tab_index] = ft.Column(
                controls=content,
                alignment=ft.MainAxisAlignment.START,
                spacing=10,
            )
        else:
            self.tab_contents[tab_index] = content
            
        # If this is the current tab, update the page
        if self.tabs.selected_index == tab_index:
            self._clear_page()
            self.page.add(self.tab_contents[tab_index])
            self.page.update()
    
    def add_tab(self, title: str, handler: Optional[Callable[[], None]] = None) -> int:
        """
        Add a new tab.
        
        Args:
            title: Tab title
            handler: Function to call when tab is selected
            
        Returns:
            Index of the newly added tab
        """
        # Add tab to the tabs control
        self.tabs.tabs.append(ft.Tab(text=title))
        
        # Calculate new tab index
        new_index = len(self.tabs.tabs) - 1
        
        # Add handler if provided
        if handler:
            self.tab_handlers[new_index] = handler
            
        self.page.update()
        return new_index
    
    def remove_tab(self, index: int) -> None:
        """
        Remove a tab.
        
        Args:
            index: Index of the tab to remove
        """
        if 0 <= index < len(self.tabs.tabs):
            # Remove tab from tabs control
            self.tabs.tabs.pop(index)
            
            # Remove handler if exists
            if index in self.tab_handlers:
                self.tab_handlers.pop(index)
                
            # Remove content if exists
            if index in self.tab_contents:
                self.tab_contents.pop(index)
                
            # Adjust handlers and contents for higher indices
            new_handlers = {}
            new_contents = {}
            
            for i, handler in self.tab_handlers.items():
                if i > index:
                    new_handlers[i-1] = handler
                else:
                    new_handlers[i] = handler
                    
            for i, content in self.tab_contents.items():
                if i > index:
                    new_contents[i-1] = content
                else:
                    new_contents[i] = content
                    
            self.tab_handlers = new_handlers
            self.tab_contents = new_contents
            
            # Update selected index if needed
            if self.tabs.selected_index >= len(self.tabs.tabs):
                self.tabs.selected_index = len(self.tabs.tabs) - 1
                
            self.page.update()
    
    def select_tab(self, index: int) -> None:
        """
        Select a specific tab and trigger its handler.
        
        Args:
            index: Index of the tab to select
        """
        if 0 <= index < len(self.tabs.tabs):
            # Update selected index
            self.tabs.selected_index = index
            
            # Clear page content
            self._clear_page()
            
            # Call the appropriate tab handler if defined
            handler = self.tab_handlers.get(index)
            if handler:
                handler()
            
            self.page.update()
    
    def back_to_previous(self) -> None:
        """
        Navigate to the previous tab if possible.
        
        Returns:
            True if successful, False if already at the first tab
        """
        current_index = self.tabs.selected_index
        if current_index > 0:
            # Navigate to previous tab
            self.select_tab(current_index - 1)
            return True
        return False
    
    def set_authorization_status(self, is_authorized: bool) -> None:
        """
        Update authorization status.
        
        Args:
            is_authorized: New authorization status
        """
        self.is_authorized = is_authorized