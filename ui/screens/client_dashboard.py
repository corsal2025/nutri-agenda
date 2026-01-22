"""
Client Dashboard Screen
"""
import flet as ft
from utils.theme import AppColors, AppSpacing, AppTheme
from services.auth_service import auth_service
from services.appointment_service import appointment_service
from services.measurement_service import measurement_service
from datetime import datetime


class ClientDashboard:
    """Dashboard for clients"""
    
    def __init__(self, page: ft.Page, user_data: dict, on_logout):
        self.page = page
        self.user_data = user_data
        self.on_logout = on_logout
        
        # Data
        self.next_appointment = None
        self.latest_measurement = None
        
        # Load data
        self.load_data()
    
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
                                        f"Cliente • {datetime.now().strftime('%d/%m/%Y')}",
                                        style=AppTheme.get_caption_style(),
                                    ),
                                ],
                                expand=True,
                            ),
                            ft.IconButton(
                                icon=ft.icons.LOGOUT,
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
                
                # Next appointment card
                ft.Text("Próxima Cita", style=AppTheme.get_subtitle_style()),
                ft.Container(height=AppSpacing.SM),
                
                self.create_appointment_card(),
                
                ft.Container(height=AppSpacing.MD),
                
                # Latest measurement card
                ft.Text("Última Medición", style=AppTheme.get_subtitle_style()),
                ft.Container(height=AppSpacing.SM),
                
                self.create_measurement_card(),
                
                ft.Container(height=AppSpacing.MD),
                
                # Quick actions
                ft.Text("Acciones", style=AppTheme.get_subtitle_style()),
                ft.Container(height=AppSpacing.SM),
                
                ft.Row(
                    controls=[
                        ft.ElevatedButton(
                            "Agendar Cita",
                            icon=ft.icons.EVENT_NOTE,
                            on_click=lambda _: self.show_message("Funcionalidad: Agendar Cita"),
                            style=ft.ButtonStyle(bgcolor=AppColors.PRIMARY),
                        ),
                        ft.ElevatedButton(
                            "Ver Progreso",
                            icon=ft.icons.TRENDING_UP,
                            on_click=lambda _: self.show_message("Funcionalidad: Ver Progreso"),
                            style=ft.ButtonStyle(bgcolor=AppColors.ACCENT),
                        ),
                    ],
                    wrap=True,
                ),
            ],
            scroll=ft.ScrollMode.AUTO,
        )
    
    def create_appointment_card(self):
        """Create next appointment card"""
        if self.next_appointment:
            apt_date = self.next_appointment.get('date', datetime.now())
            return ft.Card(
                content=ft.Container(
                    content=ft.ListTile(
                        leading=ft.Icon(ft.icons.EVENT, color=AppColors.PRIMARY),
                        title=ft.Text(f"Cita programada"),
                        subtitle=ft.Text(
                            f"{apt_date.strftime('%d/%m/%Y %H:%M')}\n"
                            f"Duración: {self.next_appointment.get('duration', 60)} minutos"
                        ),
                    ),
                    padding=AppSpacing.SM,
                ),
            )
        else:
            return ft.Card(
                content=ft.Container(
                    content=ft.ListTile(
                        leading=ft.Icon(ft.icons.INFO, color=AppColors.TEXT_SECONDARY),
                        title=ft.Text("No tienes citas programadas"),
                        subtitle=ft.Text("Agenda una cita con tu nutricionista"),
                    ),
                    padding=AppSpacing.SM,
                ),
            )
    
    def create_measurement_card(self):
        """Create latest measurement card"""
        if self.latest_measurement:
            weight = self.latest_measurement.get('weight', 0)
            bmi = self.latest_measurement.get('bmi', 0)
            measure_date = self.latest_measurement.get('date', datetime.now())
            
            return ft.Card(
                content=ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.ListTile(
                                leading=ft.Icon(ft.icons.SCALE, color=AppColors.SECONDARY),
                                title=ft.Text(f"Peso: {weight} kg"),
                                subtitle=ft.Text(
                                    f"IMC: {bmi}\n"
                                    f"Fecha: {measure_date.strftime('%d/%m/%Y')}"
                                ),
                            ),
                        ],
                    ),
                    padding=AppSpacing.SM,
                ),
            )
        else:
            return ft.Card(
                content=ft.Container(
                    content=ft.ListTile(
                        leading=ft.Icon(ft.icons.INFO, color=AppColors.TEXT_SECONDARY),
                        title=ft.Text("No hay mediciones registradas"),
                        subtitle=ft.Text("Tu nutricionista registrará tus mediciones"),
                    ),
                    padding=AppSpacing.SM,
                ),
            )
    
    async def load_data(self):
        """Load client data"""
        try:
            # Get next appointment
            appointments = await appointment_service.get_appointments_by_client(self.user_data['id'])
            upcoming = [a for a in appointments if a.get('status') == 'scheduled']
            if upcoming:
                self.next_appointment = upcoming[0]
            
            # Get latest measurement
            self.latest_measurement = await measurement_service.get_latest_measurement(self.user_data['id'])
            
            # Update UI
            self.content = self.build()
            self.page.update()
            
        except Exception as e:
            print(f"Error loading data: {e}")
    
    def show_message(self, message: str):
        """Show a snackbar message"""
        self.page.snack_bar = ft.SnackBar(content=ft.Text(message))
        self.page.snack_bar.open = True
        self.page.update()
