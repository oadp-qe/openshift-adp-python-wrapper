import json
from pathlib import Path
from openshift_resources.velero.backup import Backup

path = str(Path(__file__).parent)


def test_backup():
    # import sample Backup CR json
    with open(path + "/sample_output/backup.json", "r") as backup_json:
        backup_json_str = backup_json.read()
        backup_dict = json.loads(backup_json_str)

        # "deserialize" dict to Backup object
        b = Backup(**backup_dict)

        # "serialize" Backup object to dict
        b.dict()

