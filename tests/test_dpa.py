import json
import pytest
from pathlib import Path
from kubernetes.client import ApiException
from openshift_resources.oadp.data_protection_application import DataProtectionApplication

path = str(Path(__file__).parent)


@pytest.fixture(scope='session')
def dpa_obj():
    with open(path + "/sample_output/dpa.json", "r") as dpa_json:
        dpa_json_str = dpa_json.read()
        dpa_dict = json.loads(dpa_json_str)
        yield DataProtectionApplication.build_with_default_client(**dpa_dict)


def test_dpa_delete(dpa_obj):
    try:
        dpa_obj.delete()
    except ApiException:
        pass


def test_dpa_create(dpa_obj):
    dpa_obj.create()


def test_dpa_get(request, dpa_obj):
    obj = dpa_obj.get()
    request.addfinalizer(dpa_obj.delete)
    assert obj.metadata.name == 'test-dpa', f"Failed: dpa's name is not test-dpa; actual: {obj.metadata.name}"
