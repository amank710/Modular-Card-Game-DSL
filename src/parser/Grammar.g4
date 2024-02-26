parser grammar Grammar;

options {
    tokenVocab=Tokens; // Using the lexer definitions from Tokens
}

program : config game result EOF ;

config : CONFIG_START config_struct+ ;

config_struct
    : card_val_override
    | actions
    | variable_declarations_struct
    ;

card_val_override : CARD_VAL_OVERRIDE_START (card_val_assignment | card_disable | roles)+ ;

card_disable : DISABLEABLE_CARD ASSIGN BOOLEAN SEMI ;

card_val_assignment : ENTITY_CARD ASSIGN card_val (AND card_val)* SEMI ;

card_val : INTEGER ;

actions : ACTIONS_START (user_actions)+ ;

user_actions : SET STRING DOES user_actions_block (AND user_actions_block)* SEMI;

user_actions_block : (SYSTEM_ACTION | user_action);

user_action : STRING ;

roles : ROLES ASSIGN role (AND role)* SEMI ;

role : STRING ;

variable_declarations_struct : VARIABLES_STRUCT_START (variable_declaration)+ ;

variable_declaration : SET (common_variable_declaration | role_variable_declaration);
common_variable_declaration : COMMON HAS variable_name SEMI ;
role_variable_declaration : role HAS variable_name SEMI ;

variable_name : STRING ;

game : GAME_START (common_block | user_block)* ;

common_block : COMMON (function)+ ;

user_block : USER_START role (function)+ ;

function : func_decl (func_statement)* FUNC_END ;

func_decl : (OVERRIDABLE_FUNCTION | ACTION_CALLBACK) LPAREN RPAREN ;

func_statement
    : loop
    | variableAssignment
    | conditional
    | functionCall SEMI
    ;

loop : LOOP_START LPAREN expression RPAREN loop_body LOOP_END ;

loop_body : (func_statement)+;

variableAssignment :  (variableAccessor) ASSIGN expression SEMI ;

conditional : CONDITIONAL_IF LPAREN expression RPAREN conditional_true (conditional_false)? CONDITIONAL_END ;

conditional_true : (func_statement)+ ;

conditional_false : CONDITIONAL_ELSE (func_statement)+;

functionCall
    : SYSTEM_FUNCTION (LPAREN expression (COMMA expression)* RPAREN)?
    | user_action (LPAREN expression (COMMA expression)* RPAREN)?;

expression
    : baseExpression (binaryExpression | arithmeticExpression)?
    | functionCall
    ;

arithmeticExpression 
    : (ARITHMETIC expression ) ;

baseExpression
    : basicExpression
    | groupedExpression
    ;

binaryExpression
    : (binaryOperator expression)
    ;

basicExpression
    : BOOLEAN
    | INTEGER
    | STRING
    | ENTITY_CARD
    | variableAccessor
    ;

variableAccessor: (COMMON | role) DOT variable_name;

groupedExpression : LPAREN expression RPAREN ;

binaryOperator
    : RELATIONAL
    | AND
    | OR
    ;

result : RESULT_START result_block;

result_block : func_statement+;
