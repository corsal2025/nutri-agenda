"""
Nutritionist Dashboard Screen
"""
import flet as ft
from utils.theme import AppColors, AppSpacing, AppTheme
from services.auth_service import auth_service
from services.client_service import client_service
from services.appointment_service import appointment_service
from datetime import datetime, date


class NutritionistDashboard:
    """Dashboard for nutritionists"""
    
    def __init__(self, page: ft.Page, user_data: dict, on_logout):
        self.page = page
        self.user_data = user_data
        self.on_logout = on_logout
        
        # Stats
        self.total_clients = 0
        self.appointments_today = 0
        self.upcoming_appointments = 0
        
        # Load data
        self.load_stats()
    
    def get_view(self):
        """Get the screen view as a Container"""
        return ft.Container(
            content=self.build(),
            expand=True,
            bgcolor=AppColors.BACKGROUND,
            padding=AppSpacing.MD,
        )
    
    def build(self):
        """Build dashboard UI"""
        return ft.Column(
            controls=[
                # Header
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Column(
                                controls=[
                                    ft.Text(
                                        f"Hola, {self.user_data.get('name', 'Usuario')}",
                                        style=AppTheme.get_title_style(),
                                    ),
                                    ft.Text(
                                        f"Nutricionista • {datetime.now().strftime('%d/%m/%Y')}",
                                        style=AppTheme.get_caption_style(),
                                    ),
                                ],
                                expand=True,
                            ),
                            ft.IconButton(
                                icon="logout",
                                tooltip="Cerrar sesión",
                                on_click=lambda _: self.on_logout(),
                            ),
                        ],
                    ),
                    padding=AppSpacing.MD,
                    bgcolor=AppColors.SURFACE,
                    border_radius=8,
                ),
                
                ft.Container(height=AppSpacing.MD),
                
                # Stats cards
                ft.Row(
                    controls=[
                        self.create_stat_card(
                            "Total Clientes",
                            str(self.total_clients),
                            "people",
                            AppColors.PRIMARY
                        ),
                        self.create_stat_card(
                            "Citas Hoy",
                            str(self.appointments_today),
                            "today",
                            AppColors.SECONDARY
                        ),
                        self.create_stat_card(
                            "Próximas Citas",
                            str(self.upcoming_appointments),
                            "event",
                            AppColors.ACCENT
                        ),
                    ],
                    wrap=True,
                ),
                
                ft.Container(height=AppSpacing.MD),
                
                # Quick actions
                ft.Text("Acciones Rápidas", style=AppTheme.get_subtitle_style()),
                ft.Container(height=AppSpacing.SM),
                
                ft.Row(
                    controls=[
                        ft.ElevatedButton(
                            "Agregar Cliente",
                            icon="person_add",
                            on_click=lambda _: self.show_message("Funcionalidad: Agregar Cliente"),
                            style=ft.ButtonStyle(bgcolor=AppColors.PRIMARY),
                        ),
                        ft.ElevatedButton(
                            "Nueva Cita",
                            icon="event_note",
                            on_click=lambda _: self.show_message("Funcionalidad: Nueva Cita"),
                            style=ft.ButtonStyle(bgcolor=AppColors.SECONDARY),
                        ),
                        ft.ElevatedButton(
                            "Ver Clientes",
                            icon="list",
                            on_click=lambda _: self.show_message("Funcionalidad: Ver Clientes"),
                            style=ft.ButtonStyle(bgcolor=AppColors.ACCENT),
                        ),
                    ],
                    wrap=True,
                ),
                
                ft.Container(height=AppSpacing.LG),
                
                # Recent activity placeholder
                ft.Text("Actividad Reciente", style=AppTheme.get_subtitle_style()),
                ft.Container(height=AppSpacing.SM),
                
                ft.Card(
                    content=ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.ListTile(
                                    leading=ft.Icon("info", color=AppColors.INFO),
                                    title=ft.Text("Bienvenido a NutriAgenda"),
                                    subtitle=ft.Text("Sistema de gestión nutricional completo"),
                                ),
                            ],
                        ),
                        padding=AppSpacing.MD,
                    ),
                ),
            ],
            scroll=ft.ScrollMode.AUTO,
        )
    
    def create_stat_card(self, title: str, value: str, icon, color: str):
        """Create a statistics card"""
        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Icon(icon, size=40, color=color),
                        ft.Text(value, size=32, weight=ft.FontWeight.BOLD),
                        ft.Text(title, size=14, color=AppColors.TEXT_SECONDARY),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=AppSpacing.LG,
                width=180,
            ),
            elevation=2,
        )
    
    async def load_stats(self):
        """Load dashboard statistics"""
        try:
            # Get total clients
            clients = await client_service.get_clients_by_nutritionist(self.user_data['id'])
            self.total_clients = len(clients)
            
            # Get appointments for today
            today = date.today()
            appointments = await appointment_service.get_appointments_by_nutritionist(
                self.user_data['id'],
                start_date=today,
                end_date=today
            )
            self.appointments_today = len(appointments)
            
            # Get upcoming appointments
            all_appointments = await appointment_service.get_appointments_by_nutritionist(
                self.user_data['id']
            )
            self.upcoming_appointments = len([
                a for a in all_appointments
                if a.get('status') == 'scheduled' and a.get('date', datetime.now()).date() >= today
            ])
            
            # Update UI would go here in production
            # For now, stats are loaded but UI needs manual refresh
            self.page.update()
            
        except Exception as e:
            print(f"Error loading stats: {e}")
    
    def show_message(self, message: str):
        """Show a snackbar message"""
        self.page.snack_bar = ft.SnackBar(content=ft.Text(message))
        self.page.snack_bar.open = True
        self.page.update()
