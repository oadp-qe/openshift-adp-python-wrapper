import json
from pathlib import Path

import pytest
from kubernetes.client import ApiException

from openshift_resources.model.oadp.datamover import VolumeSnapshotRestore

path = str(Path(__file__).parent)


@pytest.fixture(scope='session')
def volume_snapshot_restore_obj():
    with open(path + "/sample_output/volume_snapshot_restore.yaml", "r") as volume_snapshot_restore_json:
        volume_snapshot_restore_json_str = volume_snapshot_restore_json.read()
        volume_snapshot_restore_dict = json.loads(volume_snapshot_restore_json_str)
        yield VolumeSnapshotRestore.build_with_default_client(**volume_snapshot_restore_dict)


def test_volume_snapshot_restore_delete(volume_snapshot_restore_obj):
    try:
        volume_snapshot_restore_obj.delete()
    except ApiException:
        pass


def test_volume_snapshot_restore_create(volume_snapshot_restore_obj):
    volume_snapshot_restore_obj.create()


def test_volume_snapshot_restore_get(request, volume_snapshot_restore_obj):
    obj = volume_snapshot_restore_obj.get()
    request.addfinalizer(volume_snapshot_restore_obj.delete)
    expected_name = 'test-volume-snapshot-restore'
    assert obj.metadata.name == expected_name, f"Failed: VSR's name is not {expected_name}; actual: {obj.metadata.name}"


