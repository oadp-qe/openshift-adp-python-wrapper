import logging

from oadp_constants.resources import ApiGroups
from ocp_resources.resource import NamespacedResource

logger = logging.getLogger(__name__)


class ReplicationSource(NamespacedResource):
    api_group = ApiGroups.VOLSYC_API_GROUOP
