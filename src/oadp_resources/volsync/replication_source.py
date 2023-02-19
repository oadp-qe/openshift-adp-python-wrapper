import logging
from enum import Enum

from oadp_constants.resources import ApiGroups
from ocp_resources.resource import NamespacedResource

logger = logging.getLogger(__name__)


class ReplicationSource(NamespacedResource):
    api_group = ApiGroups.VOLSYC_API_GROUOP.value

    class Label(Enum):
        VOLUME_SNAPSHOT_BACKUP = "datamover.oadp.openshift.io/vsb"




