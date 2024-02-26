from src.dsl_ast.nodes.function import *
from src.dsl_ast.nodes.variable import VariableAssignmentNode
from src.dsl_ast.ast_node import AstNode, ProgramNode
from src.dsl_ast.abstract_visitor import AbstractVisitor
from src.factory.config import Config
from src.factory.function_context.conditional import Conditional
from src.factory.function_context.function_context import FunctionContext
from src.factory.function_context.function_runner import FunctionRunner
from src.factory.function_context.if_statement import IfStatement
from src.factory.function_context.loop_statement import LoopStatement
from src.factory.function_context.statement import Statement
from src.factory.function_context.system_function_factory import SystemFunctionFactory
from src.factory.function_context.variable_assignment import IndirectVariableAssignment, VariableAssignment
from src.factory.function_type import FunctionType
from src.factory.prototypes.player_prototype import PlayerPrototype
from src.factory.types.callback_type import CallbackType
from src.game.objects.variable import Variable

from typing import Dict, List


class PlayerBuilder(AbstractVisitor):
    def __init__(self, config, role):
        self.variable_lookup_table: Dict[str, Dict[str, Variable]] = config.get_variables()

        self.config = config
        self.role = role
        self.player_proto = PlayerPrototype(name=role,
                                            actions=config.get_user_actions(),
                                            variables=self.variable_lookup_table)

        self.function_registry = self.initialize_registry(config)

        self.current_scope: List[AstNode] = []
        self.current_function_context: FunctionContext = None
        self.scope_to_function: Dict[str, Dict[str, FunctionContext]] = dict()

        # Function statement
        self.current_statement_context = []

    def get_role(self):
        return self.role
    
    def get_action_mapping(self):
        return self.config.get_action_mapping()

    def initialize_registry(self, config: Config) -> Dict[str, FunctionContext]:
        registry: dict[str, FunctionContext] = dict()
        registry[CallbackType.SETUP] = FunctionContext(name=CallbackType.SETUP,
                                                       variables=self.variable_lookup_table)
        registry[CallbackType.ON_TURN] = FunctionContext(name=CallbackType.ON_TURN,
                                                         variables=self.variable_lookup_table)
        action_function_registry = {name: FunctionContext(name=name, variables=self.variable_lookup_table) for name in config.get_user_actions()}

        return {**registry, **action_function_registry}
    
    def get_function_registry(self) -> Dict[str, FunctionContext]:
        return self.function_registry

    def build(self, root_node: ProgramNode) -> PlayerPrototype:
        root_node.accept_player_builder(self)

        for name, function_context in self.scope_to_function[FunctionType.COMMON].items():
           self.player_proto.register_callback(callback_type=name,
                                               callback=function_context)

        for name, function_context in self.scope_to_function[FunctionType.USER_OVERRIDE].items():
           self.player_proto.register_callback(callback_type=name,
                                               callback=function_context)

        for name, function_context in self.scope_to_function[FunctionType.RESULT].items():
           self.player_proto.register_callback(callback_type=name,
                                               callback=function_context)
           
        self.player_proto.register_action_map(self.get_action_mapping())

        return self.player_proto

    def visitCommonFunctionsNode(self, node: CommonFunctionsNode) -> None:
        self.current_scope.append(node.get_name())
        self.scope_to_function[node.get_name()] = dict()

    def visitUserFunctionsNode(self, node: UserFunctionsNode) -> None:
        self.current_scope.append(node.get_name())
        # node is at position -1
        self.scope_to_function[node.get_name()] = dict()

    def visitFunctionNode(self, node: FunctionNode) -> None:
        self.current_function_context = FunctionContext(name=node.get_name(),
                                                        variables=self.variable_lookup_table)

        current_scope = self.current_scope[-1]
        self.scope_to_function[current_scope][self.current_function_context.get_name()] = self.current_function_context

    def visitIndirectVariableAssignmentNode(self, node: VariableAssignmentNode) -> None:
        self.add_to_function(IndirectVariableAssignment(var_name=node.get_name(), role=node.get_role(), variables_map=self.variable_lookup_table))

    def visitDirectVariableAssignmentNode(self, node: VariableAssignmentNode) -> None:
        self.add_to_function(VariableAssignment(var_name=node.get_name(), value=node.get_value().createExpression(self.variable_lookup_table), role=node.get_role()))

    def visitSystemFunctionNode(self, node: SystemFunctionNode) -> None:
        arg_as_expressions = [arg.createExpression(self.variable_lookup_table) for arg in node.get_args()]
        self.add_to_function(SystemFunctionFactory().build(func=node.get_name(), args=arg_as_expressions, config=self.config))


    def visitActionFunctionNode(self, node: ActionFunctionNode):
        self.add_to_function(FunctionRunner(function_name=node.get_name(),
                                                                   function_registry=self.function_registry))

    def add_to_function(self, statement: Statement):
        if len(self.current_statement_context) is not 0:
            self.current_statement_context[-1].increment_statements()

        self.current_function_context.add_statement(statement)

    def visitContextEndNode(self, node: ContextEndNode):
        self.current_statement_context.pop()

    def visitIfElseContextNode(self, node) -> None:
        self.current_statement_context[-1].switch_context()

    def visitIfEndContextNode(self, node) -> None:
        self.current_statement_context.pop()

    def visitIfNode(self, node: IfNode) -> None:
        #Nested if not supporting
        statement = IfStatement(conditional=node.get_expression().createExpression(self.variable_lookup_table), function_context=self.current_function_context)

        self.current_statement_context.append(statement)
        self.current_function_context.add_statement(statement)
        
    def visitLoopNode(self, node: LoopNode) -> None:
        statement = LoopStatement(node.get_expression().createExpression(self.variable_lookup_table), function_context=self.current_function_context)
        self.current_statement_context.append(statement)
        self.current_function_context.add_statement(statement)

    def visitResultNode(self, node: ResultNode) -> None:
        self.current_scope.append(node.get_name())
        self.scope_to_function[node.get_name()] = dict()
        self.current_function_context = FunctionContext(name=node.get_name(),
                                                        variables=self.variable_lookup_table)
        current_scope = self.current_scope[-1]
        self.scope_to_function[current_scope][self.current_function_context.get_name()] = self.current_function_context

    def visitFunctionEndNode(self, node: FunctionEndNode) -> None:
        self.current_function_context.set_context_end()
