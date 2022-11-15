from unittest.mock import MagicMock

import pytest
from kubernetes.client import Configuration, ApiClient, V1Namespace, V1NamespaceList
from pydantic_factories import ModelFactory

from kubernetes_pydantic.conftest import DUMMY_NAMESPACE, asyncresult_return_value

from openshift_resources.model.velero.backup import Backup
from openshift_resources.velero import BackupApi
from wrapper_constants.resources import ApiGroups


@pytest.fixture
def backup_cr(meta) -> Backup:
    class Factory(ModelFactory):
        __model__ = Backup
        apiVersion = f"{ApiGroups.VELERO_API_GROUP.value}/v1"
        kind = __model__.__name__
        metadata = meta

    return Factory.build()


@pytest.mark.asyncio
async def test_custom_object_create(backup_cr):
    api = BackupApi.new(namespace=DUMMY_NAMESPACE, config=MagicMock(Configuration), client=MagicMock(ApiClient))

    ret_val = asyncresult_return_value(backup_cr.dict())
    api.core.api.custom.create_namespaced_custom_object = MagicMock(return_value=ret_val)

    res = await api.create(backup_cr)
    api.core.api.custom.create_namespaced_custom_object.assert_called_once_with(
        ApiGroups.VELERO_API_GROUP.value, "v1", DUMMY_NAMESPACE, "backups", backup_cr.dict(), async_req=True
    )
    assert res == (backup_cr, None)


@pytest.mark.asyncio
async def test_custom_object_merge(backup_cr):
    api = BackupApi.new(namespace=DUMMY_NAMESPACE, config=MagicMock(Configuration), client=MagicMock(ApiClient))

    ret_val = asyncresult_return_value(backup_cr.dict())
    api.core.api.custom.patch_namespaced_custom_object = MagicMock(return_value=ret_val)

    res = await api.merge(backup_cr.metadata.name, backup_cr)
    api.core.api.custom.patch_namespaced_custom_object.assert_called_once_with(
        ApiGroups.VELERO_API_GROUP.value, "v1", DUMMY_NAMESPACE, "backups", backup_cr.metadata.name, backup_cr.dict(), async_req=True
    )
    assert res == (backup_cr, None)


@pytest.mark.asyncio
async def test_custom_object_replace(backup_cr):
    api = BackupApi.new(namespace=DUMMY_NAMESPACE, config=MagicMock(Configuration), client=MagicMock(ApiClient))

    ret_val = asyncresult_return_value(backup_cr.dict())
    api.core.api.custom.replace_namespaced_custom_object = MagicMock(return_value=ret_val)

    res = await api.replace(backup_cr.metadata.name, backup_cr)
    api.core.api.custom.replace_namespaced_custom_object.assert_called_once_with(
        ApiGroups.VELERO_API_GROUP.value, "v1", DUMMY_NAMESPACE, "backups", backup_cr.metadata.name, backup_cr.dict(), async_req=True
    )
    assert res == (backup_cr, None)


@pytest.mark.asyncio
async def test_custom_object_delete(backup_cr):
    api = BackupApi.new(namespace=DUMMY_NAMESPACE, config=MagicMock(Configuration), client=MagicMock(ApiClient))

    ret_val = asyncresult_return_value(backup_cr.dict())
    api.core.api.custom.delete_namespaced_custom_object = MagicMock(return_value=ret_val)

    res = await api.delete(backup_cr.metadata.name)
    api.core.api.custom.delete_namespaced_custom_object.assert_called_once_with(
        ApiGroups.VELERO_API_GROUP.value, "v1", DUMMY_NAMESPACE, "backups", backup_cr.metadata.name, async_req=True
    )
    assert res is None


@pytest.mark.asyncio
async def test_custom_object_get(backup_cr):
    api = BackupApi.new(namespace=DUMMY_NAMESPACE, config=MagicMock(Configuration), client=MagicMock(ApiClient))

    ret_val = asyncresult_return_value(backup_cr.dict())
    api.core.api.custom.get_namespaced_custom_object = MagicMock(return_value=ret_val)

    res = await api.get(backup_cr.metadata.name)
    api.core.api.custom.get_namespaced_custom_object.assert_called_once_with(
        ApiGroups.VELERO_API_GROUP.value, "v1", DUMMY_NAMESPACE, "backups", backup_cr.metadata.name, async_req=True
    )
    assert res == (backup_cr, None)


@pytest.mark.asyncio
async def test_custom_object_list(backup_cr):
    api = BackupApi.new(namespace=DUMMY_NAMESPACE, config=MagicMock(Configuration), client=MagicMock(ApiClient))

    ret_val = asyncresult_return_value({"items": [backup_cr.dict()]})
    api.core.api.custom.list_namespaced_custom_object = MagicMock(return_value=ret_val)

    res = await api.list()
    api.core.api.custom.list_namespaced_custom_object.assert_called_once_with(
        ApiGroups.VELERO_API_GROUP.value, "v1", DUMMY_NAMESPACE, "backups", async_req=True
    )
    assert res == ([backup_cr], None)
