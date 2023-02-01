import io
import logging

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

    def __init__(self, resource_api_class, template_folder, namespace=None):
        self.environment = Environment(loader=FileSystemLoader(template_folder))
        self.resource_api_class = resource_api_class
        self.namespace = namespace

    def create(self,
               name,
               template,
               **kwargs):
        kwargs["name"] = name
        if self.namespace:
            kwargs["namespace"] = self.namespace

        resource_yaml_str = self.environment.get_template(name=template).render((), **kwargs)
        logger.info(f"Creating {self.resource_api_class.kind}/{name}")
        logger.info(resource_yaml_str)

        resource_api_kwargs = {
            "name": name,
            "yaml_file": io.StringIO(resource_yaml_str)
        }
        if self.namespace:
            resource_api_kwargs["namespace"] = self.namespace

        resource_api = self.resource_api_class(**resource_api_kwargs)
        resource_api.create(wait=True)

        return resource_api
