"""
Authentication Service
Handles user login, registration, and session management
"""
from typing import Optional, Dict, Any
from datetime import datetime
from services.firebase_config import firebase


class AuthService:
    """Service for user authentication"""
    
    def __init__(self):
        self.db = firebase.db
        self.current_user = None
        self.demo_mode = firebase.demo_mode
        
        # Demo users for testing
        self.demo_users = {
            'nutri@test.com': {
                'id': 'demo-nutri-1',
                'email': 'nutri@test.com',
                'password': 'test123',
                'name': 'Dr. Juan Nutricionista',
                'phone': '+54 9 11 1234-5678',
                'role': 'nutritionist',
                'createdAt': datetime.now(),
                'updatedAt': datetime.now()
            },
            'cliente@test.com': {
                'id': 'demo-client-1',
                'email': 'cliente@test.com',
                'password': 'test123',
                'name': 'María Cliente',
                'phone': '+54 9 11 8765-4321',
                'role': 'client',
                'createdAt': datetime.now(),
                'updatedAt': datetime.now()
            }
        }
    
    async def register(
        self,
        email: str,
        password: str,
        name: str,
        phone: str,
        role: str  # 'nutritionist' or 'client'
    ) -> Dict[str, Any]:
        """
        Register a new user
        
        Args:
            email: User email
            password: User password
            name: User full name
            phone: User phone number
            role: User role (nutritionist/client)
        
        Returns:
            User data dictionary
        """
        try:
            # Create user in Firebase Auth
            user = firebase.auth.create_user(
                email=email,
                password=password,
                display_name=name
            )
            
            # Store user data in Firestore
            user_data = {
                'id': user.uid,
                'email': email,
                'name': name,
                'phone': phone,
                'role': role,
                'createdAt': datetime.now(),
                'updatedAt': datetime.now()
            }
            
            self.db.collection('users').document(user.uid).set(user_data)
            
            return {
                'success': True,
                'user': user_data,
                'message': 'Usuario registrado exitosamente'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': f'Error al registrar usuario: {str(e)}'
            }
    
    async def login(self, email: str, password: str) -> Dict[str, Any]:
        """
        Login user (simplified version - requires Firebase REST API for full auth)
        
        Note: Firebase Admin SDK doesn't support email/password login directly.
        For production, use Firebase REST API or Firebase Client SDK.
        """
        try:
            # DEMO MODE: Use demo users
            if self.demo_mode:
                if email in self.demo_users:
                    demo_user = self.demo_users[email]
                    if demo_user['password'] == password:
                        user_data = {k: v for k, v in demo_user.items() if k != 'password'}
                        self.current_user = user_data
                        return {
                            'success': True,
                            'user': user_data,
                            'message': 'Login exitoso (DEMO MODE)'
                        }
                
                return {
                    'success': False,
                    'message': 'Email o contraseña incorrectos (DEMO: nutri@test.com / cliente@test.com, password: test123)'
                }
            
            # FIREBASE MODE: Real authentication
            # Get user by email
            user = firebase.auth.get_user_by_email(email)
            
            # Get user data from Firestore
            user_doc = self.db.collection('users').document(user.uid).get()
            
            if user_doc.exists:
                user_data = user_doc.to_dict()
                user_data['id'] = user.uid
                self.current_user = user_data
                
                return {
                    'success': True,
                    'user': user_data,
                    'message': 'Login exitoso'
                }
            else:
                return {
                    'success': False,
                    'message': 'Usuario no encontrado en la base de datos'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': f'Error al iniciar sesión: {str(e)}'
            }
    
    def logout(self):
        """Logout current user"""
        self.current_user = None
    
    def get_current_user(self) -> Optional[Dict[str, Any]]:
        """Get current logged in user"""
        return self.current_user
    
    def is_authenticated(self) -> bool:
        """Check if user is authenticated"""
        return self.current_user is not None
    
    def is_nutritionist(self) -> bool:
        """Check if current user is a nutritionist"""
        return self.current_user and self.current_user.get('role') == 'nutritionist'
    
    def is_client(self) -> bool:
        """Check if current user is a client"""
        return self.current_user and self.current_user.get('role') == 'client'


# Global auth service instance
auth_service = AuthService()
