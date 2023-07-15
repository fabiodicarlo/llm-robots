def main_question(request):
    return 'Create a JSON object based on the given sentence "' + request + '" following this schema: "{subject: text, verb: text, object: text}". Consider the "subject" to represent the entity performing the action, the "verb" to represent the command, the "object" to represent the target on which the action is being performed and the "direction" to represent the direction.'


def requests(index):
    req = {
        0: 'Take me the rectangular shaped object on your right',
        4: None,
    }
    return main_question(req[index])


def correct_answers(index):
    answers = {
        0: '{"subject": "me", "verb": "take", "object": "rectangular shaped object", "direction": "on your right"}',
    }
    return answers[index]
