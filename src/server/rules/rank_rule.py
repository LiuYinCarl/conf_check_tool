import Ranking_Parameter_Level_Table
import Likability_Table
import Hero_LV_Table


mastery_type = 8
favor_type = 9

@RM.reg_check_rule()
def check_favor_level() -> bool:
    """检查排行榜的英雄好感度配置."""
    flag = True
    favor_level_dict = {} # k:v = level:score
    for item in Ranking_Parameter_Level_Table.get_all().values():
        if item["Ranking_Parameter_Type"] == favor_type:
            level = item["Ranking_Parameter_Quality"]
            score = item["Ranking_Parameter_Score"]
            # 检查是否定义了重复的好感度等级配置
            if level in favor_level_dict:
                error_log("duplicate favor level({})".format(level))
                flag = False
            else:
                favor_level_dict[level] = score
    # 检查是否存在低等级的好感度分值高于高等级的好感度分值
    for level, score in favor_level_dict.items():
        for level2, score2 in favor_level_dict.items():
            if level2 < level and score2 >= score:
                error_log("favor level({})'s score({}) is more than level({})'s score({})"
                        .format(level2, score2, level, score))
                flag = False
    # 检查排行榜的好感度等级范围是否何好感度系统一致
    likely_level_set = set()
    for level in Likability_Table.get_all().keys():
        likely_level_set.add(level)

    favor_level_set = set()
    for level in favor_level_dict.keys():
        favor_level_set.add(level)
    
    if likely_level_set != favor_level_set:
        error_log("favor level set({}) is not equal to lickly system level set({})"
                .format(favor_level_set, likely_level_set))
        flag = False
    return flag


@RM.reg_check_rule()
def check_mastery_level() -> bool:
    """检查排行榜的英雄熟练度配置."""
    flag = True
    mastery_level_dict = {} # K:v = level:score
    for item in Ranking_Parameter_Level_Table.get_all().values():
        if item["Ranking_Parameter_Type"] == mastery_type:
            level = item["Ranking_Parameter_Quality"]
            score = item["Ranking_Parameter_Score"]
            if level in mastery_level_dict:
                error_log("duplicate mastery level({})".format(level))
                flag = False
            else:
                mastery_level_dict[level] = score
    for level, score in mastery_level_dict.items():
        for level2, score2 in mastery_level_dict.items():
            if level2 < level and score2 >= score:
                error_log("mastery level({})'s score({}) is more than level({})'s score({})"
                        .format(level2, score2, level, score))
                flag = False
    # 检查排行榜的好感度等级范围是否何好感度系统一致
    mastery_system_level_set = set()
    mastery_level_set = set()
    for item in Hero_LV_Table.get_all().values():
        level = item["Hero_TypeLevel"]
        mastery_system_level_set.add(level)
    for level in mastery_level_dict.keys():
        mastery_level_set.add(level)
    if mastery_system_level_set != mastery_level_set:
        error_log("mastery level set({}) is not equal to mastery system level set({})"
                .format(mastery_level_set, mastery_system_level_set))
    return flag

