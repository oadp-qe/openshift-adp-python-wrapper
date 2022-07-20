# Openshift APIs for Data Protection (OADP) Python Wrapper 

Interact with openshift adp operator customer resources 

Read more about OADP

https://access.redhat.com/articles/5456281


## Installation


```bash
git clone foobar
cd foobar
python setup.py install --user
```

## Usage

```python
import foobar
TBD
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

### Add new Resource
- OADP Operator handles both OADP and Velero Resource
- The Resource Handler Modules should be placed here:
   - openshift_resources/oadp_resource_kine.py # Kind: OadpResourceKind, OADP Resource.
   - openshift_resources/velero/velero_resource_kine.py # Kind: VeleroResourceKind, Velero Resource.
```python
class ResourceKind(Namesapceresource):
    pass
```



create a module name data_protection_application 



## License
[MIT](https://choosealicense.com/licenses/mit/)