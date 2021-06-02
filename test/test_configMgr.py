import os
import pkgutil
from typing import List
from appManagement import configMgr as cfg
from appManagement import message as msg

# ----
# Loads a configuration from a resource file and evaluates the parsed result.
# ----
def test_configMgrParse():
    config = cfg.ConfigMgr('')
    rsrc = pkgutil.get_data("test", "config_test_data.cfg")
    configContent, status = config.Parse(rsrc)
    assert status == True
    assert config.IsAuditError() == True
    messages = config.GetAudit()
    assert len(messages) == 5   
    assert auditContainsOnlyCodes(messages, [0,2008,5000]) == True

# ----
# Given a list of messages and expected message codes, this helper method returns FALSE if an unexpected code is found. Otherwise it returns TRUE.
# ----
def auditContainsOnlyCodes(messages: List[msg.Message], codes: List[int]) -> bool:
    for message in messages:
        if message.code not in codes:
            return False
    return True