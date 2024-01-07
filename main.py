from Levenshtein import distance

from lm import send_prompt, prompt_and_load_code

PROMPT_MASK_LIST_ENTITIES = 'Given the env vars HOME_ASSISTANT_URL and HOME_ASSISTANT_TOKEN a user wants to ' \
                            '{command}. ' \
                            'Write Python function "list_entities()" that returns a list of all entity objects ' \
                            'that can perform this action. ' \
                            'Consider only by entity prefix, entity_id and friendly name, but return the entire object. ' \
                            'Don''t use supported_features. ' \
                            'Not all entities has friendly_name. ' \
                            'Import and use os, requests and other necessary packages. ' \
                            'Do not call the function.'
PROMPT_MASK_SELECT_ENTITIES = 'A user asked to {command}. ' \
                              'Which of the following entities is or are the best to perform this request?\n' \
                              '{entities}\n\n' \
                              'Provide the shortest answer possible.'
PROMPT_DO_THE_COMMAND = 'Given the env vars HOME_ASSISTANT_URL and HOME_ASSISTANT_TOKEN a user wants to {command}. ' \
                        'Write Python function "call_entity()" to do that to the entity_id {entity_id} and ' \
                        'return string result. ' \
                        'Import all necessary packages. ' \
                        'Do not call the function.'

DISTANCE_THRESHOLD = 3


def filter_entities(entities_list, best_entity_answer):
    return [e for e in entities_list if
            distance(e['attributes']['friendly_name'], best_entity_answer) < DISTANCE_THRESHOLD]


def main(command):
    module_list_entities = prompt_and_load_code(PROMPT_MASK_LIST_ENTITIES.format(command=command))
    entities_list = module_list_entities.list_entities()
    entities_names = [e['attributes']['friendly_name'] for e in entities_list]

    best_entity_answer = send_prompt(
        PROMPT_MASK_SELECT_ENTITIES.format(command=command, entities=entities_names))

    best_entities = filter_entities(entities_list, best_entity_answer)
    best_entities_ids = [e['entity_id'] for e in best_entities]
    module_call_entity = prompt_and_load_code(PROMPT_DO_THE_COMMAND.format(command=command, entity_id=','.join(best_entities_ids)))

    print(module_call_entity.call_entity())


if __name__ == '__main__':
    main('Lock the door')
