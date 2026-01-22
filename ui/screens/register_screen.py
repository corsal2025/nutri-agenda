"""
Register Screen
"""
import flet as ft
from utils.theme import AppColors, AppSpacing, AppTheme
from services.auth_service import auth_service


class RegisterScreen:
    """Registration screen component"""
    
    def __init__(self, page: ft.Page, on_register_success, on_go_to_login):
        self.page = page
        self.on_register_success = on_register_success
        self.on_go_to_login = on_go_to_login
        
        # Form fields
        self.name_field = ft.TextField(
            label="Nombre completo",
            hint_text="Juan Pérez",
            prefix_icon="person_outline",
            autofocus=True,
        )
        
        self.email_field = ft.TextField(
            label="Email",
            hint_text="usuario@ejemplo.com",
            prefix_icon="email",
            keyboard_type=ft.KeyboardType.EMAIL,
        )
        
        self.phone_field = ft.TextField(
            label="Teléfono",
            hint_text="+54 9 11 1234-5678",
            prefix_icon="phone",
            keyboard_type=ft.KeyboardType.PHONE,
        )
        
        self.password_field = ft.TextField(
            label="Contraseña",
            hint_text="Mínimo 6 caracteres",
            prefix_icon="lock_outline",
            password=True,
            can_reveal_password=True,
        )
        
        self.role_dropdown = ft.Dropdown(
            label="Rol",
            hint_text="Seleccione su rol",
            options=[
                ft.dropdown.Option("nutritionist", "Nutricionista"),
                ft.dropdown.Option("client", "Cliente"),
            ],
            value="nutritionist",
        )
        
        self.error_text = ft.Text(
            "",
            color=AppColors.ERROR,
            size=12,
            visible=False
        )
        
        self.register_button = ft.ElevatedButton(
            "Registrarse",
            icon="person_add",
            on_click=self.handle_register,
            style=ft.ButtonStyle(
                bgcolor=AppColors.PRIMARY,
                color="white",
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
        """Build the register screen UI"""
        return ft.Container(
            content=ft.Column(
                controls=[
                    # Logo/Title
                    ft.Container(
                        content=ft.Icon(
                            "local_dining",
                            size=60,
                            color=AppColors.PRIMARY
                        ),
                        alignment=ft.alignment.center,
                    ),
                    ft.Text(
                        "Crear Cuenta",
                        style=AppTheme.get_title_style(),
                        text_align=ft.TextAlign.CENTER,
                    ),
                    
                    ft.Container(height=AppSpacing.LG),
                    
                    # Register form card
                    ft.Card(
                        content=ft.Container(
                            content=ft.Column(
                                controls=[
                                    self.name_field,
                                    self.email_field,
                                    self.phone_field,
                                    self.password_field,
                                    self.role_dropdown,
                                    self.error_text,
                                    ft.Container(height=AppSpacing.SM),
                                    self.register_button,
                                    self.loading_indicator,
                                ],
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                scroll=ft.ScrollMode.AUTO,
                            ),
                            padding=AppSpacing.XL,
                            width=400,
                        ),
                        elevation=4,
                    ),
                    
                    ft.Container(height=AppSpacing.MD),
                    
                    # Login link
                    ft.Row(
                        controls=[
                            ft.Text("¿Ya tienes cuenta?", style=AppTheme.get_body_style()),
                            ft.TextButton(
                                "Iniciar Sesión",
                                on_click=lambda _: self.on_go_to_login(),
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                scroll=ft.ScrollMode.AUTO,
            ),
            alignment=ft.alignment.center,
        )
    
    async def handle_register(self, e):
        """Handle register button click"""
        # Validate fields
        if not all([
            self.name_field.value,
            self.email_field.value,
            self.phone_field.value,
            self.password_field.value,
            self.role_dropdown.value
        ]):
            self.show_error("Por favor complete todos los campos")
            return
        
        if len(self.password_field.value) < 6:
            self.show_error("La contraseña debe tener al menos 6 caracteres")
            return
        
        # Show loading
        self.register_button.disabled = True
        self.loading_indicator.visible = True
        self.error_text.visible = False
        self.page.update()
        
        try:
            # Attempt registration
            result = await auth_service.register(
                email=self.email_field.value,
                password=self.password_field.value,
                name=self.name_field.value,
                phone=self.phone_field.value,
                role=self.role_dropdown.value
            )
            
            if result['success']:
                # Show success message
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text("¡Registro exitoso! Ahora puede iniciar sesión"),
                    bgcolor=AppColors.SUCCESS,
                )
                self.page.snack_bar.open = True
                
                # Clear fields
                self.name_field.value = ""
                self.email_field.value = ""
                self.phone_field.value = ""
                self.password_field.value = ""
                
                # Go to login
                self.on_go_to_login()
            else:
                self.show_error(result.get('message', 'Error al registrar'))
                
        except Exception as ex:
            self.show_error(f"Error: {str(ex)}")
        
        finally:
            # Hide loading
            self.register_button.disabled = False
            self.loading_indicator.visible = False
            self.page.update()
    
    def show_error(self, message: str):
        """Show error message"""
        self.error_text.value = message
        self.error_text.visible = True
        self.page.update()
