from openshift_resources.velero.backup import Backup


def test_backup():
    b = Backup.construct_backup("test")
    b.spec.includedNamespaces = ["mysql-persistent"]
    b.to_dict()
    b.delete(wait=True)
    b.create()
