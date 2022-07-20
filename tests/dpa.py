import json

from jinja2 import Environment, FileSystemLoader
from openshift_resources.oadp.data_protection_application import DataProtectionApplication


class Dpa:
    def __init__(self, template_folder, template, settings):
        self.environment = Environment(loader=FileSystemLoader(template_folder))
        self.template = self.environment.get_template(template)
        self.settings = settings

    def create(self,
               name,
               namespace,
               remove_first=True,
               **kwargs):
        kwargs["name"] = name
        kwargs["namespace"] = namespace

        dpa_api = DataProtectionApplication(name=name, namespace=namespace)
        if remove_first:
            dpa_api.delete(wave=True)

        return dpa_api.create(body=self.template.render(self.settings, **kwargs))


if __name__ == "__main__":
    settings = json.load(
        open("/home/amos/git/oadp-e2e-qe/output_files/api-oadp-14190-qe-devcluster-openshift-com:6443/settings.json"))
    settings_args = {"default_plugings": settings["spec"]["configuration"]["velero"]["defaultPlugins"],
                     "backup_location_provider": settings["spec"]["backupLocations"][0]["velero"]["provider"],
                     "backup_location_bucket": settings["spec"]["backupLocations"][0]["velero"]["objectStorage"][
                         "bucket"],
                     "backup_location_region": settings["spec"]["backupLocations"][0]["velero"]["config"]["region"],
                     "snapshot_location_provider": settings["spec"]["snapshotLocations"][0]["velero"]["provider"],
                     "snapshot_location_region": settings["spec"]["snapshotLocations"][0]["velero"]["config"]["region"],
                     "snapshot_location_profile": settings["spec"]["snapshotLocations"][0]["velero"]["config"][
                         "profile"]}
    dap = Dpa(
        template_folder="/home/amos/git/openshift-oadp-python-wrapper/tests/templates/",
        template="awss3dpa.j2",
        settings=settings_args

    )

    dap.create(name="ff", namespace="ttt", remove_first=True,
               enable_restic=True,
               enable_csi=True,
               enable_vsl=True,
               enable_data_mover=False)
