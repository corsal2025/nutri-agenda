"""
Login Screen
Premium Redesign
"""
import flet as ft
from utils.theme import AppColors, AppSpacing, AppBorderRadius, AppTheme, AppShadows


class LoginScreen:
    """Login screen component with premium styling"""
    
    def __init__(self, page: ft.Page, on_login_success, on_go_to_register):
        self.page = page
        self.on_login_success = on_login_success
        self.on_go_to_register = on_go_to_register
        
        # Premium Styled Fields
        self.email_field = ft.TextField(
            label="Correo Electrónico",
            hint_text="ejemplo@correo.com",
            prefix_icon=ft.icons.EMAIL_OUTLINED,
            keyboard_type=ft.KeyboardType.EMAIL,
            autofocus=True,
            border_radius=AppBorderRadius.MD,
            border_color=AppColors.BORDER,
            focused_border_color=AppColors.PRIMARY,
            text_size=14,
            content_padding=15,
        )
        
        self.password_field = ft.TextField(
            label="Contraseña",
            hint_text="••••••••",
            prefix_icon=ft.icons.LOCK_OUTLINE_ROUNDED,
            password=True,
            can_reveal_password=True,
            border_radius=AppBorderRadius.MD,
            border_color=AppColors.BORDER,
            focused_border_color=AppColors.PRIMARY,
            text_size=14,
            content_padding=15,
        )
        
        self.error_text = ft.Text(
            "",
            color=AppColors.ERROR,
            size=12,
            visible=False,
            text_align=ft.TextAlign.CENTER
        )
        
        self.login_button = ft.ElevatedButton(
            content=ft.Row(
                [
                    ft.Text("Iniciar Sesión", size=16, weight=ft.FontWeight.W_600),
                    ft.Icon(ft.icons.ARROW_FORWARD_ROUNDED, size=20)
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            on_click=self.handle_login,
            style=ft.ButtonStyle(
                bgcolor={
                    ft.MaterialState.DEFAULT: AppColors.PRIMARY,
                    ft.MaterialState.HOVERED: AppColors.PRIMARY_DARK,
                },
                color="white",
                elevation={"pressed": 0, "": 4},
                animation_duration=200,
                shape=ft.RoundedRectangleBorder(radius=AppBorderRadius.MD),
            ),
            width=320,
            height=48,
        )
        
        self.loading_indicator = ft.ProgressRing(
            width=24, 
            height=24, 
            stroke_width=2, 
            color=AppColors.PRIMARY,
            visible=False
        )
    
    def get_view(self):
        """Get the screen view"""
        return ft.Container(
            content=self.build(),
            expand=True,
            bgcolor=AppColors.BACKGROUND,
            alignment=ft.alignment.center,
            # Subtle background pattern or gradient could go here
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[AppColors.BACKGROUND, AppColors.SURFACE_VARIANT],
            ),
        )
    
    def build(self):
        """Build the modernized login UI"""
        return ft.Container(
            content=ft.Column(
                controls=[
                    # Main Card Content
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                # Brand Section
                                ft.Container(
                                    content=ft.Icon(
                                        ft.icons.ECO_ROUNDED, # More modern icon
                                        size=64,
                                        color=AppColors.PRIMARY
                                    ),
                                    alignment=ft.alignment.center,
                                    margin=ft.margin.only(bottom=AppSpacing.SM),
                                ),
                                ft.Text(
                                    "NutriAgenda",
                                    style=AppTheme.get_header_style(),
                                    text_align=ft.TextAlign.CENTER,
                                ),
                                ft.Text(
                                    "Bienvenido de nuevo",
                                    style=AppTheme.get_caption_style(),
                                    text_align=ft.TextAlign.CENTER,
                                    color=AppColors.TEXT_SECONDARY 
                                ),
                                
                                ft.Container(height=AppSpacing.LG),
                                
                                # Login Form Section
                                ft.Text(
                                    "Ingresa a tu cuenta",
                                    style=AppTheme.get_subtitle_style(),
                                    color=AppColors.TEXT_PRIMARY
                                ),
                                ft.Container(height=AppSpacing.MD),
                                
                                self.email_field,
                                ft.Container(height=AppSpacing.SM),
                                self.password_field,
                                
                                ft.Container(height=AppSpacing.SM),
                                self.error_text,
                                ft.Container(height=AppSpacing.MD),
                                
                                # Action Section
                                ft.Container(
                                    content=ft.Stack(
                                        controls=[
                                            self.login_button,
                                            ft.Container(
                                                content=self.loading_indicator,
                                                alignment=ft.alignment.center_right,
                                                padding=ft.padding.only(right=15),
                                            )
                                        ],
                                        alignment=ft.alignment.center
                                    ),
                                ),
                                
                                ft.Container(height=AppSpacing.LG),
                                
                                # Footer
                                ft.Row(
                                    controls=[
                                        ft.Text("¿No tienes cuenta?", 
                                               style=AppTheme.get_body_style(),
                                               color=AppColors.TEXT_SECONDARY),
                                        ft.TextButton(
                                            "Crear cuenta",
                                            on_click=lambda _: self.on_go_to_register(),
                                            style=ft.ButtonStyle(
                                                color=AppColors.PRIMARY,
                                                text_style=ft.TextStyle(weight=ft.FontWeight.W_600)
                                            )
                                        ),
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                ),
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        padding=ft.padding.all(40),
                        width=450,
                        border_radius=AppBorderRadius.XL,
                        bgcolor=AppColors.SURFACE,
                        shadow=AppShadows.lg, # Premium shadow
                    ),
                    
                    # Footer Credits
                    ft.Container(height=AppSpacing.XL),
                    ft.Text(
                        "© 2026 NutriAgenda. Gestión Profesional.",
                        style=AppTheme.get_caption_style(),
                        color=AppColors.TEXT_SECONDARY,
                        opacity=0.7
                    )
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                scroll=ft.ScrollMode.AUTO,
            ),
            alignment=ft.alignment.center,
            padding=20,
        )
    
    async def handle_login(self, e):
        """Handle login button click"""
        # Reset error
        self.error_text.visible = False
        self.page.update()
        
        # Validate fields
        if not self.email_field.value or not self.password_field.value:
            self.show_error("Por favor completa todos los campos")
            return
        
        # Show loading state
        self.login_button.disabled = True
        self.loading_indicator.visible = True
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
                self.on_login_success(result['user'])
            else:
                self.show_error(result.get('message', 'Credenciales inválidas'))
                
        except Exception as ex:
            self.show_error(f"Error de conexión: {str(ex)}")
        
        finally:
            # Reset state
            self.login_button.disabled = False
            self.loading_indicator.visible = False
            self.page.update()
    
    def show_error(self, message: str):
        """Show error message with animation"""
        self.error_text.value = message
        self.error_text.visible = True
        self.page.update()
