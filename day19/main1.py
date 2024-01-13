import argparse
import re
import time

from dataclasses import dataclass
from operator import gt, lt
from typing import List

argparser = argparse.ArgumentParser()
argparser.add_argument('file')

start_time = time.time()

comma_delimited_pattern = re.compile("([^,]+)")
string_in_braces_pattern = re.compile("{(.+)}")

workflow_pattern = re.compile("""
                              (?P<name>[a-z]+)   # name of the workflow
                              {(?P<rules>.+)}    # list of rules inside braces
                              """, re.VERBOSE)

rule_pattern = re.compile("""
                            (?:(?P<comparison>[^:]+):)?    # optional comparison statement followed by a colon
                            (?P<destination>.+)            # required destination value
                          """, re.VERBOSE)

comparison_pattern = re.compile("""
                                    (?P<variable>[xmas])       # variable name
                                    (?P<operator>[<>])         # comparison operator
                                    (?P<amount>[1-9][0-9]*)    # number
                                """, re.VERBOSE)


assignment_statement_pattern = re.compile("""
                                            (?P<variable>[xmas])       # variable name
                                            =                          # equals sign
                                            (?P<value>[1-9][0-9]*)     # number
                                        """, re.VERBOSE)


@dataclass
class Comparison:
    variable: str
    operator: str
    amount: int

    def is_true(self, item: dict):
        comparator = lt if self.operator == '<' else gt
        return comparator(item[self.variable], self.amount)


class WorkflowRule:

    def __init__(self, destination: str, comparison: Comparison = None):
        self.destination = destination
        self.comparison = comparison

    def get_destination(self, item: dict):
        if self.comparison is None or self.comparison.is_true(item):
            return self.destination
        return None


class Workflow:

    def __init__(self, name: str, rules: List[WorkflowRule]):
        self.name = name
        self.rules = rules

    def get_destination(self, item: dict):
        for rule in self.rules:
            destination = rule.get_destination(item)
            if destination is not None:
                return destination
        raise Exception('Missing final rule')


class WorkflowSystem:

    def __init__(self, workflows: List[Workflow]):
        self._dict = {x.name: x for x in workflows}

    def __len__(self):
        return len(self._dict)

    def get_destination(self, item: dict):
        workflow = self._dict['in']
        while True:
            destination = workflow.get_destination(item)
            if destination in ['A', 'R']:
                return destination
            workflow = self._dict[destination]



def main():
    init()
    process()
    wrapup()


def init():
    global args
    args = argparser.parse_args()


def process():
    workflow_system = WorkflowSystem(get_workflows())
    items = get_items()
    accepted_items = []
    for item in items:
        destination = workflow_system.get_destination(item)
        if destination == 'A':
            accepted_items.append(item)
    total = 0
    for item in accepted_items:
        subtotal = sum(item.values())
        total += subtotal
    print(total)


def get_workflows() -> List[Workflow]:
    result = []
    for line in get_lines():
        if line == '':
            break
        workflow_match = workflow_pattern.fullmatch(line)
        workflow_name = workflow_match.group('name')
        rule_definitions = comma_delimited_pattern.findall(workflow_match.group('rules'))
        rules = [build_rule(x) for x in rule_definitions]
        result.append(Workflow(workflow_name, rules))
    return result


def build_rule(rule_definition: str):
    rule_match = rule_pattern.fullmatch(rule_definition)
    comparison = rule_match.group('comparison')
    destination = rule_match.group('destination')
    if comparison is None:
        return WorkflowRule(destination)
    else:
        comparison_match = comparison_pattern.fullmatch(comparison)
        variable, operator, amount = comparison_match.group('variable'), comparison_match.group('operator'), int(comparison_match.group('amount'))
        return WorkflowRule(destination, Comparison(variable, operator, amount))


def get_items():
    result = []
    started = False
    for line in get_lines():
        if line == '':
            started = True
        elif started:
            item_match = string_in_braces_pattern.fullmatch(line)
            item_definition = item_match.group(1)
            result.append(build_item(item_definition))
    return result


def build_item(item_definition):
    result = {}
    assignment_statements = comma_delimited_pattern.findall(item_definition)
    for assignment_statement in assignment_statements:
        match = assignment_statement_pattern.fullmatch(assignment_statement)
        result[match.group('variable')] = int(match.group('value'))
    return result


def get_lines():
    with open(args.file) as file:
        for line in file:
            yield line.strip()


def wrapup():
    pass


if __name__ == "__main__":
    main()
    print("--- %s seconds ---" % int(time.time() - start_time))
