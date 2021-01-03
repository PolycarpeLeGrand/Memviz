from pathlib import Path

# Data paths
base_storage_path = Path('C:/Users/Sanchez/Desktop/m3data')
topic_model_name = 'topics_80_2_02_100_3_50_2k'

METADATA_DF_PATH = base_storage_path / 'corpusframes/metadata_corpusframe.p'
LEXICON_DF_PATH = base_storage_path / 'corpusframes/lexicon_corpusframe.p'

LEXCATS_TEXTS_DF_PATH = base_storage_path / 'analysis/lexcats/lexcats_texts_3_df.p'
LEXCATS_ABS_DF_PATH = base_storage_path / 'analysis/lexcats/lexcats_abs_3_df.p'
LEXCATS_PARAS_DF_PATH = base_storage_path / 'analysis/lexcats/lexcats_paras_3_df.p'
LEXCATS_CSV_PATH = base_storage_path / 'csvs/lexcats_3.csv'

TOPIC_WORDS_DF_PATH = base_storage_path / 'analysis/LDA' / topic_model_name / 'topic_words_df.p'
DOC_TOPICS_DF_PATH = base_storage_path / 'analysis/LDA' / topic_model_name / 'doc_topics_df.p'
TOPIC_REDUCTIONS_DF_PATH = base_storage_path / 'analysis/LDA' / topic_model_name / 'reductions_df.p'
VIZ_DICTS_PATH = base_storage_path / 'viz_dicts'


# Ip details when test server is run on public mode
PORT = 33
DEVICE_IP = '192.168.0.129'

# Browser tab title
PROJECT_TITLE = 'Memviz'

# Title and subtitle to display on header
HEADER_TITLE = 'Memviz'
HEADER_SUBTITLE = 'Visualisation du corpus BioMed et des analyses'

# Name and bio of the project contributors. Displayed in About tab.
CONTRIBUTORS = {
    'Name McName': 'This person is working on something ',
    'Person Person': 'This person also contributed to the project. Here is some gibberish to see what happens'
                     ' when there is more text and multiple lines might be needed.',
}

TOPIC_MAPPING = {'topic_0': 'Population',
                 'topic_1': 'Animal experiments',
                 'topic_2': 'Demographics',
                 'topic_3': 'Exposure factors',
                 'topic_4': 'Enzyme production',
                 'topic_5': 'Plant genetics and species',
                 'topic_6': 'Genetic pathway',
                 'topic_7': 'Community health',
                 'topic_8': 'Survey-report',
                 'topic_9': 'Orthopaedic trauma',
                 'topic_10': 'Health research and policy',
                 'topic_11': 'Method-measurement',
                 'topic_12': 'Genetic transcription',
                 'topic_13': 'Hematology',
                 'topic_14': 'Infection-virus',
                 'topic_15': 'Test and prediction',
                 'topic_16': 'Genotype-phenotype',
                 'topic_17': 'Research emphasis (jargon)',
                 'topic_18': 'Evolutionary biology and phylogenetics',
                 'topic_19': 'Bacteria',
                 'topic_20': 'Cell-oncology',
                 'topic_21': 'Chemical',
                 'topic_22': 'Mental health',
                 'topic_23': 'Rheumatology',
                 'topic_24': 'Mosquito-malaria',
                 'topic_25': 'Network-model',
                 'topic_26': 'Public health',
                 'topic_27': 'Physical activity',
                 'topic_28': 'Cell signaling ',
                 'topic_29': 'Cell development',
                 'topic_30': 'PCR',
                 'topic_31': 'Nervous system',
                 'topic_32': 'Weight and obesity',
                 'topic_33': 'Screening',
                 'topic_34': 'Statistics',
                 'topic_35': 'Life cycle and reproduction',
                 'topic_36': 'Imaging-artery',
                 'topic_37': 'Food-consumption',
                 'topic_38': 'Genetic expression',
                 'topic_39': 'Sex and selection',
                 'topic_40': 'Cytology',
                 'topic_41': 'Malaria-parasite',
                 'topic_42': 'Cancer',
                 'topic_43': 'Infection resistance',
                 'topic_44': 'Maternity',
                 'topic_45': 'Muscle and motion',
                 'topic_46': 'Literature review',
                 'topic_47': 'Therapy (cancer)',
                 'topic_48': 'Prognostic',
                 'topic_49': 'Medical training',
                 'topic_50': 'Cattle',
                 'topic_51': 'Cognitive performance',
                 'topic_52': 'Protein domain',
                 'topic_53': 'Cardiovascular conditions',
                 'topic_54': 'Method-model',
                 'topic_55': 'Change',
                 'topic_56': 'Score-measure',
                 'topic_57': 'Surgery',
                 'topic_58': 'Healthcare',
                 'topic_59': 'Antibody-protein',
                 'topic_60': 'Cancer (tumor)',
                 'topic_61': 'Respiratory',
                 'topic_62': 'Patient mortality',
                 'topic_63': 'Drug',
                 'topic_64': 'Diabetes',
                 'topic_65': 'Genetic expression',
                 'topic_66': 'IT systems',
                 'topic_67': 'Oxidative stress',
                 'topic_68': 'Immunology',
                 'topic_69': 'Clinical trials',
                 'topic_70': 'Diagnosis',
                 'topic_71': 'Loss-gain',
                 'topic_72': 'Brain',
                 'topic_73': 'Costs',
                 'topic_74': 'Genetic markers and traits',
                 'topic_75': 'Water-uptake',
                 'topic_76': 'Genetic sequence',
                 'topic_77': 'Childhood',
                 'topic_78': 'Genetic mutation',
                 'topic_79': 'Timelaps', }
