//2210277
grammar MiniGo;

@lexer::header {
from lexererr import *
}

@lexer::members {
    self.lastTokenType = None;
def emit(self):
    tk = self.type
    if tk != self.LINE_COMMENT:
        self.lastTokenType = tk;
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
        result = super().emit();
        return result;   

}

options{
	language = Python3;
}
program: stat EOF;
stat: program_content stat | program_content;

program_content: declare end_statement | define;

assign_operator:
	PLUS_ASSIGN
	| MINUS_ASSIGN
	| MUL_ASSIGN
	| DIV_ASSIGN
	| DOT_ASSIGN
	| MOD_ASSIGN;

block_body: block_body_element block_body | block_body_element;
block_body_element: statement_full;

expression_compare_operator:
	EQUAL
	| NOT_EQUAL
	| LESS
	| LESS_OR_EQUAL
	| GREATER
	| GREATER_OR_EQUAL;
expression_priority_2_operator: NOT | MINUS;
expression_priority_3_operator: MUL | DIV | MOD;
expression_priority_4_operator: PLUS | MINUS;

declare: declare_const | declare_var;
declare_var: VAR ID var_type | declare_var_init;
declare_var_init:
	VAR ID var_type_and_none ASSIGN init_value_for_all;
declare_const: CONST ID ASSIGN init_value_for_all;
declare_func:
	FUNCTION ID LEFT_PAREN list_func_parameters RIGHT_PAREN var_type_and_none LEFT_BRACE block_body
		RIGHT_BRACE;
declare_method:
	FUNCTION LEFT_PAREN ID ID RIGHT_PAREN ID LEFT_PAREN list_func_parameters RIGHT_PAREN
		var_type_and_none LEFT_BRACE block_body RIGHT_BRACE;

define: (
		define_struct
		| define_interface
		| declare_func
		| declare_method
	) end_statement;
define_struct:
	TYPE ID STRUCT LEFT_BRACE list_define_struct_content RIGHT_BRACE;
define_interface:
	TYPE ID INTERFACE LEFT_BRACE list_interface_content RIGHT_BRACE;
interface_content:
	ID LEFT_PAREN list_func_parameters RIGHT_PAREN var_type_and_none end_statement;
list_define_struct_content:
	ID var_type end_statement list_define_struct_content
	| ID var_type end_statement; //CHỗ này có sửa lại từ list_id -> ID
list_interface_content:
	interface_content list_interface_content
	| interface_content;
end_statement: SEMICOLON;
expr: expression end_statement;

struct_literal: ID struct_declare_init_in;
struct_declare_init_in:
	LEFT_BRACE struct_declare_init_content RIGHT_BRACE;
struct_declare_init_content:
	ID COLON init_value_for_all struct_declare_init_content_tail
	|;
struct_declare_init_content_tail:
	COMMA ID COLON init_value_for_all struct_declare_init_content_tail
	|;

expression: expression_compu | expression_assign;

expression_assign: lhs assign_operator init_value_for_all;
expression_compu: expression_number | expression_logic;
expression_logic: expression_priority_6 | expression_priority_7;

expression_number:
	expression_priority_1
	| expression_priority_2
	| expression_priority_3
	| expression_priority_4
	| expression_priority_5;

expression_priority_1:
	expression_priority_1 list_brace
	| expression_priority_1 Dot ID
	| expression_number_partner
	| expression_priority_1 Dot ID LEFT_PAREN list_parameters RIGHT_PAREN;
expression_priority_2:
	expression_priority_2_operator expression_priority_2
	| expression_priority_1;
expression_priority_3:
	expression_priority_3 expression_priority_3_operator expression_priority_2
	| expression_priority_2;
expression_priority_4:
	expression_priority_4 expression_priority_4_operator expression_priority_3
	| expression_priority_3;
expression_priority_5:
	expression_priority_5 expression_compare_operator expression_priority_4
	| expression_priority_4;

expression_priority_6:
	expression_priority_6 AND expression_priority_5
	| expression_priority_5;
expression_priority_7:
	expression_priority_7 OR expression_priority_6
	| expression_priority_6;

expression_number_partner:
	ID
	| literal_all
	| LEFT_PAREN expression_compu RIGHT_PAREN
	| statement_call;

lhs: ID | lhs Dot ID | lhs list_brace;

list_id: ID COMMA list_id | ID; //update list_id to end
list_func_parameters:
	list_id var_type list_func_parameters_tail
	|;
list_func_parameters_tail:
	COMMA list_id var_type list_func_parameters_tail
	|;

list_parameters: init_value_for_all list_parameters_tail |;
list_parameters_tail:
	COMMA init_value_for_all list_parameters_tail
	|;
list_brace:
	LEFT_BRACKET expression_compu RIGHT_BRACKET list_brace
	| LEFT_BRACKET expression_compu RIGHT_BRACKET; // đưa list_brace xuống cuối
list_bracket_init:
	LEFT_BRACKET (ID | INT_LITERAL) RIGHT_BRACKET list_bracket_init
	| LEFT_BRACKET (ID | INT_LITERAL) RIGHT_BRACKET;

expression_statement: expression;
statement_full: statement end_statement;
statement:
	statement_call
	| statement_call_method
	| CONTINUE
	| BREAK
	| statement_return
	| declare
	| statement_if_else
	| statement_for
	| expression_assign;
//|expression_statement;
statement_call:
	ID LEFT_PAREN list_parameters RIGHT_PAREN; //Chỗ này xóa 1 dòng
statement_call_method:
	statement_call_method_lhs Dot statement_call; //Chỗ này mới sửa lại
statement_call_method_lhs: //Chỗ này mới được thêm vào
	ID
	| statement_call
	| statement_call_method_lhs Dot statement_call
	| statement_call_method_lhs Dot ID
	| statement_call_method_lhs list_brace;
statement_for: FOR for_logic for_body;

for_logic: for_short | for_norm | for_range;

for_short: for_condition;
for_norm:
	for_initialization SEMICOLON for_condition SEMICOLON for_update;
for_range: ID COMMA ID DOT_ASSIGN RANGE expression_compu;

for_initialization:
	ID assign_operator init_value_for_all
	| VAR ID (scalar_type |) ASSIGN init_value_for_all;
for_condition: expression_logic;
for_update: ID assign_operator expression_compu;

for_body: LEFT_BRACE block_body RIGHT_BRACE;

statement_if_else:
	IF LEFT_PAREN expression RIGHT_PAREN LEFT_BRACE block_body RIGHT_BRACE ELSE statement_if_else
	| IF LEFT_PAREN expression RIGHT_PAREN LEFT_BRACE block_body RIGHT_BRACE ELSE LEFT_BRACE
		block_body RIGHT_BRACE
	| IF LEFT_PAREN expression RIGHT_PAREN LEFT_BRACE block_body RIGHT_BRACE;
statement_return: RETURN init_value_for_all | RETURN;

type_array: list_bracket_init var_type;
literal_all:
	INT_LITERAL
	| STRING_LITERAL
	| FLOAT_LITERAL
	| BOOL_LITERAL
	| NIL_LITERAL
	| composite_literal;
composite_literal: struct_literal | array_literal;
array_literal:
	list_bracket_init var_type LEFT_BRACE array_literal_element_list RIGHT_BRACE;
array_literal_element_list:
	array_literal_element array_literal_element_list_tail
	|;
array_literal_element_list_tail:
	COMMA array_literal_element array_literal_element_list_tail
	|;
array_literal_element:
	INT_LITERAL
	| FLOAT_LITERAL
	| STRING_LITERAL
	| BOOL_LITERAL
	| NIL_LITERAL
	| ID
	| struct_literal
	| LEFT_BRACE array_literal_element_list RIGHT_BRACE;

scalar_type: INT | FLOAT | STRING | BOOLEAN;
composite_type: ID | type_array;
var_type: scalar_type | composite_type;
var_type_and_none: var_type |;
init_value_for_all: expression_compu | literal_all;

//Define keywords
IF: 'if';
ELSE: 'else';
FOR: 'for';
RETURN: 'return';
FUNCTION: 'func';
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
fragment NIL: 'nil';
fragment TRUE: 'true';
fragment FALSE: 'false';

//Define operators
PLUS: '+';
MINUS: '-';
MUL: '*';
DIV: '/';
MOD: '%';
// /* */ */ -> MUL,DIV

EQUAL: '==';
NOT_EQUAL: '!=';
LESS: '<';
LESS_OR_EQUAL: '<=';
GREATER: '>';
GREATER_OR_EQUAL: '>=';

NOT: '!';
AND: '&&';
OR: '||';

ASSIGN: '=';
PLUS_ASSIGN: '+=';
MINUS_ASSIGN: '-=';
MUL_ASSIGN: '*=';
DIV_ASSIGN: '/=';
MOD_ASSIGN: '%=';
DOT_ASSIGN: ':=';
//Define Separators
LEFT_PAREN: '(';
RIGHT_PAREN: ')';
LEFT_BRACE: '{';
RIGHT_BRACE: '}';
LEFT_BRACKET: '[';
RIGHT_BRACKET: ']';
COMMA: ',';
SEMICOLON: ';';
COLON: ':';
//Define literals
INT_LITERAL:
	Decimal_Integers
	| Binary_Integers
	| Octal_Integers
	| Hexadecimal_Integers;
FLOAT_LITERAL: Digit+ Dot (Digit* Exponent?);
STRING_LITERAL: '"' STRING_CHAR* '"';
BOOL_LITERAL: TRUE | FALSE;
NIL_LITERAL: NIL;

//Define comment
LINE_COMMENT: '//' ~('\n' | '\r')* -> skip;
BLOCK_COMMENT: '/*' Block_Comment_Content* '*/' -> skip;

//Define Identifiers
ID: [a-zA-Z_] (Lowercase | Uppercase | Digit | Underscore)*;

NL:
	'\r'? '\n' {
        if self.lastTokenType is not None and self.lastTokenType in [
            self.ID, 
            self.INT_LITERAL,
            self.FLOAT_LITERAL, 
            self.BOOL_LITERAL, 
            self.STRING_LITERAL,
            self.NIL_LITERAL,
            self.RETURN, 
            self.CONTINUE, 
            self.BREAK, 
            self.RIGHT_PAREN, 
            self.RIGHT_BRACE, 
            self.RIGHT_BRACKET,
            self.INT,
            self.FLOAT,
            self.STRING,
            self.BOOLEAN      
        ]:
            self.type = self.SEMICOLON;
            self.text = ';'
            self.lastTokenType = self.SEMICOLON;
            return self.emit();
        else:
            self.skip();

}; //skip-convert newlines
WS: [ \t]+ -> skip; // skip spaces, tabs 

//DEFINE FRAGMENTS

fragment Lowercase: [a-z];
fragment Uppercase: [A-Z];
fragment Digit: [0-9];
Dot: '.';
fragment Exponent: [eE] [+-]? Digit+;
fragment HEX_Digit: [0-9a-fA-F];
fragment OCTAL_Digit: [0-7];
fragment Underscore: '_';

//define integers fragments
fragment Decimal_Integers: [1-9] Digit* | '0';
fragment Binary_Integers: '0' [bB] [01]+;
fragment Octal_Integers: '0' [oO] OCTAL_Digit+;
fragment Hexadecimal_Integers: '0' [xX] HEX_Digit+;

//define comment fragments
fragment Block_Comment_Char: ~[*]| '*' ~'/';
fragment Block_Comment_Content:
	BLOCK_COMMENT
	| Block_Comment_Char;
//define string fragments
fragment STRING_CHAR: ~["\\\n] | '\\' ([ntr] | '\\' | '"');

UNCLOSE_STRING:
	'"' STRING_CHAR* (EOF | '\r'? '\n') {
        if(len(self.text) >=2 and self.text[-1] == '\n' and self.text[-2] == '\r'):
            self.text = self.text[:-2];
        elif (self.text[-1] == '\n'):
            self.text = self.text[:-1];            
        raise UncloseString(self.text);
};
ILLEGAL_ESCAPE: '"' STRING_CHAR* ('\\' ~[ntr"\\] | | '\\');
ERROR_CHAR: .;