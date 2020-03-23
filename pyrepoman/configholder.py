# Standard Library Imports

# Third Party Imports

# Local Application Imports

class ConfigHolder:

    def __init__(self, args):

        self.configs = list()
        transformed_args = vars(args)
        [self.add_config(arg, transformed_args[arg]) for arg in transformed_args]

    def add_config(self, key, value):

        """ ADD KEY/VALUE TUPLE TO A DATA STRUCTURE (config,value) """

        self.configs.append((key, value))

    def merge_configs(self, data_structure):

        """ SHOULD BE THE SAME DATA STRUCTURE AS CONFIGS """

        self.configs.append(data_structure)

    def config_exist(self, config):

        if(self.get_config_value(config) != ""):
            return True

        return False

    def get_config_value(self, config):

        for pair in self.configs:
            if(pair[0] == config):
                return pair[1]

        return ""

    def __str__(self):
        
        return str(self.configs)
