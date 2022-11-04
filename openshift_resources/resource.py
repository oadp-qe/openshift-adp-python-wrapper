import logging
from abc import ABCMeta
from datetime import datetime, timedelta
from time import sleep
from typing import Optional, Any

from ocp_resources.resource import _get_client, _get_api_version
from pydantic import BaseModel, Field
from resources.io.k8s.apimachinery.pkg.apis.meta.v1 import ObjectMeta

logger = logging.getLogger(__name__)


class BaseResource(BaseModel, metaclass=ABCMeta):
    # fields included in the resource manifests; those fields could be "serialized"/"deserialized"
    apiVersion: Optional[str]
    kind: Optional[str]
    metadata: Optional[ObjectMeta]

    # excluded from the resource manifests
    dyn_client: Optional[Any] = Field(exclude=True, repr=False, description="Represents the client of the resource")
    api_group: Optional[str] = Field(exclude=True, repr=False, description="Represents the API group of the resource")

    @property
    def resource_client(self):
        if not self.dyn_client:
            self.set_client()

        if not self.apiVersion:
            self.discover_api_version()

        if not self.kind:
            self.discover_kind()

        return self.dyn_client.resources.get(api_version=self.apiVersion, kind=self.kind)

    def discover_api_version(self):
        """
        discover API version dynamically from the cluster
        :return:
        """
        if not self.apiVersion:
            self.apiVersion = _get_api_version(
                dyn_client=self.dyn_client, api_group=self.api_group, kind=self.kind
            )

    def discover_kind(self):
        if not self.kind:
            self.kind = self.__class__.__name__

    def set_client(self, client=None, config_file=None, context=None):
        """
        Set a new DynamicClient
        :param client: the DynamicClient to set. Will initialize a new DynamicClient object in case it's None
        :param config_file: path to a kubeconfig file. Default value is either KUBECONFIG or ~/.kube/config if KUBECONFIG is not set
        :param context: name of the context to use. Default value is the one used from the config file
        :return:
        """
        if not client:
            self.dyn_client = _get_client(
                config_file=config_file, context=context
            )
        else:
            self.dyn_client = client

    def create(self, **kwargs):
        """
        Create the resource
        :param kwargs: check https://github.com/kubernetes-client/python-base/blob/master/dynamic/client.py#L114 for available options
        :return: returns the dict passed as argument
        # """
        # exclude all these fields from metadata and status to avoid error upon creation
        body = self.dict(exclude={'metadata': {'resourceVersion',
                                               'selfLink',
                                               'ownerReferences',
                                               'uid',
                                               'generation',
                                               'creationTimestamp'}
            , 'status': ...}, exclude_none=True)
        return self.resource_client.create(body=body, namespace=self.metadata.namespace, **kwargs)

    def get(self, **kwargs):
        """
        Get the resource
        :param kwargs: check https://github.com/kubernetes-client/python-base/blob/master/dynamic/client.py#L114 for available options
        :return: returns a deserialized representation of the resource (self)
        """
        resp = self.resource_client.get(name=self.metadata.name, namespace=self.metadata.namespace, **kwargs)
        # easiest way I found to deserialize it
        # FIXME: if you have a better solution
        self.__init__(**resp.to_dict())

        # FIXME: not sure what to return here
        return self

    def delete(self, **kwargs):
        """
        Delete the resource
        :param kwargs: check https://github.com/kubernetes-client/python-base/blob/master/dynamic/client.py#L121 for available options
        :return:
        """
        return self.resource_client.delete(name=self.metadata.name, namespace=self.metadata.namespace, **kwargs)

    # TODO: need to update the object itself too
    def replace(self, **kwargs):
        return self.resource_client.replace(name=self.metadata.name, namespace=self.metadata.namespace, **kwargs)

    # TODO: need to update the object itself too
    def patch(self, **kwargs):
        return self.resource_client.patch(name=self.metadata.name, namespace=self.metadata.namespace, **kwargs)

    @classmethod
    def build_with_default_client(cls, **kwargs):
        """
        Returns a new instance BaseResource assuming the config file is either KUBECONFIG or ~/.kube/config
        and the context is the one used from the config file
        :param kwargs: the attributes to initialize the BaseResource object with.
        :return: New instance of BaseResource
        """
        new_resource_builder = cls(**kwargs)
        new_resource_builder.set_client()
        new_resource_builder.discover_kind()
        new_resource_builder.discover_api_version()
        return new_resource_builder

    def wait_for_status_phase(self, status_phase, exit_phases=[], timeout=240, wait_interval=1):
        """
        Wait for a given status.phase value.
        Return true when found and the last status phase sample.
        Return False is the status.phase is in exit_phases Or after timeing out (, last status phase sample.)
        """

        logger.info(f"wait for {self.kind}/{self.name} in namespace {self.namespace} status phase to be {status_phase}")
        logger.info(f"exit phases: {exit_phases}")
        start_time = datetime.now()
        end_time = start_time + timedelta(seconds=timeout)
        timed_out = False
        current_status_phase = None
        while not timed_out:
            #TODO: return is not dict
            current_status_phase = self.get("status", {"phase": None}).get("phase")
            logger.info(f"current status phase: {current_status_phase}")
            if current_status_phase == status_phase:
                return True, current_status_phase
            if current_status_phase in exit_phases:
                logger.info(f"last status {current_status_phase} is found in exit phase list.")
                return False, current_status_phase
            logger.info(f"sleeping for {timeout} seconds...")
            sleep(wait_interval)
            timed_out = (end_time < datetime.now())

        logger.info(f"time out waiting for status phase: {status_phase}")
        return False, current_status_phase
