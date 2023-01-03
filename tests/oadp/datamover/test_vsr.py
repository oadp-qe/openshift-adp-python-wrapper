import os
from pathlib import Path

import pytest as pytest

from oadp_resources.oadp.datamover.volume_snapshot_restore import VolumeSnapshotRestore

path_to_tests_dir = str(Path(__file__).parent.parent.parent)


@pytest.fixture(scope='session')
def vsr_obj():
    yaml_path = os.path.join(path_to_tests_dir, "sample_input/vsr.yaml")
    vsr = VolumeSnapshotRestore(yaml_file=yaml_path)
    vsr.create()
    yield vsr
    vsr.delete()


def test_vsr_get(vsr_obj):
    obj = list(vsr_obj.get())[0].instance
    expected_name = 'vsr-for-test'
    assert obj.metadata.name == expected_name, f"Failed: VolumeSnapshotRestore's name is not {expected_name}; actual: {obj.metadata.name}"


def test_get_vsrs_by_restore_name():
    assert VolumeSnapshotRestore.get_vsrs_by_restore_name("test-849-9hqms") is not None


def test_get_vsrs_by_source_pvc():
    assert VolumeSnapshotRestore.get_vsrs_by_source_pvc("cassandra-data-cassandra-1")

    assert not VolumeSnapshotRestore.get_vsrs_by_source_pvc("cassandra-data-cassandra-2")


def test_is_vsr_done(vsr_obj):
    assert not vsr_obj.is_done()
