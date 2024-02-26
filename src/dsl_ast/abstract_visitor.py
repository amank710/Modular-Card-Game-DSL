
class AbstractVisitor():
    def visitProgramNode(self, node) -> None:
        raise NotImplementedError

    def visitConfigurationNode(self, node) -> None:
        raise NotImplementedError

    def visitRoleNode(self, node) -> None:
        raise NotImplementedError

    def visitCardNode(self, node) -> None:
        raise NotImplementedError

    def visitUserActionNode(self, node) -> None:
        raise NotImplementedError

    def visitVariableValueNode(self, node) -> None:
        raise NotImplementedError

    def visitCardValueOverrideNode(self, node) -> None:
        raise NotImplementedError

    # Actions
    def visitActionNode(self, node) -> None:
        raise NotImplementedError

    def visitSystemActionNode(self, node) -> None:
        raise NotImplementedError

    def visitUserActionNode(self, node) -> None:
        raise NotImplementedError

    def visitGameNode(self, node) -> None:
        raise NotImplementedError

    def visitCommonNode(self, node) -> None:
        raise NotImplementedError

    def visitFunctionNode(self, node) -> None:
        raise NotImplementedError

    def visitBodyNode(self, node) -> None:
        raise NotImplementedError

    # If handling
    def visitIfNode(self, node) -> None:
        raise NotImplementedError

    def visitIfEndContextNode(self, node) -> None:
        raise NotImplementedError

    def visitIfElseContextNode(self, node) -> None:
        raise NotImplementedError

    def visitLoopNode(self, node) -> None:
        raise NotImplementedError

    def visitVariableNode(self, node) -> None:
        raise NotImplementedError

    def visitResultNode(self, node) -> None:
        raise NotImplementedError

    def visitUserDefinedNode(self, node) -> None:
        raise NotImplementedError

    def visitLongExpressionNode(self, node) -> None:
        raise NotImplementedError

    def visitIfExpressionNode(self, node) -> None:
        raise NotImplementedError

    def visitCardNode(self, node) -> None:
        raise NotImplementedError

    def visitRoleNameNode(self, node) -> None:
        raise NotImplementedError

    # Variables
    def visitVariableDeclarationRoleNode(self, node) -> None:
        raise NotImplementedError

    def visitVariableDeclarationGlobalNode(self, node) -> None:
        raise NotImplementedError

    def visitVariableDeclarationMixedNode(self):
        raise NotImplementedError

    def visitDirectVariableAssignmentNode(self, node) -> None:
        raise NotImplementedError
    
    def visitIndirectVariableAssignmentNode(self, node) -> None:
        raise NotImplementedError

    # Functions
    def visitCommonFunctionsNode(self, node) -> None:
        raise NotImplementedError

    def visitUserFunctionsNode(self, node) -> None:
        raise NotImplementedError

    def visitUserFunctionNode(self, node) -> None:
        raise NotImplementedError

    def visitSystemFunctionNode(self, node) -> None:
        raise NotImplementedError
    
    def visitContextEndNode(self, node) -> None:
        raise NotImplementedError

    def visitFunctionEndNode(self, node) -> None:
        raise NotImplementedError
