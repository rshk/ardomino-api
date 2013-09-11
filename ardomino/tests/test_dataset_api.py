"""
Tests for the CKAN catalog API
"""

import json

import pytest

from ckan.catalog import db, app as ckan_app, Dataset


#@pytest.fixture(scope="module")
@pytest.fixture()
def app(request):
    """Create a clean database, return test client"""

    db.drop_all()
    db.create_all()

    def fin():
        db.drop_all()
        request.addfinalizer(fin)

    return ckan_app.test_client()


def test_dataset_crud(app):
    result = app.get('/api/1/dataset/')
    assert result.status_code == 200

    ## To check that this is valid JSON
    data = json.loads(result.data)

    ## Make sure the db is empty
    assert len(data) == 0

    ## Create dataset
    obj = {
        'name': 'example-dataset',
        'title': 'Example Dataset',
        'license': 'cc-zero',
    }
    result = app.post('/api/1/dataset/',
                      data=json.dumps(obj),
                      content_type='application/json')
    assert result.status_code == 200
    new_obj = json.loads(result.data)
    for key in obj:
        assert new_obj[key] == obj[key]

    ## Check that the inserted object is ok
    dbobj = Dataset.query.filter_by(id=new_obj['id']).one()
    assert dbobj.attributes['name'] == obj['name']

    ## Check that we have it in the datasets list
    result = app.get('/api/1/dataset/')
    assert result.status_code == 200
    data = json.loads(result.data)
    assert len(data) == 1
    assert new_obj['id'] == data[0]['id']

    dataset_url = '/api/1/dataset/{0}/'.format(new_obj['id'])

    ## Retrieve the dataset
    result = app.get(dataset_url)
    assert result.status_code == 200
    data = json.loads(result.data)
    assert data['id'] == new_obj['id']
    for key in ('name', 'title', 'license'):
        assert data[key] == obj[key]

    ## Put - full update
    upd_obj = obj.copy()
    upd_obj['license'] = 'cc-by-sa'
    app.put(dataset_url,
            data=json.dumps(upd_obj),
            content_type='application/json')
    result = app.get(dataset_url)
    assert result.status_code == 200
    data = json.loads(result.data)
    del data['id']
    assert data == upd_obj

    ## Patch - partial update
    app.patch(dataset_url,
              data=json.dumps({'title': 'EXAMPLE DATASET'}),
              content_type='application/json')
    result = app.get(dataset_url)
    assert result.status_code == 200
    data = json.loads(result.data)
    upd_obj['title'] = 'EXAMPLE DATASET'
    del data['id']
    assert data == upd_obj

    ## Patch - key addition
    app.patch(dataset_url,
              data=json.dumps({'new_item': 'New Value'}),
              content_type='application/json')
    upd_obj['new_item'] = 'New Value'
    result = app.get(dataset_url)
    assert result.status_code == 200
    data = json.loads(result.data)
    del data['id']
    assert data == upd_obj

    ## Patch - key deletion
    app.patch(dataset_url,
              data=json.dumps({'$del': ['title']}),
              content_type='application/json')
    del upd_obj['title']
    result = app.get(dataset_url)
    assert result.status_code == 200
    data = json.loads(result.data)
    del data['id']
    assert data == upd_obj

    ## Patch - key change using $set
    app.patch(dataset_url,
              data=json.dumps({'$set': {'new_item': 'Hello'}}),
              content_type='application/json')
    upd_obj['new_item'] = 'Hello'
    result = app.get(dataset_url)
    assert result.status_code == 200
    data = json.loads(result.data)
    del data['id']
    assert data == upd_obj

    ## Patch - invalid $operation
    result = app.patch(dataset_url,
                       data=json.dumps({'$invalid': []}),
                       content_type='application/json')
    assert result.status_code == 400

    ## Delete the dataset
    result = app.delete(dataset_url)
    assert result.status_code == 200

    ## Retrieve a non-existent Dataset
    result = app.get('/api/1/dataset/does-not-exist')
    assert result.status_code == 404
    # assert result.data == 'Requested object not found'


def test_dataset_pagination(app):
    """Test dataset list pagination"""
    ## Create a bunch of datasets

    for i in xrange(50):
        obj = {
            'name': 'example-dataset-{0}'.format(i),
            'title': 'Example Dataset #{0}'.format(i),
            'license': 'cc-zero',
        }
        result = app.post('/api/1/dataset/',
                          data=json.dumps(obj),
                          content_type='application/json')
        assert result.status_code == 200

    ## todo: check maximum page size
    ## todo: check Link headers (use python-requests to parse them?)
    ## todo: add support for, and check, headers with paging information

    ## First 50-items page
    result = app.get('/api/1/dataset/?page_size=50')
    all_data = data = json.loads(result.data)
    assert len(data) == 50

    ## First 10-items page
    result = app.get('/api/1/dataset/?page_size=10')
    data = json.loads(result.data)
    assert len(data) == 10
    assert data == all_data[:10]

    ## Second 10-items page
    result = app.get('/api/1/dataset/?page_size=10&page=1')
    data = json.loads(result.data)
    assert len(data) == 10
    assert data == all_data[10:20]

    ## Invalid page size
    result = app.get('/api/1/dataset/?page_size=NotANumber')
    assert result.status_code == 400

    ## Negative page size
    result = app.get('/api/1/dataset/?page_size=-1')
    assert result.status_code == 400

    ## Invalid page number
    result = app.get('/api/1/dataset/?page=NotANumber')
    assert result.status_code == 400

    ## Negative page number
    result = app.get('/api/1/dataset/?page=-1')
    assert result.status_code == 400

    ## Test out-of-range page
    result = app.get('/api/1/dataset/?page_size=10&page=5')
    assert result.status_code == 404
