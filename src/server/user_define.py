# This module include all user deine part


def conf_table_filter(config_file_dir:str, config_file_name:str) -> bool:
    """filter config tables don't needed to check.
    
    Args:
        config_file_dir: directory path of config_file_name
        config_file_name: config file's name
    Retuens:
        need_filter: if return True, the config file will be filter.
    
    Example: if you don't want to check all config tables which name
        contain 'Ai', then you can define this function as below:

        def conf_table_filter(config_file_dir:str, config_file_name:str) -> bool:
            if 'ai' in config_file_name:
                return True
            return False
    """
    return False


