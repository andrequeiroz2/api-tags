import firebase_admin
from firebase_admin import credentials


#Connect to firebase
cred = credentials.Certificate('fbAdminConfig.json')
firebase = firebase_admin.initialize_app(cred)
