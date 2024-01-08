from Levenshtein import distance

from lm import send_prompt, prompt_and_load_code

PROMPT_MASK_LIST_ENTITIES = 'Given the env vars HOME_ASSISTANT_URL and HOME_ASSISTANT_TOKEN a user wants to ' \
                            '{command}. ' \
                            'Write Python function "list_entities()" that returns a list of entities ' \
                            'that can perform this action. ' \
                            'The list should contain only the original objects returned from the API. ' \
                            'Consider mainly entity_id, friendly name and state not "attributes", ' \
                            'but return the entire object. ' \
                            'Don''t use "supported_features" attribute. ' \
                            'Not all entities has friendly_name. ' \
                            'Import and use os, requests and other necessary packages. ' \
                            'Don''t include any explanations in your response.' \
                            'You can make more than one API call if you need to retrieve more data.'
PROMPT_MASK_SELECT_ENTITIES = 'A user asked to {command}. ' \
                              'Which of the following entities is or are the best to perform this request?\n' \
                              '{entities}\n\n' \
                              'Provide only the entity name. If more than one entity, then commas instead of "and".'
PROMPT_DO_THE_COMMAND = 'Given the env vars HOME_ASSISTANT_URL and HOME_ASSISTANT_TOKEN a user wants to {command}. ' \
                        'Write Python function "call_entity()" to do that specifically and only to the following entity_id: ' \
                        '"{entity_id}" and return string result. ' \
                        'Import and use os, requests and other necessary packages. ' \
                        'Don''t include any explanations in your response.'

DISTANCE_THRESHOLD = 3


def filter_entities(entities_list, best_entity_answers):
    return [e for e in entities_list for ans in best_entity_answers if
            distance(e['attributes']['friendly_name'], ans) < DISTANCE_THRESHOLD]


def main(command):
    # List Home-Assistant entities
    module_list_entities = prompt_and_load_code(PROMPT_MASK_LIST_ENTITIES.format(command=command))
    entities_list = module_list_entities.list_entities()
    assert len(entities_list) > 0
    entities_names = [e['attributes']['friendly_name'] for e in entities_list]

    # Filter entities
    best_entity_answers = send_prompt(
        PROMPT_MASK_SELECT_ENTITIES.format(command=command, entities=entities_names)).split(', ')
    assert len(best_entity_answers) > 0

    # Call action on entities
    best_entities = filter_entities(entities_list, best_entity_answers)
    assert len(best_entities) > 0
    best_entities_ids = [e['entity_id'] for e in best_entities]
    module_call_entity = prompt_and_load_code(
        PROMPT_DO_THE_COMMAND.format(command=command, entity_id=','.join(best_entities_ids)))

    print(module_call_entity.call_entity())


if __name__ == '__main__':
    command = 'Lock the door'
    print(f'>> {command}')
    main(command)
