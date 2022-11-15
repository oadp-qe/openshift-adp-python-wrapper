from pathlib import Path

import pytest
import yaml
from kubernetes.client import ApiException

from openshift_resources.model.velero import VolumeSnapshotLocation

path = str(Path(__file__).parent)


@pytest.fixture(scope='session')
def volume_snapshot_location_obj():
    with open(path + "/sample_output/volume_snapshot_location.json", "r") as volume_snapshot_location_json:
        volume_snapshot_location_json_str = volume_snapshot_location_json.read()
        volume_snapshot_location_dict = yaml.safe_load(volume_snapshot_location_json_str)
        yield VolumeSnapshotLocation.build_with_default_client(**volume_snapshot_location_dict)


def test_volume_snapshot_location_delete(volume_snapshot_location_obj):
    try:
        volume_snapshot_location_obj.delete()
    except ApiException:
        pass


def test_volume_snapshot_location_create(volume_snapshot_location_obj):
    volume_snapshot_location_obj.create()


def test_volume_snapshot_location_get(request, volume_snapshot_location_obj):
    obj = volume_snapshot_location_obj.get()
    request.addfinalizer(volume_snapshot_location_obj.delete)
    expected_name = 'test-volume-snapshot-location'
    assert obj.metadata.name == expected_name, f"Failed: VolumeSnapshotLocation's name is not {expected_name}; actual: {obj.metadata.name}"
