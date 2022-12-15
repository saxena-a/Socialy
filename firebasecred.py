import pyrebase

config = {
    'apiKey': "AIzaSyAkm91_OXj1eI4T7n2ShBeT6USbbXXAHbM",
    'authDomain': "socialy-ba2a2.firebaseapp.com",
    'databaseURL': "https://socialy-ba2a2-default-rtdb.firebaseio.com",
    'projectId': "socialy-ba2a2",
    'storageBucket': "socialy-ba2a2.appspot.com",
    'messagingSenderId': "305271560533",
    'appId': "1:305271560533:web:93da5448ae9d87963d37dc",
    'measurementId': "G-F8KXRWGWW7"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()