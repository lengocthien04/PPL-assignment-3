from MiniGoVisitor import MiniGoVisitor
from MiniGoParser import MiniGoParser
from AST import *


class ASTGeneration(MiniGoVisitor):
    # program: decl_list EOF;
    def visitProgram(self, ctx: MiniGoParser.ProgramContext):
        return Program(self.visit(ctx.decl_list()))
    #decl_list: decl SEMICOLON decl_list | decl SEMICOLON;
    def visitDecl_list(self, ctx: MiniGoParser.Decl_listContext):
        if ctx.getChildCount() == 3:
            return self.visit(ctx.decl()) + self.visit(ctx.decl_list())
        return self.visit(ctx.decl())
        
    # decl: vardecl | constdecl | structdecl | interfacedecl | funcdecl | methoddecl 	| invoke;
    def visitDecl(self, ctx: MiniGoParser.DeclContext):
        return [self.visit(ctx.getChild(0))]

    # vardecl: VAR ID ((type_ |) ASSIGN expression | type_);
    def visitVardecl(self, ctx: MiniGoParser.VardeclContext):
        type_ = None
        expression = None
        if ctx.type_():
            type_ = self.visit(ctx.type_())
        if ctx.expression():
            expression = self.visit(ctx.expression())
        return VarDecl(ctx.ID().getText(), 
                       type_,
                       expression)

    # constdecl: CONST ID ASSIGN expression;
    def visitConstdecl(self, ctx: MiniGoParser.ConstdeclContext):
        return ConstDecl(ctx.ID().getText(), None, self.visit(ctx.expression()))

    # structdecl: TYPE ID STRUCT LBRACE field_list RBRACE;
    def visitStructdecl(self, ctx: MiniGoParser.StructdeclContext):
        return StructType(ctx.ID().getText(), self.visit(ctx.field_list()),[])

    # interfacedecl: TYPE ID INTERFACE LBRACE method_list RBRACE;
    def visitInterfacedecl(self, ctx: MiniGoParser.InterfacedeclContext):
        return InterfaceType(ctx.ID().getText(), self.visit(ctx.method_list()))

    # method_list: method method_list | ;
    def visitMethod_list(self, ctx: MiniGoParser.Method_listContext):
        if ctx.method_list():
            if self.visit(ctx.method_list()) != []:
                return [self.visit(ctx.method())] + self.visit(ctx.method_list())
            return [self.visit(ctx.method())]
        return []

    # method: ID LPAREN (parameters |) RPAREN (type_ |) SEMICOLON;
    def visitMethod(self, ctx: MiniGoParser.MethodContext):
        params = self.visit(ctx.parameters()) if ctx.parameters() else []
        params_type = [x.parType for x in params]
        retType = self.visit(ctx.type_()) if ctx.type_() else VoidType()
        return Prototype(ctx.ID().getText(), params_type, retType)

    # field_list: field field_list | ;
    def visitField_list(self, ctx: MiniGoParser.Field_listContext):
        if ctx.field_list():
           if self.visit(ctx.field_list()) != [[]]:
              return  self.visit(ctx.field()) + self.visit(ctx.field_list())
           return self.visit(ctx.field())
        return [[]]

    # field: ID type_ SEMICOLON;

    def visitField(self, ctx: MiniGoParser.FieldContext):
        return [[ctx.ID().getText(), self.visit(ctx.type_())]]

    # funcdecl: FUNC ID LPAREN (parameters |) RPAREN (type_ |) block;
    def visitFuncdecl(self, ctx: MiniGoParser.FuncdeclContext):
        params = self.visit(ctx.parameters()) if ctx.parameters() else []
        retType = self.visit(ctx.type_()) if ctx.type_() else VoidType()

        return FuncDecl(ctx.ID().getText(), params, retType, self.visit(ctx.block()))

    # methoddecl:
    #   FUNC LPAREN (ID struct_type) RPAREN ID LPAREN (parameters |) RPAREN (type_ |) block;
    def visitMethoddecl(self, ctx: MiniGoParser.MethoddeclContext):
        methodName = ctx.ID(0).getText()
        retType = self.visit(ctx.struct_type())
        params = self.visit(ctx.parameters()) if ctx.parameters() else []
        funcType = self.visit(ctx.type_()) if ctx.type_() else VoidType()
        func =  FuncDecl(ctx.ID(1).getText(), params, funcType, self.visit(ctx.block()))
        return MethodDecl(methodName, retType, func)

    # block: LBRACE statement_list RBRACE;
    def visitBlock(self, ctx: MiniGoParser.BlockContext):
        return Block(self.visit(ctx.statement_list()))

    # statement_list: statement SEMICOLON statement_list_tail;
    def visitStatement_list(self, ctx: MiniGoParser.Statement_listContext):
        stmts = [self.visit(ctx.statement())]
        if ctx.statement_list_tail():
            return stmts + self.visit(ctx.statement_list_tail())
        return stmts

    # statement_list_tail: statement SEMICOLON statement_list_tail | ;
    def visitStatement_list_tail(self, ctx: MiniGoParser.Statement_list_tailContext):
        if ctx.getChildCount() == 0:
            return []
        stmts = [self.visit(ctx.statement())]
        if ctx.statement_list_tail():
            return stmts + self.visit(ctx.statement_list_tail())
        return stmts

    # statement:
    #   vardecl |constdecl | ivoke | assignment | if_statement |
    #   for_statement | break_statement | continue_statement | return_statement;
    def visitStatement(self, ctx: MiniGoParser.StatementContext):
        return self.visit(ctx.getChild(0))

    def visitInvoke(self, ctx: MiniGoParser.InvokeContext):
        return self.visit(ctx.getChild(0))
    

     #invoke_method: invoke_prefix DOT invoke_function;
    def visitInvoke_method(self, ctx: MiniGoParser.Invoke_methodContext):
        receiver = self.visit(ctx.invoke_prefix())
        fun = self.visit(ctx.invoke_function())
        metName = fun.funName
        args =  fun.args
        return MethCall(receiver, metName, args)
    def visitStatement(self, ctx: MiniGoParser.Invoke_prefixContext):
        return self.visit(ctx.getChild(0))
    
    #invoke_function: ID arguments;
    def visitInvoke_function(self, ctx: MiniGoParser.Invoke_functionContext):
        
        return FuncCall(ctx.ID().getText(), self.visit(ctx.arguments()))
    # invoke_prefix:
     # ID
     # | invoke_function
     # | invoke_prefix DOT invoke_function
     # | invoke_prefix DOT ID
     # | invoke_prefix index_list;
    def visitInvoke_prefix(self, ctx: MiniGoParser.Invoke_prefixContext):
        if ctx.getChildCount() ==1:
            if(ctx.ID()):
                return Id(ctx.ID().getText())
            return self.visit(ctx.invoke_function())
        elif ctx.getChildCount() == 2:
            return ArrayCell(self.visit(ctx.invoke_prefix()) , self.visit(ctx.index_list()) )
        elif ctx.ID():

            return FieldAccess(self.visit(ctx.invoke_prefix()), ctx.ID().getText())
        receiver = self.visit(ctx.invoke_prefix())
        fun = self.visit(ctx.invoke_function())
        metName = fun.funName
        args =  fun.args
        return MethCall(receiver, metName, args)                                       
        


    # assignment: lhs (COLON_ASSIGN | ADD_ASSIGN | SUB_ASSIGN | MUL_ASSIGN | DIV_ASSIGN | MOD_ASSIGN) expression;
    def visitAssignment(self, ctx: MiniGoParser.AssignmentContext):
        op = ctx.getChild(1).getText()
        rhs = self.visit(ctx.getChild(2))
        lhs =self.visit(ctx.lhs())
        
        if op == '+=':
            rhs = BinaryOp('+',lhs, rhs)
        if op == '-=':
            rhs = BinaryOp('-',lhs, rhs)
        if op == '*=':
            rhs = BinaryOp('*',lhs, rhs)  
        if op == '/=':
            rhs = BinaryOp('/',lhs, rhs)   
        if op == '%=':
            rhs = BinaryOp('%',lhs, rhs)                                                                
        return Assign(lhs, rhs)

    # lhs: ID | lhs (DOT ID | index);
    def visitLhs(self, ctx: MiniGoParser.LhsContext):
        if ctx.getChildCount() == 1:
            return Id(ctx.ID().getText())
        # Here you would handle field access and array indexing as needed.
        if ctx.ID():
            return FieldAccess(self.visit(ctx.lhs()), ctx.ID().getText() )
        return ArrayCell(self.visit(ctx.lhs()), self.visit(ctx.index_list()))


    # id_list: ID (COMMA ID)*;
    def visitId_list(self, ctx: MiniGoParser.Id_listContext):
        return [id.getText() for id in ctx.ID()]

    # expression_list: expression (COMMA expression)*;
    def visitExpression_list(self, ctx: MiniGoParser.Expression_listContext):
        return [self.visit(expr) for expr in ctx.expression()]

    # parameters: id_list type_ (COMMA id_list type_)*;
    def visitParameters(self, ctx: MiniGoParser.ParametersContext):
        first_ids = [self.visit(id_list) for id_list in ctx.id_list()]
        first_types = [self.visit(t) for t in ctx.type_()]
        pair = []
        for i  in range(0, len(first_ids)):
            for _id in first_ids[i]:
                pair =  pair + [ParamDecl(_id, first_types[i])]
        return pair



    # type_: STRING | INT | FLOAT | BOOLEAN | array_type | struct_type;
    def visitType_(self, ctx: MiniGoParser.Type_Context):
        if ctx.STRING():
            return StringType()
        elif ctx.INT():
            return IntType()
        elif ctx.FLOAT():
            return FloatType()
        elif ctx.BOOLEAN():
            return BoolType()
        elif ctx.array_type():
            return self.visit(ctx.array_type())
        elif ctx.struct_type():
            return self.visit(ctx.struct_type())

    # array_type: (LBRACKET (INTEGER_LITERAL | ID) RBRACKET)+ type_;
    def visitArray_type(self, ctx: MiniGoParser.Array_typeContext):
        dims = []
        num_child = ctx.getChildCount()
        for i in range(1,num_child,3):
            if ctx.getChild(i).getText()[0].isdigit():
                dims = dims + [IntLiteral(ctx.getChild(i).getText())]
            else:
                dims = dims + [Id(ctx.getChild(i).getText())]
        type_ = self.visit(ctx.type_())
        return ArrayType(dims, type_)

    # struct_type: ID;
    def visitStruct_type(self, ctx: MiniGoParser.Struct_typeContext):
        return Id(ctx.ID().getText())

    # expression:
    #   expr | unary_operator expression | expression multiplicative_operator expression |
    #   expression additive_operator expression | expression relational_operator expression |
    #   expression AND expression | expression OR expression;
    def visitExpression(self, ctx: MiniGoParser.ExpressionContext):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.getChild(0))
        elif ctx.getChildCount() == 2:
            op = self.visit(ctx.unary_operator())
            return UnaryOp(op, self.visit(ctx.expression(0)))
        elif ctx.getChildCount() == 3:
            left = self.visit(ctx.expression(0))
            op = ctx.getChild(1).getText()
            right = self.visit(ctx.expression(1))
            return BinaryOp(op, left, right)

    # unary_operator: NOT | MINUS;
    def visitUnary_operator(self, ctx: MiniGoParser.Unary_operatorContext):
        return (ctx.getChild(0).getText())

    # multiplicative_operator: MUL | DIV | MOD;
    def visitMultiplicative_operator(self, ctx: MiniGoParser.Multiplicative_operatorContext):
        return (ctx.getChild(0).getText())

    # additive_operator: PLUS | MINUS;
    def visitAdditive_operator(self, ctx: MiniGoParser.Additive_operatorContext):
        return (ctx.getChild(0).getText())

    # relational_operator: EQ | NEQ | LSS | LEQ | GTR | GEQ;
    def visitRelational_operator(self, ctx: MiniGoParser.Relational_operatorContext):
        return (ctx.getChild(0).getText())

    # expr: expr:	operand| invoke_method| invoke_function| expr (DOT ID | index_list);
    def visitExpr(self, ctx: MiniGoParser.ExprContext):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.getChild(0))
        elif ctx.ID():
            return FieldAccess(self.visit(ctx.expr()), ctx.ID().getText() )
        else:
            return ArrayCell(self.visit(ctx.expr()), self.visit(ctx.index_list()))


    # operand: literal | ID | LPAREN expression RPAREN;
    def visitOperand(self, ctx: MiniGoParser.OperandContext):
        if ctx.literal():
            return self.visit(ctx.literal())
        elif ctx.ID():
            return Id(ctx.ID().getText())
        else:
            return self.visit(ctx.expression())

    #index_list: index index_list | index;
    def visitIndex_list(self, ctx: MiniGoParser.Index_listContext):
        if ctx.index_list():
            return [self.visit(ctx.index())] + self.visit(ctx.index_list()) 
        return [self.visit(ctx.index())]
    # index: LBRACKET expression RBRACKET;
    def visitIndex(self, ctx: MiniGoParser.IndexContext):
        return self.visit(ctx.expression())
   

    # arguments: LPAREN (expression_list |) RPAREN;
    def visitArguments(self, ctx: MiniGoParser.ArgumentsContext):
        return self.visit(ctx.expression_list()) if ctx.expression_list() else []

    # literal:
    #   NIL | TRUE | FALSE | INTEGER_LITERAL | FLOATING_POINT_LITERAL |
    #   STRING_LITERAL | struct_literal | array_literal;
    def visitLiteral(self, ctx: MiniGoParser.LiteralContext):
        if ctx.NIL():
            return NilLiteral()
        elif ctx.TRUE():
            return BooleanLiteral(True)
        elif ctx.FALSE():
            return BooleanLiteral(False)
        elif ctx.INTEGER_LITERAL():
            return IntLiteral(ctx.INTEGER_LITERAL().getText())
        elif ctx.FLOATING_POINT_LITERAL():
            return FloatLiteral(ctx.FLOATING_POINT_LITERAL().getText())
        elif ctx.STRING_LITERAL():
            return StringLiteral(ctx.STRING_LITERAL().getText())
        elif ctx.struct_literal():
            return self.visit(ctx.struct_literal())
        elif ctx.array_literal():
            return self.visit(ctx.array_literal())

    # array_element_literal:
    # 	NIL
    # 	| TRUE
    # 	| FALSE
    # 	| INTEGER_LITERAL
    # 	| FLOATING_POINT_LITERAL
    # 	| STRING_LITERAL
    # 	| struct_literal;
    def visitArray_element_literal(self, ctx: MiniGoParser.Array_element_literalContext):
        if ctx.NIL():
            return NilLiteral()
        elif ctx.TRUE():
            return BooleanLiteral(True)
        elif ctx.FALSE():
            return BooleanLiteral(False)
        elif ctx.INTEGER_LITERAL():
            return IntLiteral(ctx.INTEGER_LITERAL().getText())
        elif ctx.FLOATING_POINT_LITERAL():
            return FloatLiteral(float(ctx.FLOATING_POINT_LITERAL().getText()))
        elif ctx.STRING_LITERAL():
            return StringLiteral(ctx.STRING_LITERAL().getText())
        elif ctx.struct_literal():
            return self.visit(ctx.struct_literal())


    # array_literal: array_type LBRACE array_body? RBRACE;
    def visitArray_literal(self, ctx: MiniGoParser.Array_literalContext):
        a = self.visit(ctx.array_type())
        dimens = a.dimens
        arrayType = a.eleType
        body = self.visit(ctx.array_body()) if ctx.array_body() else []
        return ArrayLiteral(dimens, arrayType, body)

    # array_body: array_element (COMMA array_element)*;
    def visitArray_body(self, ctx: MiniGoParser.Array_bodyContext):
        return [self.visit(child) for child in ctx.array_element()]

    # array_element: ID | literal | LBRACE array_body? RBRACE;
    def visitArray_element(self, ctx: MiniGoParser.Array_elementContext):
        if ctx.ID():
            return Id(ctx.ID().getText())
        elif ctx.array_element_literal():
            return self.visit(ctx.array_element_literal())
        else:
            return self.visit(ctx.array_body()) if ctx.array_body() else []

    # struct_literal:
    #   struct_type LBRACE (ID COLLON expression (COMMA ID COLLON expression)*)? RBRACE;
    def visitStruct_literal(self, ctx: MiniGoParser.Struct_literalContext):
        ids = [id.getText() for id in ctx.ID()]
        exprs = [self.visit(x) for x in ctx.expression()]
        name = self.visit(ctx.struct_type())
        return StructLiteral(name.name, zip(ids, exprs))

    # if_statement: IF LPAREN expression RPAREN block (ELSE (block | if_statement))?;
    def visitIf_statement(self, ctx: MiniGoParser.If_statementContext):
        condition = self.visit(ctx.expression())
        thenBlock = self.visit(ctx.block(0))
        elseBlock = None
        if ctx.ELSE():
            elseBlock = self.visit(ctx.getChild(6))
        return If(condition, thenBlock, elseBlock)

    # for_statement:
    #   FOR (basic_for_statement | normal_for_statement | range_for_statement) block;
    def visitFor_statement(self, ctx: MiniGoParser.For_statementContext):
        if ctx.basic_for_statement() is not None:
            return ForBasic(self.visit(ctx.basic_for_statement()), self.visit(ctx.block()))
        if ctx.normal_for_statement() is not None:
            init, cond, step = self.visit(ctx.normal_for_statement())
            return ForStep(init, cond, step, self.visit(ctx.block()))
        if ctx.range_for_statement() is not None:
            idx, value, arr = self.visit(ctx.range_for_statement())
            return ForEach(idx, value, arr, self.visit(ctx.block()))

    # basic_for_statement: expression;
    def visitBasic_for_statement(self, ctx: MiniGoParser.Basic_for_statementContext):
        return self.visit(ctx.expression())
    
    # assign_op: ASSIGN | PLUS_ASSIGN | MINUS_ASSIGN | MUL_ASSIGN | DIV_ASSIGN | MOD_ASSIGN;

    # normal_for_statement:
    #   (ID assign_op expression | VAR ID (assignable_for_type |) ASSIGN expression)
    #   SEMICOLON expression SEMICOLON ID assign_op expression;
    def visitNormal_for_statement(self, ctx: MiniGoParser.Normal_for_statementContext):
        init = None
        type_ =None
        if ctx.VAR():
            if(ctx.assignable_for_type()):
                type_ = self.visit(ctx.assignable_for_type())
            init = VarDecl(ctx.ID(0).getText(), type_, self.visit(ctx.expression(0)))
        else:
            lhs = Id(ctx.ID(0).getText())
            op = self.visit(ctx.assign_op(0))
            rhs = self.visit(ctx.expression(0))
            if op == '+=':
                rhs = BinaryOp('+',lhs, rhs)
            if op == '-=':
                rhs = BinaryOp('-',lhs, rhs)
            if op == '*=':
                rhs = BinaryOp('*',lhs, rhs)  
            if op == '/=':
                rhs = BinaryOp('/',lhs, rhs)   
            if op == '%=':
                rhs = BinaryOp('%',lhs, rhs)  
            init = Assign(lhs, rhs)
        Exprs = ctx.expression()
        condition = self.visit(Exprs[1])
        lhs = Id(ctx.ID(1).getText())
        op = self.visit(ctx.getChild(ctx.getChildCount()-2))
        rhs = self.visit(ctx.expression(2))
        if op == '+=':
            rhs = BinaryOp('+',lhs, rhs)
        if op == '-=':
            rhs = BinaryOp('-',lhs, rhs)
        if op == '*=':
            rhs = BinaryOp('*',lhs, rhs)  
        if op == '/=':
            rhs = BinaryOp('/',lhs, rhs)   
        if op == '%=':
            rhs = BinaryOp('%',lhs, rhs)  
        increment = Assign(lhs, rhs)
        return [init, condition, increment]
    def visitAssignable_for_type(self, ctx: MiniGoParser.Assignable_for_typeContext):
        if ctx.STRING():
            return StringType()
        elif ctx.INT():
            return IntType()
        elif ctx.FLOAT():
            return FloatType()
        elif ctx.BOOLEAN():
            return BoolType()

    def visitAssign_op(self, ctx: MiniGoParser.Assign_opContext):
        return ctx.getChild(0).getText()

    # range_for_statement: ID COMMA ID COLON_ASSIGN RANGE expression;
    def visitRange_for_statement(self, ctx: MiniGoParser.Range_for_statementContext):
        id1 = Id(ctx.ID(0).getText())
        id2 = Id(ctx.ID(1).getText())
        rangeExpr = self.visit(ctx.expression())
        return [id1, id2, rangeExpr]

    # break_statement: BREAK;
    def visitBreak_statement(self, ctx: MiniGoParser.Break_statementContext):
        return Break()

    # continue_statement: CONTINUE;
    def visitContinue_statement(self, ctx: MiniGoParser.Continue_statementContext):
        return Continue()

    # return_statement: RETURN (expression |);
    def visitReturn_statement(self, ctx: MiniGoParser.Return_statementContext):
        if ctx.expression():
            return Return(self.visit(ctx.expression()))
        else:
            return Return(None)

   

    

