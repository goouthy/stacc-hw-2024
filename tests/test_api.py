import pytest
from app.api import app

# Test client
@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()
    return client

# Testing the home page
def test_home(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Welcome to the Iris Dataset API" in response.data

# Testing the endpoints
def test_get_data(client):
    response = client.get('/dataset')
    assert response.status_code == 200
    assert b"All Data" in response.data

def test_get_summary(client):
    response = client.get('/summary')
    assert response.status_code == 200
    assert b"Full Summary Statistics" in response.data

def test_get_species_summary(client):
    response = client.get('/species_summary')
    assert response.status_code == 200
    assert b"Summary Statistics by Species" in response.data

def test_pairplot(client):
    response = client.get('/feature_pairplot')
    assert response.status_code == 200
    assert b"<img" in response.data 

def test_min_sepal_widths(client):
    response = client.get('/min_sepal_widths')
    assert response.status_code == 200
    assert b"Top 5 Smallest Sepal Width" in response.data

# Test a non-existent route
def test_nonexistent_route(client):
    response = client.get('/nonexistent')
    assert response.status_code == 404