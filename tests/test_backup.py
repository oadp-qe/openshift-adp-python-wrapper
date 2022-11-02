import json
from pathlib import Path

import pytest
from kubernetes.client import ApiException

from openshift_resources.velero.backup import Backup

path = str(Path(__file__).parent)


@pytest.fixture(scope='session')
def backup_obj():
    with open(path + "/sample_output/backup_wo_api_version.json", "r") as backup_json:
        backup_json_str = backup_json.read()
        backup_dict = json.loads(backup_json_str)
        yield Backup.build_with_default_client(**backup_dict)


def test_backup_delete(backup_obj):
    try:
        backup_obj.delete()
    except ApiException:
        pass


def test_backup_create(backup_obj):
    backup_obj.create()


def test_backup_get(request, backup_obj):
    obj = backup_obj.get()
    request.addfinalizer(backup_obj.delete)
    assert obj.metadata.name == 'test-backup', f"Failed: backup's name is not test-backup; actual: {obj.metadata.name}"


