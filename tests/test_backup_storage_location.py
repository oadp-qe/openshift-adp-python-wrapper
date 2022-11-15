import json
from pathlib import Path

import pytest
from kubernetes.client import ApiException

from openshift_resources.model.velero.backup_storage_location import BackupStorageLocation

path = str(Path(__file__).parent)


@pytest.fixture(scope='session')
def backup_storage_location_obj():
    with open(path + "/sample_output/backup_storage_location.json", "r") as backup_storage_location_json:
        backup_storage_location_json_str = backup_storage_location_json.read()
        backup_storage_location_dict = json.loads(backup_storage_location_json_str)
        yield BackupStorageLocation.build_with_default_client(**backup_storage_location_dict)


def test_backup_storage_location_delete(backup_storage_location_obj):
    try:
        backup_storage_location_obj.delete()
    except ApiException:
        pass


def test_backup_storage_location_create(backup_storage_location_obj):
    backup_storage_location_obj.create()


def test_backup_storage_location_get(request, backup_storage_location_obj):
    obj = backup_storage_location_obj.get()
    request.addfinalizer(backup_storage_location_obj.delete)
    expected_name = "test-backup-storage-location"
    assert obj.metadata.name == expected_name, f"Failed: BSL's name is not {expected_name}; actual: {obj.metadata.name}"


