"""
Measurement Service
Handles body measurements and progress tracking
"""
from typing import List, Dict, Any, Optional
from datetime import datetime
from services.firebase_config import firebase
import io
from PIL import Image


class MeasurementService:
    """Service for managing body measurements"""
    
    def __init__(self):
        self.db = firebase.db
        self.storage = firebase.storage
        self.collection = 'measurements'
    
    def calculate_bmi(self, weight: float, height: float) -> float:
        """Calculate BMI (Body Mass Index)"""
        if height <= 0:
            return 0.0
        return round(weight / ((height / 100) ** 2), 2)
    
    async def upload_photo(self, photo_bytes: bytes, client_id: str) -> Optional[str]:
        """Upload measurement photo to Firebase Storage"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"measurements/{client_id}/{timestamp}.jpg"
            
            blob = self.storage.blob(filename)
            blob.upload_from_string(photo_bytes, content_type='image/jpeg')
            blob.make_public()
            
            return blob.public_url
            
        except Exception as e:
            print(f"Error uploading photo: {e}")
            return None
    
    async def create_measurement(
        self,
        client_id: str,
        weight: float,
        height: float,
        waist: Optional[float] = None,
        hip: Optional[float] = None,
        body_fat: Optional[float] = None,
        muscle_mass: Optional[float] = None,
        notes: str = "",
        photos: Optional[List[bytes]] = None
    ) -> Dict[str, Any]:
        """
        Create a new measurement record
        
        Args:
            client_id: ID of the client
            weight: Weight in kg
            height: Height in cm
            waist: Waist measurement in cm
            hip: Hip measurement in cm
            body_fat: Body fat percentage
            muscle_mass: Muscle mass percentage
            notes: Additional notes
            photos: List of photo bytes
        
        Returns:
            Created measurement data
        """
        try:
            # Calculate BMI
            bmi = self.calculate_bmi(weight, height)
            
            # Upload photos if provided
            photo_urls = []
            if photos:
                for photo in photos:
                    url = await self.upload_photo(photo, client_id)
                    if url:
                        photo_urls.append(url)
            
            measurement_data = {
                'clientId': client_id,
                'date': datetime.now(),
                'weight': weight,
                'height': height,
                'bmi': bmi,
                'waist': waist,
                'hip': hip,
                'bodyFat': body_fat,
                'muscleMass': muscle_mass,
                'notes': notes,
                'photos': photo_urls,
                'createdAt': datetime.now()
            }
            
            doc_ref = self.db.collection(self.collection).document()
            measurement_data['id'] = doc_ref.id
            doc_ref.set(measurement_data)
            
            return {
                'success': True,
                'measurement': measurement_data,
                'message': 'Medición registrada exitosamente'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': f'Error al registrar medición: {str(e)}'
            }
    
    async def get_measurements_by_client(self, client_id: str) -> List[Dict[str, Any]]:
        """Get all measurements for a specific client"""
        try:
            measurements = []
            docs = self.db.collection(self.collection)\
                .where('clientId', '==', client_id)\
                .order_by('date', direction='DESCENDING')\
                .stream()
            
            for doc in docs:
                measurement_data = doc.to_dict()
                measurement_data['id'] = doc.id
                measurements.append(measurement_data)
            
            return measurements
            
        except Exception as e:
            print(f"Error getting measurements: {e}")
            return []
    
    async def get_latest_measurement(self, client_id: str) -> Optional[Dict[str, Any]]:
        """Get the most recent measurement for a client"""
        measurements = await self.get_measurements_by_client(client_id)
        return measurements[0] if measurements else None
    
    def get_measurement_stats(self, measurements: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate statistics from measurements"""
        if not measurements:
            return {}
        
        weights = [m['weight'] for m in measurements if 'weight' in m]
        bmis = [m['bmi'] for m in measurements if 'bmi' in m]
        
        return {
            'totalRecords': len(measurements),
            'weightChange': weights[0] - weights[-1] if len(weights) > 1 else 0,
            'averageBMI': sum(bmis) / len(bmis) if bmis else 0,
            'firstMeasurement': measurements[-1]['date'] if measurements else None,
            'latestMeasurement': measurements[0]['date'] if measurements else None
        }


# Global measurement service instance
measurement_service = MeasurementService()
