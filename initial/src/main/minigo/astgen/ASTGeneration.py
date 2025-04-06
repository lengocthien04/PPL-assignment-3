from MiniGoVisitor import MiniGoVisitor
from MiniGoParser import MiniGoParser
from AST import *

class ASTGeneration(MiniGoVisitor):
    # Visit a parse tree produced by MiniGoParser#program.
    def visitProgram(self, ctx:MiniGoParser.ProgramContext):
        return Program(self.visit(ctx.stat()))


    # Visit a parse tree produced by MiniGoParser#stat.
    # stat: program_content stat| program_content
    def visitStat(self, ctx:MiniGoParser.StatContext):
        list_stat = []
        if ctx.stat():
            list_stat.append(self.visit(ctx.program_content()))
            list_stat.extend(self.visit(ctx.stat()))
        elif ctx.program_content():
            list_stat.append(self.visit(ctx.program_content()))

        return list_stat


    # Visit a parse tree produced by MiniGoParser#program_content.
    # program_content: declare end_statement | define;
    def visitProgram_content(self, ctx:MiniGoParser.Program_contentContext):
        
        if ctx.declare():
            return self.visit(ctx.declare())
        elif ctx.define():
            return ctx.define().accept(self)
            # return self.visit(ctx.define())


    # Visit a parse tree produced by MiniGoParser#assign_operator.
    # assign_operator:PLUS_ASSIGN|MINUS_ASSIGN|MUL_ASSIGN|DIV_ASSIGN|DOT_ASSIGN|MOD_ASSIGN;
    def visitAssign_operator(self, ctx:MiniGoParser.Assign_operatorContext):
        return ctx.getChild(0).getText()


    # Visit a parse tree produced by MiniGoParser#block_body.
    # block_body: block_body_element block_body|block_body_element;
    
    def visitBlock_body(self, ctx:MiniGoParser.Block_bodyContext):
        body_block = []
        if ctx.block_body():
            body_block.append(self.visit(ctx.block_body_element()))
            body_block.extend(self.visit(ctx.block_body()))
        elif ctx.block_body_element():
            body_block.append(self.visit(ctx.block_body_element()))
        
        return body_block

    # Visit a parse tree produced by MiniGoParser#block_body_element.
    # block_body_element: statement_full;
    def visitBlock_body_element(self, ctx:MiniGoParser.Block_body_elementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by MiniGoParser#expression_compare_operator.
    # expression_compare_operator:EQUAL|NOT_EQUAL|LESS|LESS_OR_EQUAL|GREATER|GREATER_OR_EQUAL;	
    def visitExpression_compare_operator(self, ctx:MiniGoParser.Expression_compare_operatorContext):
        if ctx.EQUAL():
            return "=="
        elif ctx.NOT_EQUAL():
            return "!="
        elif ctx.LESS():
            return "<"
        elif ctx.LESS_OR_EQUAL():
            return "<="
        elif ctx.GREATER():
            return ">"
        elif ctx.GREATER_OR_EQUAL():
            return ">="
    
    # Visit a parse tree produced by MiniGoParser#expression_priority_2_operator.
    # expression_priority_2_operator: NOT|MINUS;
    def visitExpression_priority_2_operator(self, ctx:MiniGoParser.Expression_priority_2_operatorContext):
        if ctx.NOT():
            return "!"
        elif ctx.MINUS():    
            return "-"

    # Visit a parse tree produced by MiniGoParser#expression_priority_3_operator.
    # expression_priority_3_operator: MUL|DIV|MOD;
    def visitExpression_priority_3_operator(self, ctx:MiniGoParser.Expression_priority_3_operatorContext):
        if ctx.MUL():
            return "*"
        elif ctx.DIV():
            return "/"
        elif ctx.MOD():
            return "%"

    # Visit a parse tree produced by MiniGoParser#expression_priority_4_operator.
    # expression_priority_4_operator: PLUS|MINUS; 
    def visitExpression_priority_4_operator(self, ctx:MiniGoParser.Expression_priority_4_operatorContext):
        if ctx.PLUS():
            return "+"
        elif ctx.MINUS():
            return "-"

    # Visit a parse tree produced by MiniGoParser#declare.
    # declare:  declare_const |declare_var;
    def visitDeclare(self, ctx:MiniGoParser.DeclareContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by MiniGoParser#declare_var.
    # declare_var: VAR ID var_type | declare_var_init;
    def visitDeclare_var(self, ctx:MiniGoParser.Declare_varContext):
        if ctx.getChildCount() == 3:
            vName = ctx.ID().getText()
            vType = self.visit(ctx.var_type())
            vInit = None
            return VarDecl(vName,vType,vInit)
        else:
            return self.visit(ctx.declare_var_init())

    # Visit a parse tree produced by MiniGoParser#declare_var_init.
    # declare_var_init: VAR ID var_type_and_none  ASSIGN init_value_for_all ;
    def visitDeclare_var_init(self, ctx:MiniGoParser.Declare_var_initContext):
        vName = ctx.ID().getText()
        vType = self.visit(ctx.var_type_and_none())
        vInit = self.visit(ctx.init_value_for_all())
        return VarDecl(vName,vType,vInit)

    # Visit a parse tree produced by MiniGoParser#declare_const.
    # declare_const: CONST ID ASSIGN init_value_for_all;
    def visitDeclare_const(self, ctx:MiniGoParser.Declare_constContext):
        cName = ctx.ID().getText()
        cType = None
        cInit = self.visit(ctx.init_value_for_all())
        return ConstDecl(cName,cType,cInit)

    # Visit a parse tree produced by MiniGoParser#declare_func.
    # declare_func: FUNCTION ID LEFT_PAREN list_func_parameters RIGHT_PAREN var_type_and_none LEFT_BRACE block_body  RIGHT_BRACE ;
    def visitDeclare_func(self, ctx:MiniGoParser.Declare_funcContext):
        fName = ctx.ID().getText()
        fParams = []
        fRetType = VoidType()
        if ctx.list_func_parameters() and self.visit(ctx.list_func_parameters()) is not None:
            fParams = self.visit(ctx.list_func_parameters())
        if ctx.var_type_and_none() and self.visit(ctx.var_type_and_none()):
            fRetType = self.visit(ctx.var_type_and_none())
        fBody = self.visit(ctx.block_body())
        return FuncDecl(fName,fParams,fRetType,Block(fBody))

    # Visit a parse tree produced by MiniGoParser#declare_method.
    # declare_method: FUNCTION LEFT_PAREN ID ID RIGHT_PAREN ID LEFT_PAREN list_func_parameters RIGHT_PAREN var_type_and_none LEFT_BRACE block_body  RIGHT_BRACE ;
    def visitDeclare_method(self, ctx:MiniGoParser.Declare_methodContext):
        l_child = ctx.getChildren()
        rcs = ctx.getChild(2).getText()
        rcT = ctx.getChild(3).getText()
        fName = ctx.getChild(5).getText()
        fParams = []
        fRefType = VoidType()
        if ctx.list_func_parameters() and self.visit(ctx.list_func_parameters()):
            fParams = self.visit(ctx.list_func_parameters())
        if ctx.var_type_and_none() and self.visit(ctx.var_type_and_none()):
            fRefType = self.visit(ctx.var_type_and_none())
        fBody = self.visit(ctx.block_body())
        return MethodDecl(rcs,Id(rcT),FuncDecl(fName,fParams,fRefType,Block(fBody)))

    # Visit a parse tree produced by MiniGoParser#define.
    # define: define_struct end_statement
    # | define_interface end_statement
    # |declare_func end_statement
    # |declare_method  end_statement;
    def visitDefine(self, ctx:MiniGoParser.DefineContext):
        if ctx.define_struct():
            return self.visit(ctx.define_struct())
        elif ctx.define_interface():
            return self.visit(ctx.define_interface())
        elif ctx.declare_func():
            return self.visit(ctx.declare_func())
        elif ctx.declare_method():
            return self.visit(ctx.declare_method())

    # Visit a parse tree produced by MiniGoParser#define_struct.
    # define_struct: TYPE ID STRUCT LEFT_BRACE list_define_struct_content RIGHT_BRACE;
    def visitDefine_struct(self, ctx:MiniGoParser.Define_structContext):
        name = ctx.ID().getText()
        elements = self.visit(ctx.list_define_struct_content())
        methods = []
        return StructType(name,elements,methods)

    # Visit a parse tree produced by MiniGoParser#define_interface.
    # define_interface: TYPE ID INTERFACE LEFT_BRACE list_interface_content RIGHT_BRACE;
    def visitDefine_interface(self, ctx:MiniGoParser.Define_interfaceContext):
        name = ctx.ID().getText()
        methods = self.visit(ctx.list_interface_content())
        return InterfaceType(name,methods)

    # Visit a parse tree produced by MiniGoParser#interface_content.
    # interface_content: ID LEFT_PAREN list_func_parameters RIGHT_PAREN var_type_and_none end_statement;
    def visitInterface_content(self, ctx:MiniGoParser.Interface_contentContext):
        name = ctx.ID().getText()
        params = self.visit(ctx.list_func_parameters())
        params_ = [i.parType for i in params]
        retType = VoidType()
        if ctx.var_type_and_none() and self.visit(ctx.var_type_and_none()):
            retType = self.visit(ctx.var_type_and_none())
        return Prototype(name,params_,retType)


    # Visit a parse tree produced by MiniGoParser#list_define_struct_content.
    # list_define_struct_content: 
    # ID var_type end_statement list_define_struct_content
    # | ID var_type end_statement;
    def visitList_define_struct_content(self, ctx:MiniGoParser.List_define_struct_contentContext):
        list_struct_content = []
        if ctx.getChildCount() == 3:
            field_name = ctx.ID().getText()
            l_type = self.visit(ctx.var_type())
            list_struct_content.append((field_name,l_type))
        else:
            field_name = ctx.ID().getText()
            l_type = self.visit(ctx.var_type())
            list_struct_content.append((field_name,l_type))
            list_struct_content.extend(self.visit(ctx.list_define_struct_content()))
        return list_struct_content

    # Visit a parse tree produced by MiniGoParser#list_interface_content.
    # list_interface_content:  interface_content list_interface_content|interface_content;
    def visitList_interface_content(self, ctx:MiniGoParser.List_interface_contentContext):
        list_interface_content = []
        if ctx.getChildCount() == 1:
            list_interface_content.append(self.visit(ctx.interface_content()))
        else:
            list_interface_content.append(self.visit(ctx.interface_content()))
            list_interface_content.extend(self.visit(ctx.list_interface_content()))
        return list_interface_content

    # Visit a parse tree produced by MiniGoParser#end_statement.
    def visitEnd_statement(self, ctx:MiniGoParser.End_statementContext):
        pass


    # Visit a parse tree produced by MiniGoParser#expr.
    # expr: expression end_statement;
    def visitExpr(self, ctx:MiniGoParser.ExprContext):
        return self.visit(ctx.expression())


    # Visit a parse tree produced by MiniGoParser#struct_literal.
    # struct_literal: ID struct_declare_init_in;
    def visitStruct_literal(self, ctx:MiniGoParser.Struct_literalContext):
        name = ctx.ID().getText()
        elements = self.visit(ctx.struct_declare_init_in())
        return StructLiteral(name,elements)


    # Visit a parse tree produced by MiniGoParser#struct_declare_init_in.
    # struct_declare_init_in: LEFT_BRACE struct_declare_init_content RIGHT_BRACE;
    def visitStruct_declare_init_in(self, ctx:MiniGoParser.Struct_declare_init_inContext):
        return self.visit(ctx.struct_declare_init_content())


    # Visit a parse tree produced by MiniGoParser#struct_declare_init_content.
    # struct_declare_init_content: ID COLON init_value_for_all struct_declare_init_content_tail|;
    def visitStruct_declare_init_content(self, ctx:MiniGoParser.Struct_declare_init_contentContext):
        list_content = []
        if ctx.ID():
            field = ctx.ID().getText()
            value = self.visit(ctx.init_value_for_all())
            list_content.append((field,value))
            list_content.extend(self.visit(ctx.struct_declare_init_content_tail()))
        return list_content


    # Visit a parse tree produced by MiniGoParser#struct_declare_init_content_tail.
    # struct_declare_init_content_tail: COMMA ID COLON init_value_for_all struct_declare_init_content_tail|;
    def visitStruct_declare_init_content_tail(self, ctx:MiniGoParser.Struct_declare_init_content_tailContext):
        list_content = []
        if ctx.COMMA():
            field = ctx.ID().getText()
            value = self.visit(ctx.init_value_for_all())
            list_content.append((field,value))
            list_content.extend(self.visit(ctx.struct_declare_init_content_tail()))
        return list_content


    # Visit a parse tree produced by MiniGoParser#expression.
    # expression: expression_compu | expression_assign;
    def visitExpression(self, ctx:MiniGoParser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#expression_assign.
    # expression_assign: lhs assign_operator init_value_for_all ;
    def visitExpression_assign(self, ctx:MiniGoParser.Expression_assignContext):
        lhs = self.visit(ctx.lhs())
        op = ctx.assign_operator().getText()
        rhs = self.visit(ctx.init_value_for_all())
        if op == ":=":
            return Assign(lhs,rhs)
        elif op == "+=":
            return Assign(lhs,BinaryOp('+',lhs,rhs))
        elif op == "-=":
            return Assign(lhs,BinaryOp('-',lhs,rhs))
        elif op == "*=":
            return Assign(lhs,BinaryOp('*',lhs,rhs))
        elif op == "/=":
            return Assign(lhs,BinaryOp('/',lhs,rhs))
        elif op == "%=":
            return Assign(lhs,BinaryOp('%',lhs,rhs))


    # Visit a parse tree produced by MiniGoParser#expression_compu.
    # expression_compu: expression_number | expression_logic;
    def visitExpression_compu(self, ctx:MiniGoParser.Expression_compuContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#expression_logic.
    # expression_logic: expression_priority_6 | expression_priority_7;
    def visitExpression_logic(self, ctx:MiniGoParser.Expression_logicContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#expression_number.
    # expression_number: 
    # expression_priority_1
    # |expression_priority_2
    # |expression_priority_3
    # |expression_priority_4
    # |expression_priority_5
    # ;
    def visitExpression_number(self, ctx:MiniGoParser.Expression_numberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#expression_priority_1.
    # expression_priority_1: 
    # expression_priority_1 list_brace
    # | expression_priority_1 Dot ID 
    # | expression_number_partner
    # | expression_priority_1  Dot ID LEFT_PAREN list_parameters RIGHT_PAREN
    # ;
    def visitExpression_priority_1(self, ctx:MiniGoParser.Expression_priority_1Context):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.expression_number_partner())
        elif ctx.getChildCount() == 2:
            arr = self.visit(ctx.expression_priority_1())
            idx = self.visit(ctx.list_brace())
            return ArrayCell(arr,idx)
        elif ctx.getChildCount() == 3:
            rec = self.visit(ctx.expression_priority_1())
            field = ctx.ID().getText()
            return FieldAccess(rec,field)
        else:
            rec = self.visit(ctx.expression_priority_1())
            metName = ctx.ID().getText()
            args = self.visit(ctx.list_parameters())
            return MethCall(rec,metName,args)


    # Visit a parse tree produced by MiniGoParser#expression_priority_2.
  
    # expression_priority_2: 
    # expression_priority_2_operator expression_priority_2
    # |expression_priority_1
    # ;
    def visitExpression_priority_2(self, ctx:MiniGoParser.Expression_priority_2Context):
        if ctx.getChildCount() == 1:
            return self.visitChildren(ctx)
        else:
            op = ctx.expression_priority_2_operator().getText()
            body = self.visit(ctx.expression_priority_2())
            return UnaryOp(op,body)


    # Visit a parse tree produced by MiniGoParser#expression_priority_3.
    # expression_priority_3: 
    # expression_priority_3 expression_priority_3_operator expression_priority_2
    # |expression_priority_2
    # ;
    def visitExpression_priority_3(self, ctx:MiniGoParser.Expression_priority_3Context):
        if ctx.getChildCount() == 1:
            return self.visitChildren(ctx)
        else:
            op = ctx.expression_priority_3_operator().getText()
            left = self.visit(ctx.expression_priority_3())
            right = self.visit(ctx.expression_priority_2())
            return BinaryOp(op,left,right)


    # Visit a parse tree produced by MiniGoParser#expression_priority_4.
    # expression_priority_4:
    # expression_priority_4 expression_priority_4_operator expression_priority_3
    # |expression_priority_3
    def visitExpression_priority_4(self, ctx:MiniGoParser.Expression_priority_4Context):
        if ctx.getChildCount() == 1:
            return self.visitChildren(ctx)
        else:
            op = ctx.expression_priority_4_operator().getText()
            left = self.visit(ctx.expression_priority_4())
            right = self.visit(ctx.expression_priority_3())
            return BinaryOp(op,left,right)

    # Visit a parse tree produced by MiniGoParser#expression_priority_5.
    # expression_priority_5: 
    # expression_priority_5 expression_compare_operator expression_priority_4
    # |expression_priority_4
    # ;
    def visitExpression_priority_5(self, ctx:MiniGoParser.Expression_priority_5Context):
        if ctx.getChildCount() == 1:
            return self.visitChildren(ctx)
        else:
            op = ctx.expression_compare_operator().getText()
            left = self.visit(ctx.expression_priority_5())
            right = self.visit(ctx.expression_priority_4()) 
            return BinaryOp(op,left,right)


    # Visit a parse tree produced by MiniGoParser#expression_priority_6.
    # expression_priority_6: 
    # expression_priority_6 AND
    # expression_priority_5|expression_priority_5;

    def visitExpression_priority_6(self, ctx:MiniGoParser.Expression_priority_6Context):
        if ctx.getChildCount() == 1:
            return self.visitChildren(ctx)
        else:
            op = ctx.AND().getText()
            left = self.visit(ctx.expression_priority_6())
            right = self.visit(ctx.expression_priority_5())
            return BinaryOp(op,left,right)

    # Visit a parse tree produced by MiniGoParser#expression_priority_7.
    # expression_priority_7:
    # expression_priority_7 OR expression_priority_6
    # |expression_priority_6;
    def visitExpression_priority_7(self, ctx:MiniGoParser.Expression_priority_7Context):
        if ctx.getChildCount() == 1:
            return self.visitChildren(ctx)
        else:
            op = ctx.OR().getText()
            left = self.visit(ctx.expression_priority_7())
            right = self.visit(ctx.expression_priority_6())
            return BinaryOp(op,left,right)


    # Visit a parse tree produced by MiniGoParser#expression_number_partner.
    # expression_number_partner: ID|literal_all | LEFT_PAREN expression_compu RIGHT_PAREN | statement_call;
    def visitExpression_number_partner(self, ctx:MiniGoParser.Expression_number_partnerContext):
        if ctx.ID():
            return Id(ctx.ID().getText())
        elif ctx.literal_all():
            return self.visit(ctx.literal_all())
        elif ctx.LEFT_PAREN():
            return self.visit(ctx.expression_compu())
        else:
            return self.visit(ctx.statement_call())

    # Visit a parse tree produced by MiniGoParser#lhs.
    # lhs: ID | lhs  Dot ID | lhs list_brace;
    def visitLhs(self, ctx:MiniGoParser.LhsContext):        
        if ctx.getChildCount() == 3:
            rec = self.visit(ctx.lhs())
            field = ctx.ID().getText()
            return FieldAccess(rec,field)
        elif ctx.getChildCount() == 2:
            arr = self.visit(ctx.lhs())
            idx = self.visit(ctx.list_brace())
            return ArrayCell(arr,idx)
        else:
            return Id(ctx.ID().getText()) # Chỗ này chưa rõ Error

    # Visit a parse tree produced by MiniGoParser#list_id.
    # list_id: ID COMMA list_id | ID;
    def visitList_id(self, ctx:MiniGoParser.List_idContext):
        list_id = []
        if ctx.getChildCount() == 3:
            list_id.append(ctx.ID().getText())
            list_id.extend(self.visit(ctx.list_id()))
        else:
            list_id.append(ctx.ID().getText())
        return list_id

    # Visit a parse tree produced by MiniGoParser#list_func_parameters.
    # list_func_parameters: list_id var_type list_func_parameters_tail |;
    # Khúc này đang có looxim về sữa
    def visitList_func_parameters(self, ctx:MiniGoParser.List_func_parametersContext):
        list_param = []
        if ctx.getChildCount() == 3:
            lId = self.visit(ctx.list_id())
            lType = self.visit(ctx.var_type())
            for i in lId:
                list_param.append(ParamDecl(i,lType))
            list_param.extend(self.visit(ctx.list_func_parameters_tail()))
        return list_param

    # Visit a parse tree produced by MiniGoParser#list_func_parameters_tail.
    # list_func_parameters_tail: COMMA list_id var_type list_func_parameters_tail |;
    def visitList_func_parameters_tail(self, ctx:MiniGoParser.List_func_parameters_tailContext):
        list_param = []
        if ctx.COMMA():
            lId = self.visit(ctx.list_id())
            lType = self.visit(ctx.var_type())
            for i in lId:
                list_param.append(ParamDecl(i,lType))
            list_param.extend(self.visit(ctx.list_func_parameters_tail()))
        return list_param

    # Visit a parse tree produced by MiniGoParser#list_parameters.
    # list_parameters: init_value_for_all list_parameters_tail | ;
    def visitList_parameters(self, ctx:MiniGoParser.List_parametersContext):
        list_param = []
        if ctx.getChildCount() == 2:
            list_param.append(self.visit(ctx.init_value_for_all()))
            list_param.extend(self.visit(ctx.list_parameters_tail()))
        return list_param

    # Visit a parse tree produced by MiniGoParser#list_parameters_tail.
    # list_parameters_tail: COMMA init_value_for_all list_parameters_tail|;
    def visitList_parameters_tail(self, ctx:MiniGoParser.List_parameters_tailContext):
        list_param = []
        if ctx.COMMA():
            list_param.append(self.visit(ctx.init_value_for_all()))
            list_param.extend(self.visit(ctx.list_parameters_tail()))
        return list_param


    # Visit a parse tree produced by MiniGoParser#list_brace.
    # list_brace: LEFT_BRACKET expression_compu RIGHT_BRACKET list_brace | LEFT_BRACKET expression_compu RIGHT_BRACKET;
    def visitList_brace(self, ctx:MiniGoParser.List_braceContext):
        list_param = []
        if ctx.getChildCount() == 3:
            list_param.append(self.visit(ctx.expression_compu()))
        else:
            list_param.append(self.visit(ctx.expression_compu()))
            list_param.extend(self.visit(ctx.list_brace()))
        return list_param

    # Visit a parse tree produced by MiniGoParser#list_bracket_init.
    # list_bracket_init: 
    # LEFT_BRACKET (ID|INT_LITERAL) RIGHT_BRACKET list_bracket_init
    # |LEFT_BRACKET (ID|INT_LITERAL) RIGHT_BRACKET ;
    def visitList_bracket_init(self, ctx:MiniGoParser.List_bracket_initContext):
        list_init = []
        if ctx.getChildCount() == 3:
            if ctx.ID():
                list_init.append(Id(ctx.ID().getText())) # Chỗ này chưa rõ Error
            elif ctx.INT_LITERAL():
                list_init.append(IntLiteral(self.convert_to_int(ctx.INT_LITERAL().getText())))
        else:
            if ctx.ID():
                list_init.append(Id(ctx.ID().getText()))
            elif ctx.INT_LITERAL():
                list_init.append(IntLiteral(self.convert_to_int(ctx.INT_LITERAL().getText())))
            list_init.extend(self.visit(ctx.list_bracket_init()))
        return list_init


    # Visit a parse tree produced by MiniGoParser#expression_statement.
    # expression_statement: expression;
    def visitExpression_statement(self, ctx:MiniGoParser.Expression_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#statement_full.
    # statement_full: statement end_statement;
    def visitStatement_full(self, ctx:MiniGoParser.Statement_fullContext):
        return self.visit(ctx.statement())


    # Visit a parse tree produced by MiniGoParser#statement.
    # Visit a parse tree produced by MiniGoParser#statement.
    # statement: 
    # statement_call
    # |statement_call_method 
    # | CONTINUE 
    # | BREAK 
    # | statement_return 
    # | declare 
    # | statement_if_else 
    # | statement_for
    # |expression_assign;
    def visitStatement(self, ctx:MiniGoParser.StatementContext):
        if ctx.statement_call():
            return self.visit(ctx.statement_call())
        elif ctx.statement_call_method():
            return self.visit(ctx.statement_call_method())
        elif ctx.CONTINUE():
            return Continue()
        elif ctx.BREAK():
            return Break()
        elif ctx.statement_return():
            return self.visit(ctx.statement_return())
        elif ctx.declare():
            return self.visit(ctx.declare())
        elif ctx.statement_if_else():
            return self.visit(ctx.statement_if_else())
        elif ctx.statement_for():
            return self.visit(ctx.statement_for())
        elif ctx.expression_assign():
            return self.visit(ctx.expression_assign())


    # Visit a parse tree produced by MiniGoParser#statement_call.
    # statement_call: ID LEFT_PAREN list_parameters RIGHT_PAREN
    def visitStatement_call(self, ctx:MiniGoParser.Statement_callContext):
        funName = ctx.ID().getText()
        args = self.visit(ctx.list_parameters())
        return FuncCall(funName,args)

    # Visit a parse tree produced by MiniGoParser#statement_call_method.
    # statement_call_method: statement_call_method_lhs Dot statement_call; //Chỗ này mới sửa lại
    def visitStatement_call_method(self, ctx:MiniGoParser.Statement_call_methodContext):
        rec = self.visit(ctx.statement_call_method_lhs())
        funcCall = self.visit(ctx.statement_call())
        metName = funcCall.funName
        args = funcCall.args
        return MethCall(rec,metName,args)
            
    # Visit a parse tree produced by MiniGoParser#statement_call_method_lhs.
    # statement_call_method_lhs: //Chỗ này mới được thêm vào
    # ID
    # |statement_call
    # |statement_call_method_lhs Dot statement_call
    # |statement_call_method_lhs Dot ID 
    # |statement_call_method_lhs list_brace
    # ;

    def visitStatement_call_method_lhs(self, ctx:MiniGoParser.Statement_call_method_lhsContext):
        if ctx.getChildCount() == 1:
            if ctx.ID():
                return Id(ctx.ID().getText())
            return self.visitChildren(ctx)
        elif ctx.statement_call():
            rec = self.visit(ctx.statement_call_method_lhs())
            funcCall = self.visit(ctx.statement_call())
            metName = funcCall.funName
            args = funcCall.args
            return MethCall(rec,metName,args)
        elif ctx.list_brace():
            arr = self.visit(ctx.statement_call_method_lhs())
            idx = self.visit(ctx.list_brace())
            return ArrayCell(arr,idx)
        else:
            rec = self.visit(ctx.statement_call_method_lhs())
            field = ctx.ID().getText()
            return FieldAccess(rec,field)
    
    # Visit a parse tree produced by MiniGoParser#statement_for.
    # statement_for: FOR for_logic for_body;
    def visitStatement_for(self, ctx:MiniGoParser.Statement_forContext):
        for_logic, for_type = self.visit(ctx.for_logic())
        for_body = self.visit(ctx.for_body())
        if for_type == 'Basic':
            return ForBasic(for_logic,Block(for_body))
        elif for_type == 'Step':
            return ForStep(for_logic[0],for_logic[1],for_logic[2],Block(for_body))
        elif for_type == 'Each':
            return ForEach(for_logic[0],for_logic[1],for_logic[2],Block(for_body))

    # Visit a parse tree produced by MiniGoParser#for_logic.
    # for_logic: for_short | for_norm | for_range;
    def visitFor_logic(self, ctx:MiniGoParser.For_logicContext):
        if ctx.for_short():
            return [self.visit(ctx.for_short()),'Basic']
        elif ctx.for_norm():
            return [self.visit(ctx.for_norm()),'Step']
        elif ctx.for_range():
            return [self.visit(ctx.for_range()),'Each']

    # Visit a parse tree produced by MiniGoParser#for_short.
    # for_short: for_condition;
    def visitFor_short(self, ctx:MiniGoParser.For_shortContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#for_norm.
    # for_norm: for_initialization SEMICOLON for_condition SEMICOLON for_update;
    def visitFor_norm(self, ctx:MiniGoParser.For_normContext):
        init = self.visit(ctx.for_initialization())
        cond = self.visit(ctx.for_condition())
        upda = self.visit(ctx.for_update())
        return [init,cond,upda]


    # Visit a parse tree produced by MiniGoParser#for_range.
    # for_range: ID COMMA ID DOT_ASSIGN RANGE expression_compu;
    def visitFor_range(self, ctx:MiniGoParser.For_rangeContext):
        idx = ctx.getChild(0).getText()
        value = ctx.getChild(2).getText()
        arr = self.visit(ctx.expression_compu())
        return [Id(idx),Id(value),arr]

    # Visit a parse tree produced by MiniGoParser#for_initialization.
    # for_initialization:  
    # ID assign_operator init_value_for_all 
    # |VAR ID (scalar_type|) ASSIGN init_value_for_all;
    def visitFor_initialization(self, ctx:MiniGoParser.For_initializationContext):
        if ctx.getChildCount() == 3:
            op = ctx.assign_operator().getText()
            lhs = Id(ctx.ID().getText())
            rhs = self.visit(ctx.init_value_for_all())
            if op == ":=":
                return Assign(lhs,rhs)
            elif op == "+=":
                return Assign(lhs,BinaryOp('+',lhs,rhs))
            elif op == "-=":
                return Assign(lhs,BinaryOp('-',lhs,rhs))
            elif op == "*=":
                return Assign(lhs,BinaryOp('*',lhs,rhs))
            elif op == "/=":
                return Assign(lhs,BinaryOp('/',lhs,rhs))
            elif op == "%=":
                return Assign(lhs,BinaryOp('%',lhs,rhs))
        else:
            vName = ctx.ID().getText()
            vType = None
            if ctx.scalar_type() and self.visit(ctx.scalar_type()):
                vType = self.visit(ctx.scalar_type())
            vInit = self.visit(ctx.init_value_for_all())
            return VarDecl(vName,vType,vInit)

    # Visit a parse tree produced by MiniGoParser#for_condition.
    # for_condition: expression_logic; 
    def visitFor_condition(self, ctx:MiniGoParser.For_conditionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#for_update.
    # for_update: ID assign_operator expression_compu;
    def visitFor_update(self, ctx:MiniGoParser.For_updateContext):
            op = ctx.assign_operator().getText()
            lhs = Id(ctx.ID().getText())
            rhs = self.visit(ctx.expression_compu())
            if op == ":=":
                return Assign(lhs,rhs)
            elif op == "+=":
                return Assign(lhs,BinaryOp('+',lhs,rhs))
            elif op == "-=":
                return Assign(lhs,BinaryOp('-',lhs,rhs))
            elif op == "*=":
                return Assign(lhs,BinaryOp('*',lhs,rhs))
            elif op == "/=":
                return Assign(lhs,BinaryOp('/',lhs,rhs))
            elif op == "%=":
                return Assign(lhs,BinaryOp('%',lhs,rhs))

    # Visit a parse tree produced by MiniGoParser#for_body.
    # for_body: LEFT_BRACE block_body RIGHT_BRACE;
    def visitFor_body(self, ctx:MiniGoParser.For_bodyContext):
        return self.visit(ctx.block_body())


    # Visit a parse tree produced by MiniGoParser#statement_if_else.
    # statement_if_else: IF LEFT_PAREN expression RIGHT_PAREN LEFT_BRACE block_body RIGHT_BRACE ELSE statement_if_else
    # | IF LEFT_PAREN expression RIGHT_PAREN LEFT_BRACE block_body RIGHT_BRACE ELSE LEFT_BRACE block_body RIGHT_BRACE
    # | IF LEFT_PAREN expression RIGHT_PAREN LEFT_BRACE block_body RIGHT_BRACE ;
    def visitStatement_if_else(self, ctx:MiniGoParser.Statement_if_elseContext):
        if ctx.getChildCount() == 7:
            expr = self.visit(ctx.expression())
            thenStmt = self.visit(ctx.getChild(5))
            return If(expr,Block(thenStmt),None)
        elif ctx.getChildCount() == 9:
            expr = self.visit(ctx.expression())
            thenStmt = self.visit(ctx.getChild(5))
            elseStmt = self.visit(ctx.statement_if_else())
            return If(expr,Block(thenStmt),elseStmt)
        else:
            expr = self.visit(ctx.expression())
            thenStmt = self.visit(ctx.getChild(5))
            elseStmt = self.visit(ctx.getChild(9))
            return If(expr,Block(thenStmt),Block(elseStmt))

    # Visit a parse tree produced by MiniGoParser#statement_return.
    # statement_return: RETURN init_value_for_all| RETURN;
    def visitStatement_return(self, ctx:MiniGoParser.Statement_returnContext):
        if ctx.getChildCount() == 1:
            return Return(None)
        return Return(self.visit(ctx.init_value_for_all()))

    # Visit a parse tree produced by MiniGoParser#type_array.
    # type_array: list_bracket_init var_type ;
    def visitType_array(self, ctx:MiniGoParser.Type_arrayContext):
        list_init = self.visit(ctx.list_bracket_init())
        vType = self.visit(ctx.var_type())
        return ArrayType(list_init,vType)

    # Visit a parse tree produced by MiniGoParser#literal_all.
    # literal_all: INT_LITERAL|STRING_LITERAL|FLOAT_LITERAL|BOOL_LITERAL |NIL_LITERAL | composite_literal;
    def visitLiteral_all(self, ctx:MiniGoParser.Literal_allContext):
        if ctx.INT_LITERAL():
            return IntLiteral(self.convert_to_int(ctx.INT_LITERAL().getText()))
        elif ctx.STRING_LITERAL():
            return StringLiteral(ctx.STRING_LITERAL().getText()) #.replace("\"","")) # 
        elif ctx.FLOAT_LITERAL():
            return FloatLiteral(ctx.FLOAT_LITERAL().getText())
        elif ctx.BOOL_LITERAL():
            return BooleanLiteral(ctx.BOOL_LITERAL().getText())
        elif ctx.NIL_LITERAL():
            return NilLiteral()
        else:
            return self.visitChildren(ctx)

    # Visit a parse tree produced by MiniGoParser#composite_literal.
    # composite_literal: struct_literal | array_literal;
    def visitComposite_literal(self, ctx:MiniGoParser.Composite_literalContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by MiniGoParser#array_literal.
    # array_literal: list_bracket_init var_type LEFT_BRACE array_literal_element_list RIGHT_BRACE ;
    def visitArray_literal(self, ctx:MiniGoParser.Array_literalContext):
        dimens = self.visit(ctx.list_bracket_init())
        eleType = self.visit(ctx.var_type())
        value = self.visit(ctx.array_literal_element_list())
        return ArrayLiteral(dimens,eleType,value)

    # Visit a parse tree produced by MiniGoParser#array_literal_element_list.
    # array_literal_element_list: array_literal_element array_literal_element_list_tail |;
    def visitArray_literal_element_list(self, ctx:MiniGoParser.Array_literal_element_listContext):
        list_value = []
        if ctx.getChildCount() == 2:
            list_value.append(self.visit(ctx.array_literal_element()))
            list_value.extend(self.visit(ctx.array_literal_element_list_tail()))
        return list_value


    # Visit a parse tree produced by MiniGoParser#array_literal_element_list_tail.
    # array_literal_element_list_tail:COMMA array_literal_element array_literal_element_list_tail |;
    def visitArray_literal_element_list_tail(self, ctx:MiniGoParser.Array_literal_element_list_tailContext):
        list_value = []
        if ctx.COMMA():
            list_value.append(self.visit(ctx.array_literal_element()))
            list_value.extend(self.visit(ctx.array_literal_element_list_tail()))
        return list_value
    
    # Visit a parse tree produced by MiniGoParser#array_literal_element.
    # array_literal_element: 
    # INT_LITERAL
    # |FLOAT_LITERAL
    # |STRING_LITERAL
    # |BOOL_LITERAL
    # |NIL_LITERAL
    # |ID
    # |struct_literal
    # |LEFT_BRACE array_literal_element_list RIGHT_BRACE;

    def visitArray_literal_element(self, ctx:MiniGoParser.Array_literal_elementContext):
        if ctx.INT_LITERAL():
            return IntLiteral(self.convert_to_int(ctx.INT_LITERAL().getText()))
        elif ctx.FLOAT_LITERAL():
            return FloatLiteral(ctx.FLOAT_LITERAL().getText())
        elif ctx.STRING_LITERAL():
            return StringLiteral(ctx.STRING_LITERAL().getText()) #.replace("\"",""))
        elif ctx.BOOL_LITERAL():
            return BooleanLiteral(ctx.BOOL_LITERAL().getText())
        elif ctx.NIL_LITERAL():
            return NilLiteral()
        elif ctx.ID():
            return Id(ctx.ID().getText())
        elif ctx.struct_literal():
            return self.visit(ctx.struct_literal())
        elif ctx.LEFT_BRACE():
            return self.visit(ctx.array_literal_element_list())
        # ArrayLiteral([],None,self.visit(ctx.array_literal_element_list()))

    # Visit a parse tree produced by MiniGoParser#scalar_type.
    # scalar_type:INT | FLOAT| STRING | BOOLEAN;
    def visitScalar_type(self, ctx:MiniGoParser.Scalar_typeContext):
        if ctx.INT():
            return IntType()
        elif ctx.FLOAT():
            return FloatType()
        elif ctx.STRING():
            return StringType()
        elif ctx.BOOLEAN(): 
            return BoolType()

    # Visit a parse tree produced by MiniGoParser#composite_type.
    # composite_type: ID | type_array;
    def visitComposite_type(self, ctx:MiniGoParser.Composite_typeContext):
        if ctx.ID():
            return Id(ctx.ID().getText())
        return self.visitChildren(ctx)

    # Visit a parse tree produced by MiniGoParser#var_type.
    # var_type: scalar_type | composite_type;
    def visitVar_type(self, ctx:MiniGoParser.Var_typeContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by MiniGoParser#var_type_and_none.
    # var_type_and_none: var_type | ;
    def visitVar_type_and_none(self, ctx:MiniGoParser.Var_type_and_noneContext):
        if ctx.var_type():
            return self.visit(ctx.var_type())
        else:
            return None

    # Visit a parse tree produced by MiniGoParser#init_value_for_all.
    # init_value_for_all: expression_compu|literal_all;
    def visitInit_value_for_all(self, ctx:MiniGoParser.Init_value_for_allContext):
        return self.visitChildren(ctx)

    def convert_to_int(self,int_str:str):
        return int_str
        if int_str.startswith("0x") or int_str.startswith("0X"):
            return int(int_str[2:],16)
        elif int_str.startswith("0b") or int_str.startswith("0B"):
            return int(int_str[2:],2)
        elif int_str.startswith("0o") or int_str.startswith("0O"):
            return int(int_str[2:],8)
        else:
            return int(int_str)