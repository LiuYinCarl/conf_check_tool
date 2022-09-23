import SystemUnlock_Table


@RM.reg_check_rule()
def check_system_open_level() -> bool:
    return True

def check_system_open_time() -> bool:
    return False