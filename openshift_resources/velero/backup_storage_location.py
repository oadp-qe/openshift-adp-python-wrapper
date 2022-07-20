from ocp_resources.resource import NamespacedResource


class BackupStorageLocation(NamespacedResource):

    def wait_for_status_available(self):
        self.wait_for_status("Available")

    def wait_for_status_unavailable(self):
        self.wait_for_status("Unavailable")
