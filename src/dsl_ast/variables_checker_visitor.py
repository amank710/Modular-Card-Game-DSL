from antlr4 import *

from src.parser.Grammar import Grammar
from src.dsl_ast.expression import ExpressionNode
from src.dsl_ast.expression import BinaryExpressionNode, VariableExpressionNode, ExpressionValueNode, ArithmeticExpressionNode
from src.parser.GrammarVisitor import GrammarVisitor
from src.dsl_ast.ast_node import *
from src.dsl_ast.nodes.action import ActionsNode
from src.dsl_ast.nodes.action import SystemActionNode, UserActionNode
from src.dsl_ast.nodes.variable import *
from src.dsl_ast.nodes.function import FunctionNode
from src.dsl_ast.nodes.function import FunctionEndNode, SystemFunctionNode, ActionFunctionNode, IfNode


class VariablesCheckerVisitor(GrammarVisitor):
    def __init__(self) -> None:
        self.roles = []
        self.declared_variables = set()
        self.declared_actions = set()
        self.initialized_variables = set()
        self.errors = []

    # In this static checker, we are mainly checking the following:
    # 1. If a variable is declared
    # 2. If a variable is initialized at the upper line of the code (not the order of the execution of the code)
    # 3. If an action is declared
    # 4. If a variable used in an expression is declared and initialized

    def check(self, node) -> list:
        self._find_declared_variables_and_actions(node)
        self._add_card_to_variables()
        self._check_variable_and_action_declarations(node)
        return self.errors

    def _add_card_to_variables(self):
        for role in self.roles:
            self.declared_variables.add(
                f"{role}.card"
            )
            self.initialized_variables.add(
                f"{role}.card"
            )

    # This function is used to find the declared variables and actions, and stores them in the corresponding sets
    def _find_declared_variables_and_actions(self, node) -> None:
        for child in node.children:
            if isinstance(child, CardValueOverrideNode):
                self.roles.extend([role.get_name()
                                  for role in child.children[0].children])
            elif isinstance(child, ActionsNode):
                for action in child.children:
                    self.declared_actions.add(
                        f"{action.get_name()}"
                    )
                    self.initialized_variables.update(
                        f"{role}.{action.get_name()}" for role in self.roles
                    )

            elif isinstance(child, VariableDeclarationsNode):
                for var in child.children:
                    role = var.get_role()
                    if role not in self.roles:
                        self.errors.append(f"Role {role} is not declared")
                    self.declared_variables.add(f"{role}.{var.get_name()}")

            self._find_declared_variables_and_actions(child)

    # This function is used to check the variable and action declarations
    def _check_variable_and_action_declarations(self, node) -> None:
        for child in node.children:
            if isinstance(child, VariableAssignmentNode):
                self._check_variable_assignment_node(child)
            elif isinstance(child, IfNode):
                self._check_if_node(child)
            elif isinstance(child, FunctionNode):
                self._check_function_node(child)
            self._check_variable_and_action_declarations(child)

    def _check_variable_assignment_node(self, child):
        if f"{child.get_role()}.{child.get_name()}" not in self.declared_variables:
            self.errors.append(f"Variable {child.get_role()}.{child.get_name()} is not declared")
        express = child.get_value()
        num_errors = len(self.errors)
        if isinstance(express, BinaryExpressionNode):
            self._evaluate_binary_expression_node(express)
        elif isinstance(express, ArithmeticExpressionNode):
            self._evaluate_arithmetic_expression_node(express)
        elif isinstance(express, VariableExpressionNode):
            self._evaluate_variable_expression_node(express)
        if len(self.errors) == num_errors:
            self.initialized_variables.add(f"{child.get_role()}.{child.get_name()}")


    def _check_if_node(self, child):
        express = child.get_expression()
        if isinstance(express, BinaryExpressionNode):
            self._evaluate_binary_expression_node(express)

    def _check_function_node(self, child):
        if isinstance(child, SystemFunctionNode):
            arguments = child.get_args()
            for arg in arguments:
                if arg.name not in self.declared_actions:
                    self.errors.append(f"Action {arg.name} is not declared")
        else:
            if child.get_name() not in self.declared_actions and child.get_name() != 'setup' and child.get_name() != 'on_turn':
                self.errors.append(f"Action {child.get_name()} is not declared")

    def _evaluate_binary_expression_node(self, node):
        left = node.left
        right = node.right
        if isinstance(left, VariableExpressionNode):
            self._evaluate_variable_expression_node(left)
        elif isinstance(left, ArithmeticExpressionNode):
            self._evaluate_arithmetic_expression_node(left)
        elif isinstance(left, BinaryExpressionNode):
            self._evaluate_binary_expression_node(left)

        if isinstance(right, VariableExpressionNode):
            self._evaluate_variable_expression_node(right)
        elif isinstance(right, ArithmeticExpressionNode):
            self._evaluate_arithmetic_expression_node(right)
        elif isinstance(left, BinaryExpressionNode):
            self._evaluate_binary_expression_node(right)

    def _evaluate_variable_expression_node(self, node):
        if node.role not in self.roles:
            self.errors.append(f"Role {node.role} is not declared")
        if f"{node.role}.{node.name}" not in self.declared_variables and f"{node.role}.{node.name}" not in self.initialized_variables:
            self.errors.append(f"Variable {node.role}.{node.name} is not declared")
        elif f"{node.role}.{node.name}" not in self.initialized_variables:
            self.errors.append(f"Variable {node.role}.{node.name} is not initialized")

    def _evaluate_arithmetic_expression_node(self, node):
        left = node.left
        right = node.right
        if isinstance(left, VariableExpressionNode):
            self._evaluate_variable_expression_node(left)
        elif isinstance(left, ArithmeticExpressionNode):
            self._evaluate_arithmetic_expression_node(left)
        elif isinstance(left, BinaryExpressionNode):
            self._evaluate_binary_expression_node(left)

        if isinstance(right, VariableExpressionNode):
            self._evaluate_variable_expression_node(right)
        elif isinstance(right, ArithmeticExpressionNode):
            self._evaluate_arithmetic_expression_node(right)
        elif isinstance(left, BinaryExpressionNode):
            self._evaluate_binary_expression_node(right)
