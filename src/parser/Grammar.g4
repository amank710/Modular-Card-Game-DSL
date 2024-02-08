parser grammar Grammar;

options {
    tokenVocab=Tokens; // Using the lexer definitions from Tokens
}

program : config game result_block EOF ;

config : CONFIG_START config_struct+ CONFIG_END ;

config_struct
    : card_val_override
    | actions
    | variables_struct
    ;

card_val_override : CARD_VAL_OVERRIDE_START (cards | roles)+ CARD_VAL_OVERRIDE_END ;

cards : ENTITY_CARD ASSIGN basicExpression SEMI ;

actions : ACTIONS_START (user_actions)+ ACTIONS_END ;

user_actions : SET STRING DOES user_actions_block (AND user_actions_block)* SEMI;

user_actions_block : (SYSTEM_ACTION | USER_ACTION);

roles : ROLES ASSIGN STRING (AND STRING)* SEMI ;

role : STRING ;

variables_struct : VARIABLES_STRUCT_START (variable_assignment)+ VARIABLES_STRUCT_END ;

variable_assignment : SET STRING HAS basicExpression SEMI ;

game : GAME_START (common_block | user_block)* GAME_END ;

common_block : COMMON_START (function)+ COMMON_END ;

user_block : USER_START (function)+ USER_END ;

function : FUNC_START (func_statement)+ FUNC_END ;

func_statement
    : loop
    | variable
    | conditional
    | action
    ;

loop : LOOP_START LPAREN expression RPAREN (func_statement)+ LOOP_END ;

variable : STRING ASSIGN expression SEMI ;

conditional : CONDITIONAL_IF LPAREN expression RPAREN ifBlock (CONDITIONAL_ELSE elseBlock)? CONDITIONAL_END ;

ifBlock : (func_statement)+ ;

elseBlock : (func_statement)+ ;

action : (STRING | SYSTEM_ACTION) SEMI ;

expression
    : basicExpression (binaryOperator basicExpression)?
    | groupedExpression
    | arithmeticExpression
    ;

arithmeticExpression : basicExpression ARITHMETIC basicExpression ;

basicExpression
    : BOOLEAN
    | INTEGER
    | STRING
    ;

groupedExpression : LPAREN expression RPAREN ;

binaryOperator
    : RELATIONAL
    | AND
    | OR
    | NOT
    ;

result_block : RESULT_START (resultContent)+ END_RESULT ;

resultContent
    : conditional
    | variable
    ;