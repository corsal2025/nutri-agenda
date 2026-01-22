"""
Appointment Management Service
Handles scheduling and management of appointments
"""
from typing import List, Dict, Any, Optional
from datetime import datetime, date
from services.firebase_config import firebase


class AppointmentService:
    """Service for managing appointments"""
    
    def __init__(self):
        self.db = firebase.db
        self.collection = 'appointments'
    
    async def create_appointment(
        self,
        client_id: str,
        nutritionist_id: str,
        appointment_date: datetime,
        duration: int = 60,
        notes: str = ""
    ) -> Dict[str, Any]:
        """
        Create a new appointment
        
        Args:
            client_id: ID of the client
            nutritionist_id: ID of the nutritionist
            appointment_date: Date and time of appointment
            duration: Duration in minutes
            notes: Additional notes
        
        Returns:
            Created appointment data
        """
        try:
            appointment_data = {
                'clientId': client_id,
                'nutritionistId': nutritionist_id,
                'date': appointment_date,
                'duration': duration,
                'status': 'scheduled',  # scheduled, completed, cancelled, no-show
                'notes': notes,
                'createdAt': datetime.now(),
                'updatedAt': datetime.now()
            }
            
            doc_ref = self.db.collection(self.collection).document()
            appointment_data['id'] = doc_ref.id
            doc_ref.set(appointment_data)
            
            return {
                'success': True,
                'appointment': appointment_data,
                'message': 'Cita creada exitosamente'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': f'Error al crear cita: {str(e)}'
            }
    
    async def get_appointments_by_nutritionist(
        self,
        nutritionist_id: str,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> List[Dict[str, Any]]:
        """Get appointments for a nutritionist, optionally filtered by date range"""
        try:
            appointments = []
            query = self.db.collection(self.collection)\
                .where('nutritionistId', '==', nutritionist_id)
            
            if start_date:
                query = query.where('date', '>=', start_date)
            if end_date:
                query = query.where('date', '<=', end_date)
            
            docs = query.stream()
            
            for doc in docs:
                appointment_data = doc.to_dict()
                appointment_data['id'] = doc.id
                appointments.append(appointment_data)
            
            return sorted(appointments, key=lambda x: x['date'])
            
        except Exception as e:
            print(f"Error getting appointments: {e}")
            return []
    
    async def get_appointments_by_client(self, client_id: str) -> List[Dict[str, Any]]:
        """Get all appointments for a specific client"""
        try:
            appointments = []
            docs = self.db.collection(self.collection)\
                .where('clientId', '==', client_id)\
                .stream()
            
            for doc in docs:
                appointment_data = doc.to_dict()
                appointment_data['id'] = doc.id
                appointments.append(appointment_data)
            
            return sorted(appointments, key=lambda x: x['date'])
            
        except Exception as e:
            print(f"Error getting appointments: {e}")
            return []
    
    async def update_appointment_status(
        self,
        appointment_id: str,
        status: str
    ) -> Dict[str, Any]:
        """Update appointment status"""
        try:
            self.db.collection(self.collection).document(appointment_id).update({
                'status': status,
                'updatedAt': datetime.now()
            })
            
            return {
                'success': True,
                'message': 'Estado de cita actualizado'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': f'Error al actualizar cita: {str(e)}'
            }
    
    async def cancel_appointment(self, appointment_id: str) -> Dict[str, Any]:
        """Cancel an appointment"""
        return await self.update_appointment_status(appointment_id, 'cancelled')


# Global appointment service instance
appointment_service = AppointmentService()
