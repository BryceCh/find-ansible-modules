#!/usr/bin/env python3

import argparse
import sys
import yaml

__doc__ = """
simple script to look for modules used in an ansible playbook
"""

# Set acceptable extensions for analyzed files
extensions = ['.yml','.yaml']

# from https://docs.ansible.com/ansible/latest/reference_appendices/playbooks_keywords.html
ANSIBLE_KEYWORDS = (
        'action', 'always', 'any_errors_fatal', 'args', 'async', 'become',
        'become_exe', 'become_flags', 'become_method', 'become_user', 'block',
        'changed_when', 'check_mode', 'collections', 'connection', 'debugger',
        'delay', 'delegate_facts', 'delegate_to', 'diff', 'environment',
        'fact_path', 'failed_when', 'gather_facts', 'gather_subset',
        'handlers', 'hosts', 'ignore_errors', 'ignore_unreachable',
        'local_action', 'loop', 'loop_control', 'max_fail_percentage',
        'module_defaults', 'name', 'no_log', 'notify', 'order', 'poll',
        'port', 'post_tasks', 'pre_tasks', 'post_tasks', 'register',
        'remote_user', 'rescue', 'retries', 'roles', 'run_once', 'serial',
        'strategy', 'tags', 'throttle', 'timeout', 'until', 'vars',
        'vars_files', 'vars_prompt', 'when')

def extract_candidates(yaml_content):
    candidates = []

    for item in yaml_content:
        if type(item) is list:
            return extract_candidates(item)
        elif type(item) is dict:
            for key in item:
                # skip 'with_<plugin >' loops
                if key.startswith('with_'):
                    continue

                # NOTE:side-effect of not handling dict of dicts here is that
                # module arguments are skipped.  need to test more complex
                # scenarios to see if skips anything we actually want
                if type(item[key]) is list:
                    # skip 'roles' keyword in a playbook since no individual
                    # tasks are called in this section
                    if key == 'roles':
                        continue
                    candidates += extract_candidates(item[key])
                else:
                    candidates.append(key)
        else:
            continue
    return candidates


def parse_cli_args():
    parser = argparse.ArgumentParser(
            description='Look for modules used in an ansible playbook')
    parser.add_argument(
            'filename',
            type=str, nargs='+',
            default=[],
            help='playbook or task file to parse for list of modules')

    parsed = parser.parse_args()

    if len(parsed.filename) == 0:
        parser.print_help(sys.stderr)
        sys.exit(1)

    return parsed


def main(args):
    exts = tuple(extensions)
    for filename in args.filename:
        if not filename.endswith(exts):
            sys.stderr.write(f'{filename}: does not end in one of {exts}; skipping\n')
            continue

        with open(filename, 'r') as content:
            try:
                yaml_content = yaml.safe_load(content)
            except yaml.parser.ParserError:
                sys.stderr.write(f'{filename}: error parsing YAML, skipping\n')
                continue
            except yaml.YAMLError as e:
                sys.stderr.write(e)
                continue

            if not type(yaml_content) is list:
                sys.stderr.write(
                        f'{filename} is not a list of plays or tasks, '
                        'skipping\n')
                continue

        candidates = extract_candidates(yaml_content)

        for keyword in ANSIBLE_KEYWORDS:
            while keyword in candidates:
                candidates.remove(keyword)
        
        if (len(candidates) > 0): 
          print(f'Modules found in {filename}:')
          print('\n'.join(sorted(set(candidates))) + '\n')
        else:
          print(f'No modules found in {filename}')

    return 0


if __name__ == '__main__':
    args = parse_cli_args()
    sys.exit(main(args))
