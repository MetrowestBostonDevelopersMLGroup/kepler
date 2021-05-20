import os
import pkgutil
from appManagement import configMgr as cfg

def test_configMgrParse():
    config = cfg.ConfigMgr('')
    rsrc = pkgutil.get_data("test", "config_test_data.cfg")
    audit, status = config.Parse(rsrc)
    pass