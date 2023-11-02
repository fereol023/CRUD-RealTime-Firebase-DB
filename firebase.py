#import pyrebase ### ou autre chose selon vos possibilités (firestore, bucket google cloud, etc.)
#sinon utilisez l'interface Admin
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
# voir aussi  : tutoriel ici https://firebase.google.com/docs/database/admin/start?hl=fr

class FirebaseClient:
    def __init__(self):
        '''
            Configure Firebase avec les informations d'authentification de votre projet
        '''
        self.config_path = 'config.json'
        self.database_url = 'https://mydatabase-93b44-default-rtdb.europe-west1.firebasedatabase.app/'
        try : 
            cred = credentials.Certificate(self.config_path)
            firebase_admin.initialize_app(cred, {
                'databaseURL': self.database_url
            })
        except Exception as e:
            print("Erreur lors de l'initialisation de la connexion.")
            raise e

    def create_user(self, uid: str, user_data: dict = None) -> None:
        '''
            Ajoutez un nouvel utilisateur à la base de données Firebase
            @params uid : Identifiant de l'utilisateur
            @params user_data : Données de l'utilisateur (un dictionnaire)

            @return: None
        '''
        try : 
            ref = db.reference('users')
            ref.child(uid).set(user_data)
            print(f'{uid} created !')
        except Exception as e:
            print(f"Erreur lors de l'enregistrement de l'utilisateur {uid} : {user_data}")
            raise e

    def read_user(self, uid: str) -> dict:
        '''
          Lisez les données de l'utilisateur à partir de la base de données Firebase
          @params uid : Identifiant de l'utilisateur

          @return: Données de l'utilisateur (un dictionnaire)
        '''
        ref = db.reference('users')
        user_data = ref.child(uid).get()
        return user_data

    def update_user(self, uid: str, user_data: dict = None) -> None:
        ''' 
            Mettez à jour les données de l'utilisateur dans la base de données Firebase
            @params uid : Identifiant de l'utilisateur
            @params user_data : Données de l'utilisateur à mettre à jour (un dictionnaire)     

            @return: None
        '''
        ref = db.reference('users')
        ref.child(uid).update(user_data)
        print(f'{uid} updated !')

    def delete_user(self, uid: str) -> None:
        '''
            Supprimez l'utilisateur de la base de données Firebase
            @params uid : Identifiant de l'utilisateur

            @return: None
        '''
        ref = db.reference('users')
        ref.child(uid).delete()
        print(f'{uid} deleted !')


if __name__ == "__main__":

    ''' 
        Q1 : Créez des nouveaux utilisateurs (from UserAccount.csv)
    '''
    import pandas as pd
    users_data = pd.read_csv('UsersAccount.csv')
    single_user = users_data.head(1).to_dict(orient='records')[0]
    single_user_id = single_user['uid']
    single_user_data = {k:v for k,v in single_user.items() if k != 'uid'}


    f = FirebaseClient()
    f.create_user(uid=single_user_id, user_data=single_user_data)

    ''' 
        Q2 : Lisez les données de l'utilisateur
    '''
    f.read_user(uid=single_user_id)

    '''
        Q3 : Mettez à jour les données de l'utilisateur
    '''
    # tech addict au lieu de nature lover
    new_data = {'name': 'Alice', 'birthday': '1990-05-15', 'bio': 'Tech addict', 'joindate': '2022-01-10'}
    f.update_user(uid=single_user_id, 
                  user_data=new_data)

 
    '''
        Q4 : Supprimez l'utilisateur
    '''
    f.delete_user(uid=single_user_id)
