def parse_tags(targs):
    """
    Tags can be in the forma key:value or simply value
    """
    tags = {}
    for t in targs:
        split_tag = t.split(':')
        if len(split_tag) > 1:
            tags['tag:' + split_tag[0]] = split_tag[1]
        else:
            tags['tag:' + split_tag[0]] = ''
    return tags


def run_action(actions, cmd):
    if cmd not in actions:
        print('{} is an invalid action\n'.format(cmd))
        print('Valid actions are:')
        for k in actions.keys():
            print('* {} \n'.format(k))
        exit(1)
    else:
        actions[cmd]()
