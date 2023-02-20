import logging
from enum import Enum

from oadp_constants.resources import ApiGroups
from ocp_resources.resource import NamespacedResource

logger = logging.getLogger(__name__)


class ReplicationDestination(NamespacedResource):
    api_group = ApiGroups.VOLSYC_API_GROUOP.value

    class Label(Enum):
        VOLUME_SNAPSHOT_RESTORE = "datamover.oadp.openshift.io/vsr"
