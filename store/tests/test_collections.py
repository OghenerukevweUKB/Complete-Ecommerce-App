from django.contrib.auth.models import User
from rest_framework import status
from store.models import Collection
from model_bakery import baker
from .conftest import authenticate
import pytest

@pytest.fixture
def create_collection(api_client):
    def do_create_collection(collection):
        return api_client.post('/store/collections/', collection) 
    return do_create_collection


@pytest.mark.django_db
class TestCreateCollection:
    def test_if_user_is_anonymous_returns_401(self,  create_collection):
        #Arrange

        #Act
        response = create_collection({'title':'a'})

        #Assert
        assert response.status_code ==status.HTTP_401_UNAUTHORIZED


    def test_if_user_is_not_admin_returns_403(self, authenticate,create_collection):
        #Arrange

        #Act
        authenticate()
        response = create_collection({'title':'a'})

        #Assert
      
        assert response.status_code ==status.HTTP_403_FORBIDDEN


    def test_if_data_is_invalid_returns_400(self, api_client, create_collection):
        #Arrange

        #Act
        authenticate(is_staff=True)
        response = create_collection({'title':''})

        #Assert
        assert response.status_code ==status.HTTP_400_BAD_REQUEST
        assert response.data['title'] is not None

    def test_if_data_is_valid_returns_201(self, create_collection):
        #Arrange

        #Act
        authenticate(is_staff=True)
        response = create_collection({'title':'a'})

        #Assert
        assert response.status_code ==status.HTTP_201_CREATED
        assert response.data['id'] > 0


@pytest.mark.django_db
class TestRetrieveCollection:
    def test_if_collection_exits_return_200(self, api_client):
        collection = baker.make(Collection)

        #act
        response = api_client.get(f'/store/collections/{collection.id}/')

        #assert
        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            'id':collection.id,
            'title':collection.title,
            'products_count':0
        }

         
    