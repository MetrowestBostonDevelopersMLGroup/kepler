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
    WARNING_VECTORIZER_SECTION_MISSING_STOPWORDS = msg.Message(2004, 'Analyze section vectorize collection missing stop-words attribute. English will be the default stop words value.','Warning')
    WARNING_COMBINE_COLUMN_MISSING_ITEM_COUNT_ATTRIBUTE = msg.Message(2005, 'Files section combine column collection missing item-count attribute. The entire column contents will be combined by default.','Warning')
    WARNING_COMBINE_COLUMN_MISSING_DROP_SOURCE_COLUMNS_ATTRIBUTE = msg.Message(2006, 'Files section combine column collection missing drop-source-columns attribute. The source columns will be dropped by default.','Warning')
    WARNING_WORKING_COLUMN_MISSING_ITEM_COUNT_ATTRIBUTE = msg.Message(2007, 'Working column section JSON column missing item-count attribute. The entire column contents will be extracted by default.','Warning')

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

    ERROR_WORKING_COLUMN_MISSING_HEADER_ATTRIBUTE = msg.Message(5012, 'Working column property is missing the header attribute.','Error')
    ERROR_WORKING_COLUMN_IS_JSON_ATTRIBUTE = msg.Message(5013, 'Working column property is-json attribute should be a boolean.','Error')

    ERROR_ANALYZE_SECTION_MISSING_VECTORIZERS = msg.Message(5014, 'Analyze section missing vectorize collection.','Error')
    ERROR_VECTORIZER_SECTION_MISSING_ID  = msg.Message(5015, 'Analyze section vectorize collection missing id attribute.','Error')
    ERROR_VECTORIZER_SECTION_MISSING_VECTORIZER  = msg.Message(5016, 'Analyze section vectorize collection missing vectorizer attribute.','Error')
    ERROR_VECTORIZER_SECTION_MISSING_COLUMN  = msg.Message(5017, 'Analyze section vectorize collection missing column attribute.','Error')

    ERROR_COMBINE_COLUMN_MISSING_COMBINE_HEADER_ATTRIBUTE = msg.Message(5018, 'Files section combine column collection missing column-header attribute.','Error')
    ERROR_COMBINE_COLUMN_MISSING_COLUMN1_ATTRIBUTE = msg.Message(5019, 'Files section combine column collection missing column1 attribute.','Error')
    ERROR_COMBINE_COLUMN_MISSING_COLUMN2_ATTRIBUTE = msg.Message(5020, 'Files section combine column collection missing column2 attribute.','Error')

    ERROR_WORKING_COLUMN_MISSING_EXTRACT_ELEMENT_ATTRIBUTE = msg.Message(5021, 'Working column property is missing the extract-element attribute for this JSON define column.','Error')

    ERROR_COMBINE_COLUMN1_NOT_WORKING_COLUMN = msg.Message(5022, 'Working column collection does not contain merge column1: ','Error')
    ERROR_COMBINE_COLUMN2_NOT_WORKING_COLUMN = msg.Message(5023, 'Working column collection does not contain merge column2: ','Error')

    ERROR_ANALYZE_SECTION_NOT_CONTAIN_SPARSE_STACK = msg.Message(5024, 'The analyze section is missing the sparse-stack collection: ','Error')
    ERROR_SPARSE_STACK_SECTION_MISSING_ID = msg.Message(5025, 'The sparse-stack collection record is missing the id attribute.','Error')
    ERROR_SPARSE_STACK_SECTION_MISSING_STACK_TYPE = msg.Message(5026, 'The sparse-stack collection record is missing the stack-type attribute','Error')
    ERROR_SPARSE_STACK_SECTION_MISSING_STACK_FORMAT = msg.Message(5027, 'The sparse-stack collection record is missing the format attribute','Error')
    ERROR_SPARSE_STACK_SECTION_MISSING_VECT_MATRIX_IDS = msg.Message(5028, 'The sparse-stack collection record is missing the vectorized-matrix-ids attribute','Error')
    ERROR_ANALYZE_SECTION_NOT_CONTAIN_METRICS = msg.Message(5029, 'The analyze section is missing the metrics section.','Error')
    ERROR_ANALYZE_METRICS_MISSING_SIMILARITY = msg.Message(5030, 'The metrics section is missing the similarity attribute.','Error')

    ERROR_CONFIG_DOES_NOT_CONTAIN_RECOMMEND_SECTION = msg.Message(5031, 'The configuration file is missing a recommend section.','Error')
    ERROR_RECOMMEND_SECTION_MISSING_REQUEST_COLUMN_ATTRIBUTE = msg.Message(5032, 'The recommend section is missing the request-column attribute.','Error')
    ERROR_RECOMMEND_SECTION_MISSING_RESPONSE_COUNT_ATTRIBUTE = msg.Message(5033, 'The recommend section is missing the response-count attribute.','Error')
    ERROR_RECOMMEND_SECTION_MISSING_RESPONSE_COLUMNS = msg.Message(5034, 'The recommend section is missing the response-columns collection.','Error')
    ERROR_RECOMMEND_SECTION_MISSING_SOURCE_COLUMN = msg.Message(5035, 'The response-columns collection is missing the source attribute.','Error')
    ERROR_RECOMMEND_SECTION_MISSING_OUTPUT_COLUMN = msg.Message(5036, 'The response-columns collection is missing the output attribute.','Error')


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


