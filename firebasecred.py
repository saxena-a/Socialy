import pyrebase

# config = {
#     'apiKey': "AIzaSyAkm91_OXj1eI4T7n2ShBeT6USbbXXAHbM",
#     'authDomain': "socialy-ba2a2.firebaseapp.com",
#     'databaseURL': "https://socialy-ba2a2-default-rtdb.firebaseio.com",
#     'projectId': "socialy-ba2a2",
#     'storageBucket': "socialy-ba2a2.appspot.com",
#     'messagingSenderId': "305271560533",
#     'appId': "1:305271560533:web:93da5448ae9d87963d37dc",
#     'measurementId': "G-F8KXRWGWW7"
# }

config = {
'apiKey': "AIzaSyDW_jsI3hW8nJG8qBkUMfx-3079AdQd1zA",
    'authDomain': "socially-b481b.firebaseapp.com",
    'projectId': "socially-b481b",
    'storageBucket': "socially-b481b.appspot.com",
    'messagingSenderId': "859048523837",
    'appId': "1:859048523837:web:cf71436685da89bcdd1254",
    'measurementId': "G-X6452SSB2P",
    'databaseURL': "https://socially-b481b-default-rtdb.asia-southeast1.firebasedatabase.app/"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()