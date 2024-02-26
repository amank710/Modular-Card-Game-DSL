from src.dsl_ast.ast_node import *
from src.dsl_ast.expression import ArithmeticExpressionNode, BinaryExpressionNode, VariableExpressionNode, ExpressionValueNode
from src.dsl_ast.nodes.action import ActionsNode, SystemActionNode, UserActionNode
from src.dsl_ast.nodes.variable import *
from src.dsl_ast.nodes.function import *
from src.factory.function_context.expressions.binary_expression import Relation
from src.factory.function_type import FunctionType
from src.factory.types.callback_type import CallbackType
from src.parser.Grammar import Grammar
from src.parser.GrammarVisitor import GrammarVisitor

from antlr4 import *
import logging


class AstVisitorGenerator(GrammarVisitor):
    def visitProgram(self, ctx: Grammar.ProgramContext):
        node = ProgramNode("PROGRAM")
        if ctx.config():
            node.add_child(self.visitConfig(ctx.config()))
        if ctx.game():
            node.add_child(self.visitGame(ctx.game()))
        if ctx.result():
            node.add_child(self.visitResult(ctx.result()))
        return node

    def visitCard_val_override(self, ctx: Grammar.Card_val_overrideContext):
        node = CardValueOverrideNode(
            "CARD_VALUE_OVERRIDE")
        if ctx.card_val_assignment():
            node.add_child(self.visitCard_val_assignment(
                ctx.card_val_assignment()))
        # TODO(arun): Handle "joker=false"
        # if ctx.card_disable():
        #   node.add_child(self.visitCard_disable)
        if ctx.roles():
            node.add_child(self.visitRoles(ctx.roles()))
        return node

    def visitCard_val_assignment(self, ctx: Grammar.Card_val_assignmentContext):
        node = CardsNode("CARDS")
        for card_ctx in ctx:
            card_node = CardNode(key=card_ctx.ENTITY_CARD().getText())
            for value in card_ctx.card_val():
                card_node.add_value(int(value.INTEGER().getText()))
            node.add_child(card_node)

        return node

    def visitRole(self, ctx: Grammar.RoleContext):
        return RoleNameNode(ctx.getText())

    def visitRoles(self, ctx: Grammar.RolesContext):
        node = RoleNode("ROLES")
        for and_roles in ctx:
            for role in and_roles.role():
                node.add_child(self.visitRole(role))
        return node

    def visitActions(self, ctx: Grammar.ActionsContext):
        actions_node = ActionsNode("ACTIONS")
        for action in ctx.user_actions():
            actions_node.add_child(self.visitUser_actions(action))
        return actions_node

    def visitUser_actions(self, ctx: Grammar.User_actionsContext):
        action_node = UserActionNode(name=ctx.STRING().getText())
        for user_actions_ctx in ctx.user_actions_block():
            if user_actions_ctx.SYSTEM_ACTION():
                action_node.add_child(SystemActionNode(
                    user_actions_ctx.SYSTEM_ACTION().getText()))
            elif user_actions_ctx.USER_ACTION():
                action_node.add_child(UserActionNode(
                    user_actions_ctx.USER_ACTION().getText()))

        return action_node

    def visitVariable_declarations_struct(self, ctx: Grammar.Variable_declarations_structContext):
        variables_node = VariableDeclarationsNode("VARIABLES")
        for variable in ctx.variable_declaration():
            variables_node.add_child(
                self.visitVariable_declarationContext(variable))
        return variables_node

    def visitFunctionCall(self, ctx: Grammar.FunctionCallContext):
        args = list()
        for e in ctx.expression():
            args.append(self.visitExpression(e))

        if ctx.SYSTEM_FUNCTION():
            node = SystemFunctionNode(ctx.SYSTEM_FUNCTION().getText(), args=args)
            return node
        elif ctx.USER_ACTION():
            node = ActionFunctionNode(ctx.USER_ACTION().getText(), args)
            return node
        else:
            logging.critical("AST Generation: unknown function call")

    def visitVariable_declarationContext(self, ctx: Grammar.Variable_declarationContext):
        # print('visitVariable_declarationContext')
        if ctx.common_variable_declaration():
            return self.visitCommon_variable_declaration(ctx.common_variable_declaration())
        elif ctx.role_variable_declaration():
            return self.visitRole_variable_declaration(ctx.role_variable_declaration())

    def visitCommon_variable_declaration(self, ctx: Grammar.Common_variable_declarationContext):
        print('visitCommon_variable_declaration')
        variable_name = ctx.variable_name().STRING().getText()
        return VariableDeclarationCommonNode(variable_name)

    def visitRole_variable_declaration(self, ctx: Grammar.Common_variable_declarationContext):
        variable_name = ctx.variable_name().STRING().getText()
        return VariableDeclarationRoleNode(name=variable_name, scope=ctx.role().STRING().getText())

    def visitConfig_struct(self, ctx: Grammar.Config_structContext):
        config_node = ConfigurationNode("CONFIGURATION")
        for struct in ctx:
            if struct.card_val_override():
                config_node.add_child(
                    self.visitCard_val_override(struct.card_val_override()))
            if struct.actions():
                config_node.add_child(self.visitActions(struct.actions()))
            if struct.variable_declarations_struct():
                config_node.add_child(
                    self.visitVariable_declarations_struct(struct.variable_declarations_struct()))
        return config_node

    def visitConfig(self, ctx):
        return self.visitConfig_struct(ctx.config_struct())

    def visitCommon_block(self, ctx: Grammar.Common_blockContext):
        common_fns_node = CommonFunctionsNode(FunctionType.COMMON)

        for function in ctx.function():
            function_node = self.visitFunction(function)
            common_fns_node.add_child(function_node)

        return common_fns_node

    def visitUser_block(self, ctx: Grammar.User_blockContext):
        user_fns_node = UserFunctionsNode(name=FunctionType.USER_OVERRIDE, role=ctx.role().STRING().getText())
        for function in ctx.function():
            user_fns_node.add_child(self.visitFunction(function))
        return user_fns_node

    def visitGame(self, ctx: Grammar.GameContext):
        game_node = GameNode("GAME")
        for struct in ctx.common_block():
            common_node = self.visitCommon_block(struct)
            game_node.add_child(common_node)
        for struct in ctx.user_block():
            user_node = self.visitUser_block(struct)
            game_node.add_child(user_node)
        return game_node

    def visitResult(self, ctx: Grammar.Result_blockContext):
        return self.visitResult_block(ctx.result_block())

    def visitFunction(self, ctx: Grammar.FunctionContext):
        name = ""
        if ctx.func_decl().OVERRIDABLE_FUNCTION():
            name = ctx.func_decl().OVERRIDABLE_FUNCTION().getText()
        elif ctx.func_decl().ACTION_CALLBACK():
            name = ctx.func_decl().ACTION_CALLBACK().getText()[3:]
        function_node = FunctionNode(name=name)

        for statement in ctx.func_statement():
            function_node.add_child(self.visitFunc_statement(statement))

        function_node.add_child(FunctionEndNode(name=name))

        return function_node

    def visitLoop(self, ctx: Grammar.LoopContext):
        conditional = self.visitExpression(ctx.expression())
        loop_node =  LoopNode(name="LOOP", expression=conditional)

        for statement in ctx.loop_body().func_statement():
            loop_node.add_child(self.visitFunc_statement(statement))

        loop_node.add_child(ContextEndNode(name="loop then"))

        return loop_node

    def visitConditional(self, ctx: Grammar.ConditionalContext):
        if_expression = ctx.expression()
        expression_node = self.visitExpression(if_expression)
        if_node = IfNode(name="IF", expression=expression_node)

        for statement in ctx.conditional_true().func_statement():
            if_node.add_child(self.visitFunc_statement(statement))
        
        if ctx.conditional_false():
            if_node.add_child(IfElseContext(name="else if"))
            for statement in ctx.conditional_false().func_statement():
                if_node.add_child(self.visitFunc_statement(statement))

        if_node.add_child(IfEndContext(name="else if"))


        return if_node

    def visitExpression(self, ctx: Grammar.ExpressionContext):
        if ctx.arithmeticExpression():
            left_expression = self.visitBaseExpression(ctx.baseExpression())
            right_expression = self.visitArithmeticExpression(ctx.arithmeticExpression())
            operand = ctx.arithmeticExpression().ARITHMETIC().getText()
            arithmetic_expression_node = ArithmeticExpressionNode(operator=operand, left=left_expression, right=right_expression)
            return arithmetic_expression_node
        elif ctx.binaryExpression():
            left_expression = self.visitBaseExpression(ctx.baseExpression())
            right_expression = self.visitBinaryExpression(ctx.binaryExpression())
            relation = ""
            if ctx.binaryExpression().binaryOperator().RELATIONAL():
                relation = ctx.binaryExpression().binaryOperator().RELATIONAL().getText()
            elif ctx.binaryExpression().binaryOperator().AND():
                relation = Relation.AND
            elif ctx.binaryExpression().binaryOperator().OR():
                relation = Relation.OR
            binary_expression_node = BinaryExpressionNode(name=relation, left=left_expression, right=right_expression)
            
            return binary_expression_node
        elif ctx.functionCall():
            return self.visitFunctionCall(ctx.functionCall())
        elif ctx.baseExpression():
            return self.visitBaseExpression(ctx.baseExpression())

    def visitBasicExpression(self, ctx: Grammar.BasicExpressionContext):
        #import pdb
        #pdb.set_trace()
        # TODO(arun): handle ENTITY_CARD correctly
        if (ctx.variableAccessor()):
            return VariableExpressionNode(access_context=self.visitVariableAccessor(ctx.variableAccessor()))
        elif(ctx.BOOLEAN()):
            return ExpressionValueNode((ctx.BOOLEAN().getText()).lower() == "true")
        elif (ctx.INTEGER()):
            return ExpressionValueNode(int(ctx.INTEGER().getText()))
        elif (ctx.STRING()):   
            return ExpressionValueNode(str(ctx.STRING().getText()))
        else:
            return "error: unknown basic expression"

    def visitArithmeticExpression(self, ctx: Grammar.ArithmeticExpressionContext):
        return self.visitExpression(ctx.expression())

    def visitGroupedExpression(self, ctx: Grammar.GroupedExpressionContext):
        return self.visitExpression(ctx.expression())

    def visitBaseExpression(self, ctx: Grammar.BaseExpressionContext):
        if ctx.basicExpression():
            return self.visitBasicExpression(ctx.basicExpression())
        elif ctx.groupedExpression():
            return self.visitGroupedExpression(ctx.groupedExpression())
        else:
            return "error: unknown base expression"

    def visitBinaryExpression(self, ctx: Grammar.BinaryExpressionContext):
        return self.visitExpression(ctx.expression())

    def visitBinaryOperator(self, ctx: Grammar.BinaryOperatorContext):
        return OperatorNode(ctx.getText())

    def visitConditional_true(self, ctx: Grammar.Conditional_trueContext):
        true_node = IfNode("THEN")
        # new_node = self.visitFunc_statement(ctx.func_statement())
        # for child in new_node.children:
        #     true_node.add_child(child)
        for statement in ctx.func_statement():
            true_node.add_child(self.visitFunc_statement(statement))
        # true_node.add_child(ContextEndNode(name=))
        return true_node

    def visitConditional_false(self, ctx: Grammar.Conditional_falseContext):
        else_node = IfNode("ELSE")
        # new_node = self.visitFunc_statement(
        #     ctx.func_statement())
        # for child in new_node.children:
        #     else_node.add_child(child)
        for statement in ctx.func_statement():
            else_node.add_child(self.visitFunc_statement(statement))
        return else_node

    def visitVariableAssignment(self, ctx: Grammar.VariableAssignmentContext):
        variable_assignment = DirectVariableAssignmentNode(access_context=self.visitVariableAccessor(ctx.variableAccessor()), value=self.visitExpression(ctx.expression()))
        if ctx.expression().functionCall():
            variable_assignment = DelayedVariableAssignmentNode(access_context=self.visitVariableAccessor(ctx.variableAccessor()), delay_function=self.visitFunctionCall(ctx.expression().functionCall()))
            
        return variable_assignment

    def visitVariableAccessor(self, ctx: Grammar.VariableAccessorContext):
        variable_name = ctx.variable_name().STRING().getText()
        if ctx.COMMON():
            return VariableDeclarationGlobalNode(name=variable_name)
        elif ctx.variable_name():
            return VariableDeclarationRoleNode(name=variable_name,
                                               scope=ctx.role().STRING().getText())

    def visitFunc_statement(self, ctx: Grammar.Func_statementContext):
        if ctx.loop():
            loop_node = self.visitLoop(ctx.loop())
            return loop_node
        elif ctx.conditional():
            if_node = self.visitConditional(ctx.conditional())
            return if_node
        elif ctx.variableAssignment():
            variable_node = self.visitVariableAssignment(ctx.variableAssignment())
            return variable_node
        elif ctx.functionCall():
            function_call_node = self.visitFunctionCall(
            ctx.functionCall())
            return function_call_node
        else:
            logging.critical("AST Generation: Unknown statement type")


    def visitResult_block(self, ctx: Grammar.Result_blockContext):
        result_node = ResultNode(FunctionType.RESULT)

        for statement in ctx.func_statement():
            new_node = self.visitFunc_statement(statement)
            result_node.add_child(new_node)

        result_node.add_child(FunctionEndNode(name="RESULT"))
        return result_node
