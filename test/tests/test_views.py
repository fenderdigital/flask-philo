from flask_philo.test import FlaskTestCase

from tests.test_app.models import User
from decimal import Decimal
import json


class TestApiRequest(FlaskTestCase):

    def test_get_resource(self):
        """
        Get a Rest resource in json format
        """
        assert 0 == User.objects.count()
        user = User(
            username='username1', email='email1@email.com', password='123')
        user.add()

        user2 = User(
            username='username2', email='email2@email.com', password='123')
        user2.add()
        self.postgresql_pool.commit()
        result = self.client.get('/users/{}'.format(user.id))
        assert 200 == result.status_code
        data = json.loads(result.get_data().decode('utf-8'))
        assert 'username' in data
        assert 'id' in data
        assert user.id == data['id']

    def test_get_resource_list(self):
        """
        Get a list of rest resources
        """
        assert 0 == User.objects.count()
        user = User(
            username='username1', email='email1@email.com', password='123')
        user.add()

        user2 = User(
            username='username2', email='email2@email.com', password='123')
        user2.add()
        self.postgresql_pool.commit()
        result = self.client.get('/users')
        assert 200 == result.status_code
        data = json.loads(result.get_data().decode('utf-8'))
        assert len(data) == 2
        assert 'username' in data[0]
        assert 'id' in data[0]
        assert user.id == data[0]['id']
        assert user2.id == data[1]['id']

    def test_post_resource(self):
        """
        Test A valid
        """
        assert 0 == User.objects.count()
        user = {
            'username': 'user', 'email': 'email@test.com', 'password': '123'}
        response = self.client.post(
            '/users',
            data=json.dumps(user),
            headers=self.json_request_headers
        )
        self.postgresql_pool.commit()
        assert 1 == User.objects.count()
        assert 201 == response.status_code
        data = json.loads(response.get_data().decode('utf-8'))
        user2 = User.objects.filter_by()[0]
        assert data['id'] == user2.id

    def test_put_resource(self):
        """
        Test A valid put request
        """
        assert 0 == User.objects.count()
        user = User(
            username='username1', email='email1@email.com',
            password='123', credit_score=2.33)
        user.add()
        self.postgresql_pool.commit()
        data = {
            'id': user.id, 'username': 'updatedusername',
            'email': user.email, 'password': '123', 'credit_score': '10.44'}

        result = self.client.put(
            '/users/{}'.format(user.id),
            data=json.dumps(data),
            headers=self.json_request_headers
        )
        data = json.loads(result.get_data().decode('utf-8'))
        user2 = User.objects.get(id=user.id)

        assert 200 == result.status_code
        assert 1 == User.objects.count()
        assert user.id == user2.id and user2.id == data['id']
        assert round(user.credit_score, 2) == round(Decimal(2.33), 2)
        assert round(user2.credit_score, 2) == round(Decimal(10.44), 2)

    def test_delete_resource(self):
        """
        deleting a resource using delete
        """
        assert 0 == User.objects.count()
        user = User(
            username='username1', email='email1@email.com', password='123')
        user.add()
        self.postgresql_pool.commit()
        assert 1 == User.objects.count()
        result = self.client.delete(
            '/users/{}'.format(user.id),
            headers=self.json_request_headers
        )
        assert 200 == result.status_code
        assert 0 == User.objects.count()

    def test_cors(self):
        result = self.client.get('/cors-api/test-cors')
        assert 'Access-Control-Allow-Origin' in result.headers
        cors_val = result.headers['Access-Control-Allow-Origin']
        assert 'FLASK_PHILO_TEST_CORS' == cors_val
