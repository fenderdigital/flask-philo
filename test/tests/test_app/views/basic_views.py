from flask import request
from flask_philo import app
from flask_philo.views import BaseView, BaseResourceView
from flask_philo.db.exceptions import NotFoundError
from tests.test_app.models import User

from tests.test_app.serializers import (
    GetUserSerializer, PostUserSerializer, PutUserSerializer
)


class BasicTemplateView(BaseView):
    def get(self, template_name='template1'):
        if 'template1' == template_name:
            tname = 'templates_1/index.html'
            data = {'msg_1': 'hello template1'}
        else:
            tname = 'templates_2/index.html'
            data = {'msg_2': 'hello template2'}
        return self.render_template(tname, **data)


class UserResourceView(BaseResourceView):

    def get(self, id=None):
        try:
            if not id:
                data = [
                    GetUserSerializer(model=user).to_json()
                    for user in User.objects.filter_by()
                ]
            else:
                data = GetUserSerializer(
                    model=User.objects.get(id=id)).to_json()

            return self.json_response(data=data)
        except NotFoundError as e:
            app.logger.error(e)
            return self.json_response(status=404)

        except Exception as e:
            app.logger.error(e)
            return self.json_response(status=400)

    def post(self):
        try:
            data = PostUserSerializer(request=request).to_json()
            user = User(**data)
            user.add()
            self.postgresql_pool.commit()
            user = User.objects.get(id=user.id)
            app.logger.info('user with id {} has been created'.format(user.id))
            return self.json_response(status=201, data={'id': user.id})

        except Exception as e:
            app.logger.error(e)
            self.postgresql_pool.rollback()
            return self.json_response(status=500)

    def put(self, id):
        try:
            serializer = PutUserSerializer(request=request)
            serializer.update()
            self.postgresql_pool.commit()
            return self.json_response(
                status=200, data=serializer.to_json())
        except Exception as e:
            app.logger.error(e)
            self.postgresql_pool.rollback()
            return self.json_response(status=500)

    def delete(self, id):
        try:
            user = User.objects.get(id=id)
            user.delete()
            self.postgresql_pool.commit()
            return self.json_response()
        except Exception as e:
            app.logger.error(e)
            self.postgresql_pool.rollback()
            return self.json_response(status=500)


class CorsResourceView(BaseResourceView):
    def get(self):
        return self.json_response(status=200, data={'cors': 'ok'})
