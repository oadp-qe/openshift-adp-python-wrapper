import io
import logging

from utils.misc import run_shell_cmd

from jinja2 import Environment, FileSystemLoader

logger = logging.getLogger(__name__)

class OADPResource:
    """
    Manage Openshift Resources
    Managing Resources, using external j2 templates to create a resource manifest.
    Args:
        oadp_resource_api_class: openshift resource class
        template_folder: root folder for j2 templates
        settings: template var values to always use when Creating a Resource (For Example: Bucket  Name, Region, etc.)
    """

    def __init__(self, oadp_resource_api_class, template_folder, settings):
        self.environment = Environment(loader=FileSystemLoader(template_folder))
        self.settings = settings
        self.oadp_resource_api_class = oadp_resource_api_class

    def create(self,
               name,
               namespace,
               template,
               remove_first=True,
               **kwargs):
        logger.info(f"Trying to create kwargs['Kind'] {name} in {namespace}...")

        kwargs["name"] = name
        kwargs["namespace"] = namespace
        resource_api = self.oadp_resource_api_class(
            # when using a yaml file (Path to file or StringIO), as we do here, the name & namespace values are taken
            # form the passed yaml
            name=None,
            namespace=None,
            #
            yaml_file=io.StringIO(self.environment
                                  .get_template(name=template)
                                  .render(self.settings, **kwargs)))
        if remove_first:
            cmd = f"oc delete -n {namespace}  {resource_api.kind}/{name} --ignore-not-found=true --wait=true"
            run_shell_cmd(cmd)

        resource_api.create(wait=True)

        return resource_api
