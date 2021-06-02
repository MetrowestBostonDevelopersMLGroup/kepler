import pytest_mock 
from appManagement import dataFile as df
from appManagement import configMgr as cfg
from engine import transform as xf
from appManagement import audit as au

def test_mocking_class_transform_method(mocker):

    def mock_MergeDataFiles(self, configMgr: cfg.ConfigMgr):
        data = df.DataFile('json','uploaddir', au.Audit())
        return data

    mocker.patch(
        'engine.transform.Transform.MergeDataFiles',
        mock_MergeDataFiles
    )

    transformer = xf.Transform()    
    config = cfg.ConfigMgr('')
    datafileOutput = transformer.MergeDataFiles(config)
    assert(datafileOutput is not None)
