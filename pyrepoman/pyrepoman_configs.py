# Standard Library Imports

# Third Party Imports

# Local Application Imports

def pyrepoman_configs_add(key, value):

    """ KEY AND VALUE ARE TAKEN IN, ADD TO DATA STRUCTURE WITH KEY/VALUE TUPLE IN A LIST (key[0],value[0]) """

    PYREPOMAN_CONFIGS.append((key, value))

def pyrepoman_configs_merge(data_structure):

    PYREPOMAN_CONFIGS.append(data_structure)

def pyrepoman_configs_config_exist(key):

    if(key in PYREPOMAN_CONFIGS):
        return True

    return False

def pyrepoman_configs_select_config_value(config):

    for pair in PYREPOMAN_CONFIGS:
        if(pair[0] == config):
            return pair[1]

PYREPOMAN_CONFIGS = []