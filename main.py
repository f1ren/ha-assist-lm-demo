from Levenshtein import distance

from llm import prompt_and_extract_code, send_prompt

DISTANCE_THRESHOLD = 3

PROMPT_MASK_LIST_ENTITIES = 'Given the env vars HOME_ASSISTANT_URL and HOME_ASSISTANT_TOKEN a user wants to {command}. ' \
                            'Write Python function "list_entities" that returns a list of all entities that can perform this action. '
PROMPT_MASK_SELECT_ENTITIES = 'A user asked to {command}. ' \
                              'Which of the following entities is or are the best to perform this request?\n' \
                              '{entities}\n\n' \
                              'Provide the shortest answer possible.'
PROMPT_DO_THE_COMMAND = 'Given the env vars HOME_ASSISTANT_URL and HOME_ASSISTANT_TOKEN a user wants to {command}. ' \
                        'Write Python function call_entity() to do that to entity_id {entity_id} and string result.'


def filter_entities(entities_list, best_entity_answer):
    return [e for e in entities_list if
            distance(e['attributes']['friendly_name'], best_entity_answer) < DISTANCE_THRESHOLD]


def main():
    command = 'Lock the door'
    prompt_and_extract_code(PROMPT_MASK_LIST_ENTITIES.format(command=command))
    entities_list = [{'entity_id': 'input_text.main_door_unlock_code_typed', 'state': '322323231233223', 'attributes': {'editable': True, 'min': 0, 'max': 30, 'pattern': None, 'mode': 'password', 'icon': 'mdi:key', 'friendly_name': 'Main door unlock code typed'}, 'last_changed': '2024-01-04T21:04:37.663668+00:00', 'last_updated': '2024-01-04T21:04:37.663668+00:00', 'context': {'id': '01HKB4NN8XZ8NYKAJAZB9CTCS9', 'parent_id': '01HKB4NMR1XFWGKE0K2H2JN9EJ', 'user_id': None}}, {'entity_id': 'automation.door_lock_keypad_unlock', 'state': 'on', 'attributes': {'id': '1699946729725', 'last_triggered': '2024-01-04T21:04:37.662026+00:00', 'mode': 'single', 'current': 0, 'friendly_name': 'Door lock: keypad unlock'}, 'last_changed': '2024-01-04T07:16:31.179880+00:00', 'last_updated': '2024-01-04T21:04:37.664328+00:00', 'context': {'id': '01HKB4NN8XZ8NYKAJAZB9CTCS9', 'parent_id': '01HKB4NMR1XFWGKE0K2H2JN9EJ', 'user_id': None}}, {'entity_id': 'binary_sensor.nuki_main_locked', 'state': 'on', 'attributes': {'timestamp': '2024-01-05T06:00:30', 'device_class': 'lock', 'friendly_name': 'Nuki Main Locked'}, 'last_changed': '2024-01-05T05:43:21.122793+00:00', 'last_updated': '2024-01-05T06:00:29.547714+00:00', 'context': {'id': '01HKC3AVKBN04KGK7HKREWJSB8', 'parent_id': None, 'user_id': None}}, {'entity_id': 'lock.nuki_main_lock', 'state': 'unlocked', 'attributes': {'friendly_name': 'Nuki Main Lock', 'supported_features': 1}, 'last_changed': '2024-01-05T05:43:21.123408+00:00', 'last_updated': '2024-01-05T05:43:21.123408+00:00', 'context': {'id': '01HKC2BF93JVP22GC81RKDRQ2V', 'parent_id': None, 'user_id': None}}, {'entity_id': 'lock.kids_shower_heater_child_lock', 'state': 'unlocked', 'attributes': {'friendly_name': 'Kids shower heater Child lock', 'supported_features': 0}, 'last_changed': '2024-01-04T07:16:45.930835+00:00', 'last_updated': '2024-01-04T07:16:45.930835+00:00', 'context': {'id': '01HK9N9SQAB677TJA7K90E2W6K', 'parent_id': None, 'user_id': None}}, {'entity_id': 'lock.parents_shower_heater_child_lock', 'state': 'unlocked', 'attributes': {'friendly_name': 'Parents shower heater Child lock', 'supported_features': 0}, 'last_changed': '2024-01-04T07:18:14.880082+00:00', 'last_updated': '2024-01-04T07:18:14.880082+00:00', 'context': {'id': '01HK9NCGK071A1M0K8EQAGKZ4F', 'parent_id': None, 'user_id': None}}, {'entity_id': 'lock.router_plug_child_lock', 'state': 'unlocked', 'attributes': {'friendly_name': 'Router plug Child lock', 'supported_features': 0}, 'last_changed': '2024-01-04T07:18:14.881876+00:00', 'last_updated': '2024-01-04T07:18:14.881876+00:00', 'context': {'id': '01HK9NCGK1D6SJN78WAK55TY1V', 'parent_id': None, 'user_id': None}}, {'entity_id': 'switch.roborock_q_revo_child_lock', 'state': 'on', 'attributes': {'icon': 'mdi:account-lock', 'friendly_name': 'Roborock Q Revo Child lock'}, 'last_changed': '2024-01-04T07:17:01.232877+00:00', 'last_updated': '2024-01-04T07:17:01.232877+00:00', 'context': {'id': '01HK9NA8NGKHHJGEYB6K15PN8K', 'parent_id': None, 'user_id': None}}]
    entities_names = [e['attributes']['friendly_name'] for e in entities_list]
    prompt_and_extract_code(PROMPT_MASK_SELECT_ENTITIES.format(command=command, entities=entities_names))
    best_entity_answer = '"Nuki Main Lock"'
    best_entities = filter_entities(entities_list, best_entity_answer)
    best_entities_ids = [e['entity_id'] for e in best_entities]
    print(send_prompt(PROMPT_DO_THE_COMMAND.format(command=command, entity_id=','.join(best_entities_ids))))


if __name__ == '__main__':
    main()
