import io
import json
import logging
import os
import pytest
import tempfile

from oadp_resource import OADPResource
from openshift_resources.oadp.data_protection_application import DataProtectionApplication
from openshift_resources.velero.backup_storage_location import BackupStorageLocation
from utils.misc import run_shell_cmd

logger = logging.getLogger(__name__)


def create_credentials_secret(name, namespace, credentials_file_path):
    if run_shell_cmd(f"oc delete secret/{name} --ignore-not-found") != 0:
        pytest.fail(f"something went wrong when trying to delete secret {name} in namespace {namespace}")

    cmd = f"oc create secret generic {name} -n {namespace} " \
          f"--from-file cloud={credentials_file_path}"
    if run_shell_cmd(cmd) != 0:
        pytest.fail(f"something went wrong when trying to create secret {name} in namespace {namespace}")


def update_credentials_secret(name, namespace, credentials_file_path):
    cmd = f"oc create secret generic {name} -n {namespace} " \
          f"--from-file cloud={credentials_file_path} " \
          f"--dry-run -o yaml | oc replace -f -"

    run_shell_cmd(cmd)


@pytest.fixture(scope="session")
def dpa_api_face():
    setting_file = os.environ.get("SETTINGS_FILE")
    template_folder = os.environ.get("RESOURCE_TEMPLATES_FOLDER", "testdata/templates/")
    provider = os.environ.get("PROVIDER")
    settings = json.load(
        open(setting_file))
    settings_args = \
        {"default_plugings": settings["spec"]["configuration"]["velero"]["defaultPlugins"],
         "backup_location_provider": settings["spec"]["backupLocations"][0]["velero"]["provider"],
         "backup_location_bucket": settings["spec"]["backupLocations"][0]["velero"]["objectStorage"][
             "bucket"],
         "backup_location_region": settings["spec"]["backupLocations"][0]["velero"]["config"]["region"],
         "snapshot_location_provider": settings["spec"]["snapshotLocations"][0]["velero"]["provider"],
         "snapshot_location_region": settings["spec"]["snapshotLocations"][0]["velero"]["config"]["region"],
         "snapshot_location_profile": settings["spec"]["snapshotLocations"][0]["velero"]["config"][
             "profile"]}

    return OADPResource(
        oadp_resource_api_class=DataProtectionApplication,
        template_folder=template_folder,
        settings=settings_args

    )


@pytest.mark.runme
def test_reconciliation_should_be_triggered_by_secret_change(dpa_api_face, tmpdir):
    oadp_namespace = "openshift-adp"
    provider = os.environ.get("PROVIDER")
    credentials_file = os.environ.get("CREDENTIALS_FILE")
    template = f"{provider}dpa.j2"
    dpa_name = "triggered-by-secret-change"
    credentials_secret_name = "start-with-empty-credentials"
    create_credentials_secret(name=credentials_secret_name, namespace=oadp_namespace,
                              credentials_file_path=tempfile.NamedTemporaryFile(delete=False).name)
    dap_api = \
        dpa_api_face \
            .create(name=dpa_name, namespace=oadp_namespace, remove_first=True,
                    template=template,
                    credentials_secret_name=credentials_secret_name,
                    enable_restic=True,
                    enable_csi=True,
                    enable_vsl=False)

    dap_api.wait_for_failed_reconciliation()

    bsl_api = next(BackupStorageLocation.get(name=f"{dpa_name}-1", namespace=oadp_namespace))
    bsl_api.wait_for_status_unavailable()

    update_credentials_secret(name=credentials_secret_name, namespace=oadp_namespace,
                              credentials_file_path=credentials_file)

    dap_api.wait_for_successful_reconciliation()
    bsl_api.wait_for_status_available()

#
# def deploy_sql_application():
#     os.system("applications/deploy_sql.sh")


# def test_back_vsl():
#     provider = "awss3"
#     run_config = pyconfig
#
#     # Provider Credentials
#     create_credentials_secret("credentials")
#     # Create DPA CR
#     #   Load template
#     dpa_dict = yaml.safe_load(open(
#         f"../openshift_resources/templates/oadp.openshift.io/v1alpha1/dpa/providers/{provider}/awss3dpa.yaml"))
#
#     #   Set values from configuration file
#     dpa_dict["spec"]["backupLocations"][0]["velero"]["objectStorage"]["bucket"] = "oadpbucket124695"
#     dpa = DataProtectionApplication(
#         name="test-1",
#         namespace="openshift-adp",
#         resource_dict=dpa_dict)
#     #    Create the CR
#     dpa.create(wait=True)
#     #    Wait for DPA reconciliation
#     dpa.wait_for_condition(condition="Reconciled", status="True")
#     #    Wait for Velero Resources reconciliation
#     next(BackupStorageLocation.get(name="test-1-1", namespace="openshift-adp")) \
#         .wait_for_status(status="Available")
#     # Start the Backup
#     bu_dict = yaml.safe_load(open("../openshift_resources/templates/velero.io/v1/backup.yaml"))
#     bu = Backup(
#         name="test-1",
#         namespace="openshift-adp",
#         resource_dict=bu_dict
#     )
#     bu.create()
#
#     # Wait for for backup to complete
#     bu.wait_for_status(status="Completed")
