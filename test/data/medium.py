def main_question(request):
    return 'Create a JSON object based on the given sentence "' + request + '" following this schema: "{subject: text, verb: text, object: text}". Consider the "subject" to represent the entity performing the action, the "verb" to represent the command, and the "object" to represent the target on which the action is being performed.'


def requests(index):
    req = {
        0: 'Can you follow me?',
        1: 'Can you stop?',
        2: 'Can you go right?',
        3: 'Can you go left?',
        4: None,
    }
    return main_question(req[index])


def correct_answers(index):
    answers = {
        0: '{"subject": "i", "verb": "follow", "object": "you"}',
        1: '{"subject": "i", "verb": "stop", "object": ""}',
        2: '{"subject": "i", "verb": "go", "object": "right"}',
        3: '{"subject": "i", "verb": "go", "object": "left"}',
    }
    return answers[index]
