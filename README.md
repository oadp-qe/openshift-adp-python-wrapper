# Openshift APIs for Data Protection (OADP) Python Client Wrapper 

Manage Openshift adp Custom Resources 

Depened on:

https://github.com/RedHatQE/openshift-python-wrapper


Read more about OADP



## Installation


```bash
# Install from repo
git clone https://github.com/oadp-qe/openshift-adp-python-wrapper
pip install <path to>/openshift-adp-python-wrapper
```

## Usage Example
### Creating a dpa CR, wait for a successful reconciliation and delete it. 
note: 
1. The j2 helper module includes a build-in filter for getting env variable values: `env_override`
2. NO Templates are not provided with this project.Please refer to OADP Documentation for more information. 

openshift_resource/oadp/data_protection_application
```python
# openshift_resource/oadp/data_protection_application
r = constants.resources
class DataProtectionApplication(NamespacedResource):
    api_group = r.OADP_API_GROUP

    def wait_for_successful_reconciliation(self):
        self.wait_for_condition(condition=r.CONDITION_RECONCILED, status=r.STATUS_SUC_RECONCILED)

    def wait_for_failed_reconciliation(self):
        self.wait_for_condition(condition=r.CONDITION_RECONCILED, status=r.STATUS_FAILED_TO_RECONCILE)
```
templates/awsdpa.j2
```yaml
apiVersion: oadp.openshift.io/v1alpha1
kind: DataProtectionApplication
metadata:
  namespace: {{ namespace }}
  name: {{ name }}
spec:
  configuration:
    velero:
      defaultPlugins:
      - openshift
      - azure
{% if enable_csi is defined and enable_csi %}
      - csi
{% endif %}
{% if enable_restic is defined  and enable_restic %}
    restic:
      enable:  {{ enable_restic  }}
{% endif }} 
  backupLocations:
    - name: default
      velero:
        provider: azure
        default: true
        objectStorage:
          bucket: {{ "missing-bucket-env" | env_override("BUCKET") }}
          prefix: velero
        credential:
        {% if credentials_secret_name is defined %}
          name: {{ credentials_secret_name }}
        {% else %}
          name: {{ "cloud-credentials-azure"  | env_override("CREDS_SECRET_REF") }}
        {% endif %}


          key: cloud
        config:
          resourceGroup: {{ "missing:" | env_override("AZURE_RESOURCE_GROUP")  }}
          storageAccount: {{ "missing:" | env_override("BUCKET") }}
          storageAccountKeyEnvVar: AZURE_STORAGE_ACCOUNT_ACCESS_KEY
          subscriptionId: {{ "missing:" | env_override("AZURE_SUBSCRIPTION_ID") }}

```

```python
# some_module.py
# In this example we expect KUBECONFIG to be set and point to the OADP cluster 
from openshift_resources.utils.openshift_resource_jinja2_based_builder import OpenshiftResourceJinja2BasedBuilder
from openshift_resources.model.oadp import DataProtectionApplication

dpa = OpenshiftResourceJinja2BasedBuilder(
  resource_api_class=DataProtectionApplication,
  template_folder="templates/",
  namespace="openshift-adp")
.create(
  name="dpa_name"
template = "awsdpa.j2",
           enable_restic = True,
                           enable_csi = True,
                                        enable_vsl = True)
dpa.wait_for_successful_reconciliation()
dpa.delete()


```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

### Add new Resource
- OADP Operator handles both OADP and Velero Resource
- The Resource Handler Modules should be placed here:
   - openshift_resources/oadp/oadp_api_group.py # Kind: OadpApiGroup (for example). Or
   - openshift_resources/velero/velero_resource_kine.py # Kind: VeleroApiGroup (again, just an example).
```python
# openshift_resources/oadp/oadp_api_group.py
class OadpApiGroup(Namesapceresource):
    pass

# openshift_resources/velero/velero_resource_kine.py
class VeleroApiGroup(Namesapceresource):
    pass

```


## License
[MIT](https://choosealicense.com/licenses/mit/)
