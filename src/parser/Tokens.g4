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
CONFIG_END : 'END CONFIGURATION' ;
CARD_VAL_OVERRIDE_START : 'CARD_VALUE_OVERRIDE' ;
CARD_VAL_OVERRIDE_END : 'END CARD_VALUE_OVERRIDE' ;
ACTIONS_START : 'ACTIONS' ;
ACTIONS_END : 'END ACTIONS' ;
VARIABLES_STRUCT_START : 'VARIABLES' ;
VARIABLES_STRUCT_END : 'END VARIABLES' ;

ROLES : 'ROLES' | 'roles' ;
ENTITY_CARD : 'ace' | 'king' | 'queen' | 'joker' ;
SET : 'SET' | 'set' ;


// Block and Section Markers
RESULT_START : 'RESULT' ;
END_RESULT : 'END RESULT' ;
GAME_START : 'GAME' ;
GAME_END : 'END GAME' ;
COMMON_START : 'COMMON' ;
COMMON_END : 'END COMMON' ;
USER_START : 'USER_OVERRIDE' WS* STRING;
USER_END : 'END USER_OVERRIDE' ;
FUNC_START : 'on_turn()' | 'setup()' | ACTION_CALLBACK ;
FUNC_END : 'END FUNCTION' | 'end function' ;

SYSTEM_ACTION : 'pickCard()' | 'hideCard()' ;
USER_ACTION : STRING LPAREN RPAREN ;
ACTION_CALLBACK : 'on_' (USER_ACTION | SYSTEM_ACTION) ;

STRING : [a-zA-Z_][a-zA-Z0-9_]* ;