from urllib import request, response
from django.test import RequestFactory, TestCase
import io
import ast
import json
from users.handlers import create, delete, getAUser, update, delete

a_user_to_create = {
    'username': 'toCreate',
    'email': 'an@email.fr',
    'first_name': 'first',
    'last_name': 'last',
    'password': 'pswd'
}

a_user_to_get = {
    'id': 2,
    'username': 'foobar',
    'first_name': 'foo',
    'last_name': 'bar',
    'email': 'foobar@hotmail.com',
    'is_active': True,
    'date_joined': '2022-04-25T21:50:32.229Z'
}

to_update = {
        "toPatch": {
            "last_name": "another last name"
    }
}

class UserTest(TestCase):
    fixtures = ['test_users.json']
    @classmethod
    def setUpTestData(cls):
        cls.factory = RequestFactory()

    def tearDown(self):
        pass

    def testCreateUserNormal(self): # we create en user in the "normal" way
        request = self.factory.post('/create/', a_user_to_create)
        response = create(request)
        fixed = response.content.replace(b"'", b'"')
        userCreated = json.load(io.BytesIO(fixed))
        self.assertEqual(userCreated['username'], a_user_to_create['username'])
        self.assertEqual(userCreated['email'], a_user_to_create['email'])
        self.assertEqual(userCreated['first_name'], a_user_to_create['first_name'])
        self.assertEqual(userCreated['last_name'], a_user_to_create['last_name'])

    def testCreateUserEmpty(self): # we pass an empty object
        request = self.factory.post('/create/', {})
        response = create(request)
        userCreated = json.loads(response.content.decode("UTF-8"))
        self.assertEqual(userCreated['name'], 'NoValueError')
        self.assertEqual(response.status_code, 400)

    def testGetUserNormal(self): # normal flow
        request = self.factory.get('/get/2')
        response = getAUser(request=request, id=2)
        fixed = response.content.replace(b"'", b'"')
        the_user = json.load(io.BytesIO(fixed))
        self.assertEqual(the_user['id'], a_user_to_get['id'])
        self.assertEqual(the_user['username'], a_user_to_get['username'])
        self.assertEqual(the_user['first_name'], a_user_to_get['first_name'])
        self.assertEqual(the_user['last_name'], a_user_to_get['last_name'])
        self.assertEqual(the_user['email'], a_user_to_get['email'])
        self.assertEqual(the_user['is_active'], a_user_to_get['is_active'])
        self.assertEqual(the_user['date_joined'], a_user_to_get['date_joined'])

    def testGetUserEmpty(self): # we want a user out of range
        request = self.factory.get('/get/7')
        response = getAUser(request=request, id=7)
        the_user = json.loads(response.content.decode("UTF-8"))
        self.assertEqual(the_user['name'],'DoesNotExist')
        self.assertEqual(response.status_code, 400)

    def testUpdateUserNormal(self): # normal flow
        request = self.factory.patch('/update/2', to_update)
        response = update(request=request, id=2)
        print(response.content)
        patched_user = json.loads(response.content.decode("UTF-8")) # ast.literal_eval not working here
        self.assertEqual(patched_user['last_name'], to_update['toPatch']['last_name'])

    def testUpdateUserWrongId(self): # we want a user out of range
        request = self.factory.patch('/get/7', to_update)
        response = update(request=request, id=7)
        test = response.content.decode("UTF-8")
        patched_user = ast.literal_eval(response.content.decode("UTF-8")) # json.loads not working...
        self.assertEqual(patched_user['name'],'DoesNotExist')
        self.assertEqual(response.status_code, 403)

    def testDeleteUserNormal(self):
        request = self.factory.delete('/delete/4')
        response = delete(request=request, id=4)
        self.assertEqual(response.status_code, 200)

    def testUpdateUserWrongId(self): # we want a user out of range
        request = self.factory.patch('/get/7', to_update)
        response = update(request=request, id=7)
        test = response.content.decode("UTF-8")
        patched_user = ast.literal_eval(response.content.decode("UTF-8")) # json.loads not working...
        self.assertEqual(patched_user['name'],'DoesNotExist')
        self.assertEqual(response.status_code, 403)
