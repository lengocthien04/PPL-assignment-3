//2213250
grammar MiniGo;

@lexer::header {
from lexererr import *
}

@lexer::members {
def emit(self):
    tk = self.type
    if tk == self.UNCLOSE_STRING:       
        result = super().emit();
        raise UncloseString(result.text);
    elif tk == self.ILLEGAL_ESCAPE:
        result = super().emit();
        raise IllegalEscape(result.text);
    elif tk == self.ERROR_CHAR:
        result = super().emit();
        raise ErrorToken(result.text); 
    else:
        self.lastToken = super().emit()
        return self.lastToken;
}

options{
	language = Python3;
}

//! PARSER RULE

program: decl_list EOF;

decl_list: decl SEMICOLON decl_list | decl SEMICOLON;

decl:
	vardecl
	| constdecl
	| structdecl
	| interfacedecl
	| funcdecl
	| methoddecl;

vardecl: VAR ID ((type_ |) ASSIGN expression | type_);

constdecl: CONST ID ASSIGN expression;

structdecl: TYPE ID STRUCT LBRACE field_list RBRACE;

interfacedecl: TYPE ID INTERFACE LBRACE method_list RBRACE;
method_list: method method_list |;

method: ID LPAREN (parameters |) RPAREN (type_ |) SEMICOLON;

field_list: field field_list |;

field: ID type_ SEMICOLON;

funcdecl: FUNC ID LPAREN (parameters |) RPAREN (type_ |) block;

methoddecl:
	FUNC LPAREN (ID struct_type) RPAREN ID LPAREN (parameters |) RPAREN (
		type_
		|
	) block;

block: LBRACE statement_list RBRACE;

statement:
	vardecl
	| constdecl
	| invoke
	| assignment
	| if_statement
	| for_statement
	| break_statement
	| continue_statement
	| return_statement;

statement_list: statement SEMICOLON statement_list_tail;
statement_list_tail: statement SEMICOLON statement_list_tail |;

invoke: invoke_method | invoke_function;

invoke_method: invoke_prefix DOT invoke_function;

invoke_prefix:
	ID
	| invoke_function
	| invoke_prefix DOT invoke_function
	| invoke_prefix DOT ID
	| invoke_prefix index_list;
invoke_function: ID arguments;

for_statement:
	FOR (
		basic_for_statement
		| normal_for_statement
		| range_for_statement
	) block;

basic_for_statement: expression;

normal_for_statement: (
		ID assign_op expression
		| VAR ID (assignable_for_type |) ASSIGN expression
	) SEMICOLON expression SEMICOLON ID assign_op expression;

range_for_statement: ID COMMA ID COLON_ASSIGN RANGE expression;

assign_op:
	COLON_ASSIGN
	| ADD_ASSIGN
	| SUB_ASSIGN
	| MUL_ASSIGN
	| DIV_ASSIGN
	| MOD_ASSIGN;

assignable_for_type: STRING | INT | FLOAT | BOOLEAN;

if_statement:
	IF LPAREN expression RPAREN block (
		ELSE (block | if_statement)
	)?;

break_statement: BREAK;

continue_statement: CONTINUE;

return_statement: RETURN (expression |);

assignment:
	lhs (
		COLON_ASSIGN
		| ADD_ASSIGN
		| SUB_ASSIGN
		| MUL_ASSIGN
		| DIV_ASSIGN
		| MOD_ASSIGN
	) expression;

lhs: ID | lhs (DOT ID | index_list);

id_list: ID (COMMA ID)*;

expression_list: expression (COMMA expression)*;

parameters: id_list type_ (COMMA id_list type_)*;

type_:
	STRING
	| INT
	| FLOAT
	| BOOLEAN
	| array_type
	| struct_type;

array_type: (LBRACKET (INTEGER_LITERAL | ID) RBRACKET)+ type_;

struct_type: ID;

expression:
	expr
	| unary_operator expression
	| expression multiplicative_operator expression
	| expression additive_operator expression
	| expression relational_operator expression
	| expression AND expression
	| expression OR expression;

unary_operator: NOT | MINUS;

multiplicative_operator: MUL | DIV | MOD;

additive_operator: PLUS | MINUS;

relational_operator: EQ | NEQ | LSS | LEQ | GTR | GEQ;

expr:
	operand
	| invoke_method
	| invoke_function
	| expr (DOT ID | index_list);

operand: literal | ID | LPAREN expression RPAREN;

index_list: index index_list | index;

index: LBRACKET expression RBRACKET;

arguments: LPAREN (expression_list |) RPAREN;

literal:
	NIL
	| TRUE
	| FALSE
	| INTEGER_LITERAL
	| FLOATING_POINT_LITERAL
	| STRING_LITERAL
	| struct_literal
	| array_literal;

array_element_literal:
	NIL
	| TRUE
	| FALSE
	| INTEGER_LITERAL
	| FLOATING_POINT_LITERAL
	| STRING_LITERAL
	| struct_literal;

array_literal: array_type LBRACE array_body? RBRACE;

array_body: array_element (COMMA array_element)*;

array_element:
	ID
	| array_element_literal
	| LBRACE array_body? RBRACE;

struct_literal:
	struct_type LBRACE (
		ID COLLON expression (COMMA ID COLLON expression)*
		|
	) RBRACE;

//! Lexer rules KEYWORDS NIL
NIL: 'nil';

IF: 'if';
ELSE: 'else';
FOR: 'for';
RETURN: 'return';
FUNC: 'func';
TYPE: 'type';
STRUCT: 'struct';
INTERFACE: 'interface';
STRING: 'string';
INT: 'int';
FLOAT: 'float';
BOOLEAN: 'boolean';
CONST: 'const';
VAR: 'var';
CONTINUE: 'continue';
BREAK: 'break';
RANGE: 'range';

// BOOLEAN
TRUE: 'true';
FALSE: 'false';

// IDENTIFIER
ID: [a-zA-Z_][a-zA-Z_0-9]*;

// OPERATORS
PLUS: '+';
MINUS: '-';
MUL: '*';
DIV: '/';
MOD: '%';

ASSIGN: '=';
COLON_ASSIGN: ':=';
ADD_ASSIGN: '+=';
SUB_ASSIGN: '-=';
MUL_ASSIGN: '*=';
DIV_ASSIGN: '/=';
MOD_ASSIGN: '%=';

AND: '&&';
OR: '||';
NOT: '!';

EQ: '==';
NEQ: '!=';
LSS: '<';
LEQ: '<=';
GTR: '>';
GEQ: '>=';

DOT: '.';
COLLON: ':';

COMMA: ',';

// SEPERATOR

LPAREN: '(';
RPAREN: ')';
LBRACE: '{';
RBRACE: '}';
LBRACKET: '[';
RBRACKET: ']';

//! LITERALS 

//INTERGER
INTEGER_LITERAL:
	DECIMAL_INTEGER
	| BINARY_INTEGER
	| OCTAL_INTEGER
	| HEX_INTEGER;
fragment BINARY_INTEGER: '0' [bB] [0-1]+;
fragment OCTAL_INTEGER: '0' [oO] [0-7]+;
fragment HEX_INTEGER: '0' [xX] [0-9a-fA-F]+;
fragment DECIMAL_INTEGER: '0' | [1-9] [0-9]*;

// FLOATING POINT
FLOATING_POINT_LITERAL: DECIMAL_FLOAT;

fragment DECIMAL_FLOAT: [0-9]+ '.' [0-9]* EXPONENT?;
// Integer part, mandatory dot, optional fraction, optional exponent

fragment EXPONENT: [eE] [+-]? [0-9]+;

// STRING LITERALS
STRING_LITERAL: '"' STRING_CHAR* '"';

// COMMENTS
LINE_COMMENT: '//' ~[\r\n]* -> skip;

BLOCK_COMMENT:
	'/*' (BLOCK_COMMENT | ('*' ~'/') | ~'*')* '*/' -> skip;

NL:
	'\r'? '\n' {
    auto_NL_to_SEMICOLON = [
        MiniGoLexer.BREAK,
        MiniGoLexer.CONTINUE,
        MiniGoLexer.RETURN,
        MiniGoLexer.NIL,
        MiniGoLexer.INT,
        MiniGoLexer.FLOAT,
        MiniGoLexer.BOOLEAN,
        MiniGoLexer.STRING,
        MiniGoLexer.ID,
        MiniGoLexer.RPAREN,
        MiniGoLexer.RBRACE,
        MiniGoLexer.RBRACKET,
        MiniGoLexer.INTEGER_LITERAL,
        MiniGoLexer.FLOATING_POINT_LITERAL,
        MiniGoLexer.STRING_LITERAL,
        MiniGoLexer.TRUE,
        MiniGoLexer.FALSE
    ]

    if hasattr(self, "lastToken") and self.lastToken is not None:
        if self.lastToken.type in auto_NL_to_SEMICOLON:
            self.type = MiniGoLexer.SEMICOLON
            self.text = ';'
            return self.emit()
    self.skip()
};

SEMICOLON: ';';

// WHITESPACE
WS: [ \t\r]+ -> skip; // skip spaces, tabs 

ILLEGAL_ESCAPE: '"' STRING_CHAR* '\\' (~[ntr"\\] | EOF);
UNCLOSE_STRING: '"' STRING_CHAR*;

fragment STRING_CHAR: ~["\\\r\n] | '\\' [ntr"\\];
ERROR_CHAR: .;