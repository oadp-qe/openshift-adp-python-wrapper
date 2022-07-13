import logging

import kubernetes
from openshift.dynamic import DynamicClient

from data_protection_application import DataProtectionApplication




if __name__ == "__main__":
    client = DynamicClient(client=kubernetes.config.new_client_from_config())

    with DataProtectionApplication(
            credientials=cred
            objectstrore=objstr,
            config=cnf) as dpa:
            dpa.wait_for_recosilidation()
            pass

