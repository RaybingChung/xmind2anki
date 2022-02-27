from typing import List

from xmind_parser import ProcessedNode


# def cvt2ind_wri_nt(node: Node):
#     deck_name = 'test'
#     common_model = "基础"  # common_mode
#     common_phrase_model = '主题-表达'
#     common_idea_model = '主题-思路'
#     advanced_model = "主题-词组-思路"  # advanced_mode
#     tags = ['xmind']
#     children = node['children']
#     en_children = []
#     cn_children = []
#
#     for child in children:
#         if not is_chinese(child):
#             en_children.append(child)
#         else:
#             cn_children.append(child)
#     if len(cn_children) != 0 and len(en_children) != 0:
#         phrase = ''
#         des_ideas = ''
#         for en_child in en_children:
#             phrase = phrase + decorate_string(en_child)
#         for cn_child in cn_children:
#             des_ideas = des_ideas + decorate_string(cn_child)
#
#         return nt_add_detail(ind_wri_material(node['title'], phrase, des_ideas),
#                              deck_name, model_name=advanced_model, tags=tags)
#
#     elif len(cn_children) != 0 and len(en_children) == 0:
#         back = ''
#         for cn_child in cn_children:
#             back = back + decorate_string(cn_child)
#         return nt_add_detail(common_note(front=node['title'], back=back),
#                              deck_name, model_name=common_idea_model, tags=tags)
#     elif len(cn_children) == 0 and len(en_children) != 0:
#         back = ''
#         for en_child in en_children:
#             back = back + decorate_string(en_child)
#         return nt_add_detail(common_note(front=node['title'], back=back),
#                              deck_name, model_name=common_phrase_model, tags=tags)
#     else:
#         pass


def cvt2ind_wri_nt_rem_path(node: ProcessedNode):
    deck_name = 'test'
    common_model = "基础"  # common_mode
    common_phrase_model = '主题-表达'
    common_idea_model = '主题-思路'
    advanced_model = "主题-词组-思路"  # advanced_mode
    tags = ['xmind']
    children = node['children']
    en_children = []
    cn_children = []

    for child in children:
        if not is_chinese(child):
            en_children.append(child)
        else:
            cn_children.append(child)

    message_shown_when_questioning = node['title']

    for ancestor in reversed(node['ancestors']):
        message_shown_when_questioning = ancestor + ' -> ' + message_shown_when_questioning
    message_shown_when_questioning = decorate_string(message_shown_when_questioning)

    if len(cn_children) != 0 and len(en_children) != 0:
        phrase = ''
        des_ideas = ''
        for en_child in en_children:
            phrase = phrase + decorate_string(en_child)
        for cn_child in cn_children:
            des_ideas = des_ideas + decorate_string(cn_child)

        return nt_add_detail(ind_wri_material(message_shown_when_questioning, phrase, des_ideas),
                             deck_name, model_name=advanced_model, tags=tags)

    elif len(cn_children) != 0 and len(en_children) == 0:
        back = ''
        for cn_child in cn_children:
            back = back + decorate_string(cn_child)
        return nt_add_detail(common_note(front=message_shown_when_questioning, back=back),
                             deck_name, model_name=common_idea_model, tags=tags)
    elif len(cn_children) == 0 and len(en_children) != 0:
        back = ''
        for en_child in en_children:
            back = back + decorate_string(en_child)
        return nt_add_detail(common_note(front=message_shown_when_questioning, back=back),
                             deck_name, model_name=common_phrase_model, tags=tags)
    else:
        pass


def is_chinese(string):
    for _char in string:
        if '\u4e00' <= _char <= '\u9fa5':
            return True
    return False


def ind_wri_material(title, phrases, des_ideas):
    return {
        "正面": title,
        "背面": phrases,
        "思路": des_ideas
    }


def common_note(front, back):
    return {
        "正面": front,
        "背面": back
    }


def nt_add_detail(nt, deck_name: str, model_name: str, tags: List):
    return {
        "deckName": deck_name,
        "modelName": model_name,
        "tags": tags,
        "fields": nt
    }


def decorate_string(string: str):
    return '<div>' + string + '</div>'
