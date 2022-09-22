import SystemUnlock_Table


@RM.reg_check_rule()
def check_system_open_level() -> bool:
    flag = True
    unlock_level = SystemUnlock_Table.get_var(8, "Unlock_Level")
    if unlock_level != 3:
        error_log("BP system unlock level({}) is not level(3)".format(unlock_level))
        flag = False
    return flag

def check_system_open_time() -> bool:
    return True