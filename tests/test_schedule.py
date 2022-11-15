from pathlib import Path

import pytest
import yaml
from kubernetes.client import ApiException

from openshift_resources.model.velero.schedule import Schedule

path = str(Path(__file__).parent)


@pytest.fixture(scope='session')
def schedule_obj():
    with open(path + "/sample_output/schedule.yaml", "r") as schedule_yaml:
        schedule_yaml_str = schedule_yaml.read()
        schedule_dict = yaml.safe_load(schedule_yaml_str)
        yield Schedule.build_with_default_client(**schedule_dict)


def test_backup_delete(schedule_obj):
    try:
        schedule_obj.delete()
    except ApiException:
        pass


def test_backup_create(schedule_obj):
    schedule_obj.create()


def test_backup_get(request, schedule_obj):
    obj = schedule_obj.get()
    request.addfinalizer(schedule_obj.delete)
    expected_name = 'test-schedule'
    assert obj.metadata.name == expected_name, f"Failed: schedule's name is not {expected_name}; actual: {obj.metadata.name}"


