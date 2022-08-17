import io
import logging
import os
import subprocess

from jinja2 import Environment, FileSystemLoader

logger = logging.getLogger(__name__)


class OpenshiftResourceJinja2BasedBuilder:
    """
    Create Openshift Resources
    based on jinja2 templates to create a resource manifest.

    Build-in Filters:
        env_override(<name>): get the value of the environment variable <name>

    Args:
        resource_api_class: openshift resource class
        template_folder: root folder for j2 templates
        namespace: for all resource created by an instance of this class
    """

    @staticmethod
    def env_override(value, key):
        return os.getenv(key, value)

    def __init__(self, resource_api_class, template_folder, namespace):
        self.environment = Environment(loader=FileSystemLoader(template_folder))
        self.resource_api_class = resource_api_class
        self.namespace = namespace

        self.environment.filters['env_override'] = self.env_override

    def remove_and_create(self,
                          name,
                          template,
                          **kwargs):
        kwargs["name"] = name
        kwargs["namespace"] = self.namespace

        resource_yaml_str = self.environment.get_template(name=template).render((), **kwargs)
        logger.info(f"Re-Creating {self.resource_api_class}/{name}")
        logger.info(resource_yaml_str)
        resource_api = self.resource_api_class(
            # do not remove.
            name=name,
            namespace=self.namespace,
            #
            yaml_file=io.StringIO(resource_yaml_str))

        resource_api.delete()

        resource_api.create(wait=True)

        return resource_api
