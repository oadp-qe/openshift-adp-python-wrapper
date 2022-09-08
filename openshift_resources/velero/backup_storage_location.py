from ocp_resources.resource import NamespacedResource
import wrapper_constants.resources as r


class BackupStorageLocation(NamespacedResource):

    def wait_for_status_available(self):
        self.wait_for_status(r.STATUS_AVAILABLE)

    def wait_for_status_unavailable(self):
        self.wait_for_status(r.STATUS_UNAVAILABLE)
