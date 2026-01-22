"""
Firebase Configuration and Initialization
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Check if Firebase should be initialized
DEMO_MODE = os.getenv('DEMO_MODE', 'true').lower() == 'true'

if not DEMO_MODE:
    try:
        import firebase_admin
        from firebase_admin import credentials, auth, firestore, storage
    except ImportError:
        print("Warning: firebase_admin not installed")
        DEMO_MODE = True


class FirebaseConfig:
    """Firebase configuration singleton"""
    
    _instance = None
    _initialized = False
    demo_mode = DEMO_MODE
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            if not self.demo_mode:
                self._initialize_firebase()
            else:
                print("⚠️  Running in DEMO MODE - Firebase not configured")
                print("   To use Firebase, create .env file with credentials")
            FirebaseConfig._initialized = True
    
    def _initialize_firebase(self):
        """Initialize Firebase Admin SDK"""
        try:
            # Check if already initialized
            firebase_admin.get_app()
        except ValueError:
            try:
                # Priority 1: Environment variable with JSON content (Cloud Run)
                firebase_cred_json = os.getenv('FIREBASE_CREDENTIALS')
                
                if firebase_cred_json:
                    print("🔧 Loading Firebase credentials from environment variable...")
                    import json
                    cred = credentials.Certificate(json.loads(firebase_cred_json))
                    
                # Priority 2: Path to JSON file
                elif os.getenv('FIREBASE_ADMIN_CREDENTIALS'):
                    cred_path = os.getenv('FIREBASE_ADMIN_CREDENTIALS')
                    if os.path.exists(cred_path):
                        print(f"🔧 Loading Firebase credentials from file: {cred_path}")
                        cred = credentials.Certificate(cred_path)
                    else:
                        raise FileNotFoundError(f"Firebase credentials file not found: {cred_path}")
                
                # Priority 3: Default file location
                elif os.path.exists('./firebase-admin-key.json'):
                    print("🔧 Loading Firebase credentials from ./firebase-admin-key.json")
                    cred = credentials.Certificate('./firebase-admin-key.json')
                
                # Priority 4: Environment variables (individual fields)
                else:
                    print("🔧 Loading Firebase credentials from environment variables...")
                    cred = credentials.Certificate({
                        "type": "service_account",
                        "project_id": os.getenv('FIREBASE_PROJECT_ID'),
                        "private_key_id": os.getenv('FIREBASE_PRIVATE_KEY_ID'),
                        "private_key": os.getenv('FIREBASE_PRIVATE_KEY', '').replace('\\n', '\n'),
                        "client_email": os.getenv('FIREBASE_CLIENT_EMAIL'),
                        "client_id": os.getenv('FIREBASE_CLIENT_ID'),
                        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                        "token_uri": "https://oauth2.googleapis.com/token",
                        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                    })
                
                firebase_admin.initialize_app(cred, {
                    'storageBucket': os.getenv('FIREBASE_STORAGE_BUCKET')
                })
                print("✅ Firebase initialized successfully")
            except Exception as e:
                print(f"⚠️  Firebase initialization failed: {e}")
                print("   Switching to DEMO MODE")
                self.demo_mode = True
    
    @property
    def auth(self):
        """Get Firebase Auth instance"""
        if self.demo_mode:
            return None
        return auth
    
    @property
    def db(self):
        """Get Firestore instance"""
        if self.demo_mode:
            return None
        return firestore.client()
    
    @property
    def storage(self):
        """Get Storage instance"""
        if self.demo_mode:
            return None
        return storage.bucket()


# Global instance
firebase = FirebaseConfig()
