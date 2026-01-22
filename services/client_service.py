"""
Client Management Service
Handles CRUD operations for clients
"""
from typing import List, Dict, Any, Optional
from datetime import datetime
from services.firebase_config import firebase


class ClientService:
    """Service for managing nutrition clients"""
    
    def __init__(self):
        self.db = firebase.db
        self.collection = 'clients'
    
    async def create_client(
        self,
        nutritionist_id: str,
        personal_info: Dict[str, Any],
        medical_history: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Create a new client
        
        Args:
            nutritionist_id: ID of the nutritionist
            personal_info: Personal information (name, email, phone, birthDate, gender, etc.)
            medical_history: Medical history data
        
        Returns:
            Created client data
        """
        try:
            client_data = {
                'nutritionistId': nutritionist_id,
                'personalInfo': personal_info,
                'medicalHistory': medical_history,
                'createdAt': datetime.now(),
                'updatedAt': datetime.now()
            }
            
            # Add to Firestore
            doc_ref = self.db.collection(self.collection).document()
            client_data['id'] = doc_ref.id
            doc_ref.set(client_data)
            
            return {
                'success': True,
                'client': client_data,
                'message': 'Cliente creado exitosamente'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': f'Error al crear cliente: {str(e)}'
            }
    
    async def get_clients_by_nutritionist(self, nutritionist_id: str) -> List[Dict[str, Any]]:
        """Get all clients for a specific nutritionist"""
        try:
            clients = []
            docs = self.db.collection(self.collection)\
                .where('nutritionistId', '==', nutritionist_id)\
                .stream()
            
            for doc in docs:
                client_data = doc.to_dict()
                client_data['id'] = doc.id
                clients.append(client_data)
            
            return clients
            
        except Exception as e:
            print(f"Error getting clients: {e}")
            return []
    
    async def get_client_by_id(self, client_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific client by ID"""
        try:
            doc = self.db.collection(self.collection).document(client_id).get()
            
            if doc.exists:
                client_data = doc.to_dict()
                client_data['id'] = doc.id
                return client_data
            
            return None
            
        except Exception as e:
            print(f"Error getting client: {e}")
            return None
    
    async def update_client(
        self,
        client_id: str,
        updates: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update client information"""
        try:
            updates['updatedAt'] = datetime.now()
            
            self.db.collection(self.collection).document(client_id).update(updates)
            
            return {
                'success': True,
                'message': 'Cliente actualizado exitosamente'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': f'Error al actualizar cliente: {str(e)}'
            }
    
    async def delete_client(self, client_id: str) -> Dict[str, Any]:
        """Delete a client"""
        try:
            self.db.collection(self.collection).document(client_id).delete()
            
            return {
                'success': True,
                'message': 'Cliente eliminado exitosamente'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': f'Error al eliminar cliente: {str(e)}'
            }
    
    def calculate_age(self, birth_date: datetime) -> int:
        """Calculate age from birth date"""
        today = datetime.now()
        age = today.year - birth_date.year
        
        if (today.month, today.day) < (birth_date.month, birth_date.day):
            age -= 1
        
        return age


# Global client service instance
client_service = ClientService()
