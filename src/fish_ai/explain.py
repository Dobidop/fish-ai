# -*- coding: utf-8 -*-

from sys import argv
from fish_ai import engine


def get_instructions(commandline):
    return [
        {
            'role': 'system',
            'content': '''
            Respond with a single sentence which explains the fish shell
            command given by the user.

            The sentence must begin with a verb. The sentence should be
            written in {language}.
            '''.format(language=engine.get_config('language') or 'English')
        },
        {
            'role': 'user',
            'content': 'df -h'
        },
        {
            'role': 'assistant',
            'content': 'List all disks on the system'
        },
        {
            'role': 'user',
            'content': 'docker pull alpine:3'
        },
        {
            'role': 'assistant',
            'content': 'Pull the Alpine 3 container from DockerHub'
        },
        {
            'role': 'user',
            'content': 'sed -i "s/foo/bar/g" docker-compose.yml'
        },
        {
            'role': 'assistant',
            'content': 'Substitute all occurrences of the string "foo" with ' +
                    'the string "bar" in the file "docker-compose.yml"'
        },
        {
            'role': 'user',
            'content': commandline
        }
    ]


def get_messages(commandline):
    return [engine.get_system_prompt()] + get_instructions(commandline)


def explain():
    commandline = argv[1]

    try:
        engine.get_logger().debug('Explaining commandline: ' + commandline)
        response = engine.get_response(messages=get_messages(commandline))
        print('# ' + response)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        engine.get_logger().exception(e)
        # Leave the commandline untouched
        print(commandline)
