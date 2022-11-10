from pathlib import Path

import pytest
import yaml
from kubernetes.client import ApiException

from openshift_resources.oadp.datamover.volume_snapshot_backup import VolumeSnapshotBackup

path = str(Path(__file__).parent)


@pytest.fixture(scope='session')
def volume_snapshot_backup_obj():
    with open(path + "/sample_output/volume_snapshot_backup.yaml", "r") as volume_snapshot_backup_json:
        volume_snapshot_backup_json_str = volume_snapshot_backup_json.read()
        volume_snapshot_backup_dict = yaml.safe_load(volume_snapshot_backup_json_str)
        yield VolumeSnapshotBackup.build_with_default_client(**volume_snapshot_backup_dict)


def test_volume_snapshot_backup_delete(volume_snapshot_backup_obj):
    try:
        volume_snapshot_backup_obj.delete()
    except ApiException:
        pass


def test_volume_snapshot_backup_create(volume_snapshot_backup_obj):
    volume_snapshot_backup_obj.create()


def test_volume_snapshot_backup_get(request, volume_snapshot_backup_obj):
    obj = volume_snapshot_backup_obj.get()
    request.addfinalizer(volume_snapshot_backup_obj.delete)
    expected_name = 'test-volume-snapshot-backup'
    assert obj.metadata.name == expected_name, f"Failed: VSB's name is not {expected_name}; actual: {obj.metadata.name}"


