lexer grammar Tokens;

WS : [ \t\r\n\f]+ -> skip ;

// Symbols
SEMI : ';' ;
COMMA : ',' ;
LPAREN : '(' ;
RPAREN : ')' ;
LCURLY : '{' ;
RCURLY : '}' ;
ASSIGN : '=' ;
HAS : 'has' | 'HAS' ;
DOES : 'does' | 'DOES' ;
DOT : '.' ;

// Relational and Arithmetic Operators
RELATIONAL : '>' | '<' | '==' | '!=' | '>=' | '<=' ;
ARITHMETIC : '+' | '-' | '*' | '/' | '%' ;

// Expression Types
BOOLEAN : 'TRUE' | 'FALSE' ;
INTEGER : [0-9]+ ;

// Logical Operators
AND : 'AND' | 'and' ;
OR : 'OR' | 'or' ;
NOT : 'NOT' | 'not' ;

// Conditional Keywords
CONDITIONAL_IF : 'IF' | 'if' ;
CONDITIONAL_ELSE : 'ELSE' | 'else' ;
CONDITIONAL_RETURN : 'RETURN' | 'return' ;
CONDITIONAL_END : 'END IF' | 'end if' ;

// Loop Keywords
LOOP_START : 'LOOP' | 'loop' ;
LOOP_END : 'END LOOP' | 'end loop' ;

// Configuration Section Tokens
CONFIG_START : 'CONFIGURATION' ;
CARD_VAL_OVERRIDE_START : 'CARD_VALUE_OVERRIDE' ;
ACTIONS_START : 'ACTIONS' ;
VARIABLES_STRUCT_START : 'VARIABLES' ;

ROLES : 'ROLES' | 'roles' ;
ENTITY_CARD : 'ace' | 'king' | 'queen' | 'jack' | 'ACE' | 'KING' | 'QUEEN' | 'JACK' ;
DISABLEABLE_CARD : 'joker' | 'JOKER' ;
SET : 'SET' | 'set' ;


// Block and Section Markers
RESULT_START : 'RESULT' ;
GAME_START : 'GAME' ;
COMMON : 'COMMON' ;
USER_START : 'USER_OVERRIDE' ;
USER_END : 'END USER_OVERRIDE' ;
OVERRIDABLE_FUNCTION : 'on_turn' | 'setup' ;
FUNC_END : 'END FUNCTION' | 'end function' ;

SYSTEM_ACTION : 'pickCard' | 'skipTurn' ;
SYSTEM_FUNCTION : 'waitFor' ;
ACTION_CALLBACK : 'on_' (STRING | SYSTEM_ACTION) ;


STRING : [a-zA-Z_][a-zA-Z0-9_]* ;
