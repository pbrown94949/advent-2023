import argparse
import collections
import re
import time

from dataclasses import dataclass
from operator import gt, lt
from typing import Deque, Generator, List

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

    def get_inverse(self):
        if self.operator == '<':
            return Comparison(self.variable, '>', self.amount - 1)
        return Comparison(self.variable, '<', self.amount + 1)


class WorkflowRule:

    def __init__(self, destination: str, comparison: Comparison = None):
        self.destination = destination
        self.comparison = comparison

    def __repr__(self):
        return f"WorkflowRule(destination={self.destination}, comparison={self.comparison})"


class Workflow:

    def __init__(self, name: str, rules: List[WorkflowRule] = []):
        self.name = name
        self.rules = rules

    def __repr__(self):
        return f"Workflow(name={self.name}, rules={self.rules})"


class TreeNode[T]:

    def __init__(self, item: T):
        self.item = item
        self.parent: TreeNode = None
        self.children: List[TreeNode] = []

    def __repr__(self):
        return f"TreeNode(item={self.item})"

    def add_child(self, node: "TreeNode"):
        self.children.append(node)
        node.parent = self

    def get_left_siblings(self) -> List["TreeNode"]:
        result = []
        if self.parent is not None:
            for node in self.parent.children:
                if node == self:
                    break
                result.append(node)
        return result

    def dfs(self) -> Generator["TreeNode", None, None]:
        queue = collections.deque()
        queue.append(self)
        while queue:
            node: TreeNode = queue.popleft()
            for child in node.children:
                queue.append(child)
            yield node


@dataclass(frozen=True)
class Span:
    start: int
    end: int

    def __len__(self):
        if self.start == 0:
            return 0
        return self.end - self.start + 1

    def get_overlap(self, other: "Span"):
        start = max(self.start, other.start)
        end = min(self.end, other.end)
        if start <= end:
            return Span(start, end)
        else:
            return Span(0, 0)


def main():
    init()
    process()
    wrapup()


def init():
    global args
    args = argparser.parse_args()


def process():
    root = build_workflow_rule_tree()
    total = 0
    for path in get_accepted_paths(root):
        total += count_combinations_on_node(path)
    print(total)


def build_workflow_rule_tree():
    workflows = get_workflows()
    workflows = {wf.name: wf for wf in workflows}
    workflows['A'] = Workflow('A')
    workflows['R'] = Workflow('R')
    root = TreeNode(WorkflowRule('in'))
    queue = collections.deque([root])
    while queue:
        node: TreeNode[WorkflowRule] = queue.popleft()
        wf_name = node.item.destination
        wf = workflows[wf_name]
        for rule in wf.rules:
            child_node = TreeNode(rule)
            node.add_child(child_node)
            queue.append(child_node)
    return root


def get_accepted_paths(root: TreeNode[WorkflowRule]):
    node: TreeNode[WorkflowRule]
    for node in root.dfs():
        if node.item.destination == 'A':
            yield node


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


def get_lines():
    with open(args.file) as file:
        for line in file:
            yield line.strip()


def count_combinations_on_node(node: TreeNode[WorkflowRule]):
    comparisons = get_comparisons(node)
    return count_combinations(comparisons)


def get_comparisons(node: TreeNode[WorkflowRule]):
    # get all the comparisons that had to be true to reach this node
    result = []
    while node is not None:
        if node.item.comparison is not None:
            result.append(node.item.comparison)
        sibling: TreeNode[WorkflowRule]
        for sibling in node.get_left_siblings():
            if sibling.item.comparison is not None:
                result.append(sibling.item.comparison.get_inverse())
        node = node.parent
    return result


def count_combinations(comparisons: List[Comparison]):
    spans = {
        'x': Span(1, 4000),
        'm': Span(1, 4000),
        'a': Span(1, 4000),
        's': Span(1, 4000)
    }
    for comparison in comparisons:
        if comparison.operator == '<':
            rule_span = Span(1, comparison.amount - 1)
        else:
            rule_span = Span(comparison.amount + 1, 4000)
        spans[comparison.variable] = rule_span.get_overlap(spans[comparison.variable])
    result = 1
    for span in spans.values():
        result *= len(span)
    return result


def wrapup():
    pass


if __name__ == "__main__":
    main()
    print("--- %s seconds ---" % int(time.time() - start_time))
