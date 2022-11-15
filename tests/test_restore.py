from pathlib import Path

import pytest
import yaml
from kubernetes.client import ApiException

from openshift_resources.velero.restore import Restore

path = str(Path(__file__).parent)


@pytest.fixture(scope='session')
def restore_obj():
    with open(path + "/sample_output/restore.yaml", "r") as restore_yaml:
        restore_yaml_str = restore_yaml.read()
        restore_dict = yaml.safe_load(restore_yaml_str)
        yield Restore.build_with_default_client(**restore_dict)


def test_restore_delete(restore_obj):
    try:
        restore_obj.delete()
    except ApiException:
        pass


def test_restore_create(restore_obj):
    restore_obj.create()


def test_restore_get(request, restore_obj):
    obj = restore_obj.get()
    request.addfinalizer(restore_obj.delete)
    expected_name = 'test-restore'
    assert obj.metadata.name == expected_name, f"Failed: restores's name is not {expected_name}; actual: {obj.metadata.name}"


