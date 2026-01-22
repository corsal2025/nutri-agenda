"""
NutriAgenda - Main Application
Flet-based nutrition management app
"""
import flet as ft
from utils.theme import AppTheme, AppColors
from ui.screens.login_screen import LoginScreen
from ui.screens.register_screen import RegisterScreen
from ui.screens.nutritionist_dashboard import NutritionistDashboard
from ui.screens.client_dashboard import ClientDashboard
from services.auth_service import auth_service


class NutriAgendaApp:
    """Main application class"""
    
    def __init__(self, page: ft.Page):
        self.page = page
        self.current_user = None
        
        # Configure page
        self.page.title = "NutriAgenda"
        self.page.theme = AppTheme.get_light_theme()
        self.page.bgcolor = AppColors.BACKGROUND
        self.page.padding = 0
        self.page.window_width = 400
        self.page.window_height = 800
        self.page.window_resizable = True
        
        # Show login screen
        self.show_login()
    
    def show_login(self):
        """Show login screen"""
        self.page.clean()
        login_screen = LoginScreen(
            self.page,
            on_login_success=self.handle_login_success,
            on_go_to_register=self.show_register
        )
        self.page.add(login_screen.get_view())
        self.page.update()
    
    def show_register(self):
        """Show register screen"""
        self.page.clean()
        register_screen = RegisterScreen(
            self.page,
            on_register_success=self.handle_register_success,
            on_go_to_login=self.show_login
        )
        self.page.add(register_screen.get_view())
        self.page.update()
    
    def handle_login_success(self, user_data: dict):
        """Handle successful login"""
        self.current_user = user_data
        
        # Show appropriate dashboard based on role
        if user_data.get('role') == 'nutritionist':
            self.show_nutritionist_dashboard()
        else:
            self.show_client_dashboard()
    
    def handle_register_success(self, user_data: dict):
        """Handle successful registration"""
        # After successful registration, go to login
        self.show_login()
    
    def show_nutritionist_dashboard(self):
        """Show nutritionist dashboard"""
        self.page.clean()
        dashboard = NutritionistDashboard(
            self.page,
            self.current_user,
            on_logout=self.handle_logout
        )
        self.page.add(dashboard.get_view())
        self.page.update()
    
    def show_client_dashboard(self):
        """Show client dashboard"""
        self.page.clean()
        dashboard = ClientDashboard(
            self.page,
            self.current_user,
            on_logout=self.handle_logout
        )
        self.page.add(dashboard.get_view())
        self.page.update()
    
    def handle_logout(self):
        """Handle user logout"""
        auth_service.logout()
        self.current_user = None
        self.show_login()


def main(page: ft.Page):
    """Main entry point"""
    app = NutriAgendaApp(page)


if __name__ == "__main__":
    import os
    
    # Configurar logging
    import logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("flet")
    
    port = int(os.environ.get("PORT", 8551))
    logger.info(f"Starting Flet app on port {port}")
    
    try:
        ft.app(
            target=main,
            view=ft.AppView.WEB_BROWSER,
            port=port,
            host="0.0.0.0",
            # web_renderer="html"  # Removed: HTML renderer not supported in newer Flet versions
        )
    except Exception as e:
        logger.error(f"Error starting app: {e}")

