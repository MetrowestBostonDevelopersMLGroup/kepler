from appManagement import message as msg
import pandas as pd

class Audit:

    messages = []
    isErrorEncountered = False

    # info messages 0 - 2000
    INFO_START_AUDIT = msg.Message(0, 'Start audit.', 'Info')
    
    # warning messages 2001 - 4001
    WARNING_FILE_SECTION_DOES_NOT_CONTAIN_NA_FILTER = msg.Message(2001, 'One of the file sections does not define an na-filter property, a value of TRUE will be defaulted.','Warning')
    WARNING_FILE_SECTION_DOES_NOT_CONTAIN_COLUMNS_TO_DROP = msg.Message(2002, 'One of the file sections does not define columns to drop.','Warning')
    WARNING_FILE_SECTION_DOES_NOT_CONTAIN_COLUMNS_TO_RENAME = msg.Message(2003, 'One of the file sections does not define columns to rename.','Warning')

    #error messages 5000+
    ERROR_DATAFILE_NOT_UPLOADED = msg.Message(5000, 'This datafile has not been uploaded.','Error')
    ERROR_CONFIG_DOES_NOT_CONTAIN_FILE_SECTION = msg.Message(5001, 'The configuration file does not contain a file definition section.','Error')
    ERROR_FILE_SECTION_DOES_NOT_CONTAIN_FILENAME = msg.Message(5002, 'One of the file sections is missing a filename property.','Error')
    ERROR_FILE_SECTION_DOES_NOT_CONTAIN_WORKING_COLUMNS = msg.Message(5003, 'One of the file sections is missing a collection of working columns.','Error')
    ERROR_FILE_SECTION_EMPTY = msg.Message(5004, 'The file section of the configuration file is empty.','Error')
    ERROR_CONFIG_DOES_NOT_CONTAIN_TRANSFORM_SECTION = msg.Message(5005, 'The configuration file does not contain a transform definition section.','Error')
    ERROR_CONFIG_DOES_NOT_CONTAIN_ANALYZE_SECTION = msg.Message(5006, 'The configuration file does not contain an analyze definition section.','Error')

    ERROR_TRANSFORM_DROP_COLUMN_EXCEPTION = msg.Message(5007, 'An attempt to drop columns failed.','Error')
    ERROR_TRANSFORM_RENAME_COLUMN_EXCEPTION = msg.Message(5008, 'An attempt to rename columns failed.','Error')

    ERROR_TRANSFORM_SECTION_MERGE_MISSING_FROM_FILENAME = msg.Message(5009, 'Transform section merge property is missing the from-filename attribute.','Error')
    ERROR_TRANSFORM_SECTION_MERGE_MISSING_TO_FILENAME = msg.Message(5010, 'Transform section merge property is missing the to-filename attribute.','Error')
    ERROR_TRANSFORM_SECTION_MERGE_MISSING_ON_COLUMN = msg.Message(5011, 'Transform section merge property is missing the on-column attribute.','Error')

    def __init__(self):
        pass

    def AddMessage(self, message, extra):
        if (message.level =='Error'):
            self.isErrorEncountered = True

        message.extra = str(extra)
        self.messages.append(message)
        print(str(message.code)+' '+message.message+' '+message.extra)

    def IsErrorInAudit(self):
        return self.isErrorEncountered

    def MessagesAsHtmlTable(self):
        df = pd.DataFrame([t.__dict__ for t in self.messages ])
        return df.to_html()


