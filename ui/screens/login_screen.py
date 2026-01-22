"""
Login Screen
"""
import flet as ft
from utils.theme import AppColors, AppSpacing, AppBorderRadius, AppTheme
from services.auth_service import auth_service


class LoginScreen:
    """Login screen component"""
    
    def __init__(self, page: ft.Page, on_login_success, on_go_to_register):
        self.page = page
        self.on_login_success = on_login_success
        self.on_go_to_register = on_go_to_register
        
        # Form fields
        self.email_field = ft.TextField(
            label="Email",
            hint_text="nutricionista@ejemplo.com",
            prefix_icon=ft.icons.EMAIL,
            keyboard_type=ft.KeyboardType.EMAIL,
            autofocus=True,
        )
        
        self.password_field = ft.TextField(
            label="Contraseña",
            hint_text="Ingrese su contraseña",
            prefix_icon=ft.icons.LOCK_OUTLINE,
            password=True,
            can_reveal_password=True,
        )
        
        self.error_text = ft.Text(
            "",
            color=AppColors.ERROR,
            size=12,
            visible=False
        )
        
        self.login_button = ft.ElevatedButton(
            "Iniciar Sesión",
            icon=ft.icons.LOGIN,
            on_click=self.handle_login,
            style=ft.ButtonStyle(
                bgcolor=AppColors.PRIMARY,
                color=ft.colors.WHITE,
            ),
            width=300,
            height=50,
        )
        
        self.loading_indicator = ft.ProgressRing(visible=False)
    
    def get_view(self):
        """Get the screen view as a Container"""
        return ft.Container(
            content=self.build(),
            expand=True,
            bgcolor=AppColors.BACKGROUND,
            alignment=ft.alignment.center,
        )
    
    def build(self):
        """Build the login screen UI"""
        return ft.Container(
            content=ft.Column(
                controls=[
                    # Logo/Title
                    ft.Container(
                        content=ft.Icon(
                            ft.icons.LOCAL_DINING,
                            size=80,
                            color=AppColors.PRIMARY
                        ),
                        alignment=ft.alignment.center,
                        margin=ft.margin.only(bottom=AppSpacing.MD),
                    ),
                    ft.Text(
                        "NutriAgenda",
                        style=AppTheme.get_title_style(),
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Text(
                        "Gestión profesional de nutrición",
                        style=AppTheme.get_caption_style(),
                        text_align=ft.TextAlign.CENTER,
                    ),
                    
                    ft.Container(height=AppSpacing.XL),
                    
                    # Login form card
                    ft.Card(
                        content=ft.Container(
                            content=ft.Column(
                                controls=[
                                    ft.Text(
                                        "Iniciar Sesión",
                                        style=AppTheme.get_subtitle_style(),
                                    ),
                                    ft.Container(height=AppSpacing.MD),
                                    self.email_field,
                                    self.password_field,
                                    self.error_text,
                                    ft.Container(height=AppSpacing.MD),
                                    self.login_button,
                                    self.loading_indicator,
                                ],
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            ),
                            padding=AppSpacing.XL,
                            width=400,
                        ),
                        elevation=4,
                    ),
                    
                    ft.Container(height=AppSpacing.MD),
                    
                    # Register link
                    ft.Row(
                        controls=[
                            ft.Text("¿No tienes cuenta?", style=AppTheme.get_body_style()),
                            ft.TextButton(
                                "Registrarse",
                                on_click=lambda _: self.on_go_to_register(),
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            alignment=ft.alignment.center,
        )
    
    async def handle_login(self, e):
        """Handle login button click"""
        # Validate fields
        if not self.email_field.value or not self.password_field.value:
            self.show_error("Por favor complete todos los campos")
            return
        
        # Show loading
        self.login_button.disabled = True
        self.loading_indicator.visible = True
        self.error_text.visible = False
        self.page.update()
        
        try:
            # Attempt login
            result = await auth_service.login(
                self.email_field.value,
                self.password_field.value
            )
            
            if result['success']:
                # Clear fields
                self.email_field.value = ""
                self.password_field.value = ""
                
                # Call success callback
                self.on_login_success(result['user'])
            else:
                self.show_error(result.get('message', 'Error al iniciar sesión'))
                
        except Exception as ex:
            self.show_error(f"Error: {str(ex)}")
        
        finally:
            # Hide loading
            self.login_button.disabled = False
            self.loading_indicator.visible = False
            self.page.update()
    
    def show_error(self, message: str):
        """Show error message"""
        self.error_text.value = message
        self.error_text.visible = True
        self.page.update()
