"""
 * @author nhphung
"""
from AST import * 
from Visitor import *
from Utils import Utils
from StaticError import *
from functools import reduce


class MType:
    def __init__(self,partype,rettype):
        self.partype = partype
        self.rettype = rettype

    def __str__(self):
        return "MType([" + ",".join(str(x) for x in self.partype) + "]," + str(self.rettype) + ")"

class Symbol:
    def __init__(self,name,mtype,value = None):
        self.name = name
        self.mtype = mtype
        self.value = value

    def __str__(self):
        return "Symbol(" + str(self.name) + "," + str(self.mtype) + ("" if self.value is None else "," + str(self.value)) + ")"



class StaticChecker(BaseVisitor,Utils):
        
    
    def __init__(self,ast):
        self.ast = ast
        self.global_envi = [Symbol("getInt",MType([],IntType()),None),Symbol("putIntLn",MType([IntType()],VoidType()))]
        self.currentFunc = None
        self.ForBlock = None
        self.isCheck = False
    
    def check(self):
        return self.visit(self.ast,self.global_envi)
    
    def CheckTypeBasic(self, aType, bType):
        if type(aType) is ArrayType and type(bType) is ArrayType:
            raise ValueError('chua xu li array nua huhu')
        if type(aType) is StructType and type(bType) is StructType:
            return aType.name == bType.name
        if type(aType) is type(bType):
            return True
        return False
    
    def CheckTypeComplex(self,aType, bType, c):
        if type(aType) is FloatType and type(bType) is IntType:
            return True
        if type(aType) is InterfaceType and type(bType) is StructType:
            interface_method = aType.methods
            # for i in interface_method:
            #     print(i)
            struct_method = bType.methods
            # for i in struct_method:
            #     print(i)
            for i in interface_method:
                res = self.lookup(i.name, struct_method, lambda x: x.name)
                if res is None:
                    return False
                if len(i.mtype.partype) != len(res.mtype.partype):
                    return False
                if not self.CheckTypeBasic(i.mtype.rettype, res.mtype.rettype):
                    return False
                for z in range(len(i.mtype.partype)):
                    if not self.CheckTypeBasic(i.mtype.partype[z], res.mtype.partype[z].mtype):
                        return False
            return True
        return self.CheckTypeBasic(aType, bType)
    
    def getType(self, tp, c):
        parType = tp
        if isinstance(tp, tuple):
            parType = tp[0]
        try:
            parType = self.visit(parType, c)
            if type(parType) is Tuple:
                parType = parType[0]
            if isinstance(parType, tuple):
                parType = parType[0]
            # if type(parType) is Tuple:
            #     parType = parType[0]
            # if isinstance(parType, tuple):
            #     parType = parType[0]
        except Exception as e:
           if isinstance(e, Redeclared):
            return parType
           raise Undeclared(Type(), parType.name)
        return parType
    
    def addToLocal(self, ele, c):
        return [[ele] +c[0]] + c[1:]

    #symbol:
    #6 type : var, const, func, struct, interface, method
    #var: symbol name, type, value
    #const: symbol name, type , value
    #func: symbol name, mtype(partype: list symbol(name, type, value), retype: type)
    #method: symbol name, mtype(partype: list symbol(name, type, value), retype: type)
    #struct: symbol name, structtype, value
    #interface: symbol name, interfacetype, value

    def visitProgram(self,ast: Program, c):
        c = [[
            #them cac ham co san vao nhe
            Symbol('getInt', MType([], IntType()), None),
            Symbol('putInt', MType([Symbol('i', IntType(), None)], VoidType()), None),
            Symbol('putIntLn', MType([Symbol('i', IntType(), None)], VoidType()), None),
            Symbol('getFloat', MType([], FloatType()), None),
            Symbol('putFloat', MType([Symbol('f', FloatType(), None)], VoidType()), None),
            Symbol('putFloatLn', MType([Symbol('f', FloatType(), None)], VoidType()), None),
            Symbol('getBool', MType([], BoolType()), None),
            Symbol('putBool', MType([Symbol('b', BoolType(), None)], VoidType()), None),
            Symbol('putBoolLn', MType([Symbol('b', BoolType(), None)], VoidType()), None),
            Symbol('getString', MType([], StringType()), None),
            Symbol('putString', MType([Symbol('s', StringType(), None)], VoidType()), None),
            Symbol('putStringLn', MType([Symbol('s', StringType(), None)], VoidType()), None),
            Symbol('putLn', MType([], VoidType()), None),

        ]]
        reduce(lambda acc, ele: self.visit(ele, acc), ast.decl, c)
        return None
    
    def visitVarDecl(self,ast: VarDecl, c):
        # var a int ( a = 0 )
        # var a People ()
        # var a[3] int
        # var a = 12 (infertype a  = int)
        # var a float = 12 ( force type int to float)
        # var a string = 12 (type mismatch)

        res = self.lookup(ast.varName, c[0], lambda x: x.name)
        varType = None
        varInitType = None
        varInitValue = 0
        if res is not None: raise Redeclared(Variable(), ast.varName )
        if ast.varType :
            varType = self.getType(ast.varType, c)
            
        if ast.varInit :
            varInitType, varInitValue = self.visit(ast.varInit, c)
            if varType is None: 
                varType = self.visit(varInitType,c )
                return [[Symbol(ast.varName, varType, varInitValue)] + c[0]] + c[1:]
            if not self.CheckTypeComplex(varType, varInitType, c):
                raise TypeMismatch(ast)
        return [[Symbol(ast.varName, varType, varInitValue)] + c[0]] + c[1:]

    def visitConstDecl(self,ast: ConstDecl, c):
        res = self.lookup(ast.conName, c[0], lambda x: x.name)
        if res is not None: raise Redeclared(Constant(), ast.conName)
        constType, constValue = self.visit(ast.iniExpr, c)
        return [[Symbol(ast.conName, constType, constValue)] + c[0]] + c[1:]
       
    def visitFuncDecl(self,ast: FuncDecl, c):
        res = self.lookup(ast.name, c[0], lambda x: x.name)

        if res is not None: raise Redeclared(Function(), ast.name)
        # viet 1 ham lay gia tri cua ID
        paramBlock = []
        for i in ast.params :
            res = self.lookup(i.parName, paramBlock, lambda x: x.name)
            if res is not None:
                raise Redeclared(Parameter(), i.parName)
            paramBlock.append(Symbol(i.parName, self.getType(i.parType,c), None))
        self.currentFunc = Symbol(ast.name, MType(paramBlock, self.getType(ast.retType, c)))
        # chua xu ly reType error
        self.visit(ast.body, [paramBlock] + [[Symbol(ast.name, MType(paramBlock, self.getType(ast.retType, c)))] +c[0]] + c[1:])
        self.currentFunc = None
        return [[Symbol(ast.name, MType(paramBlock, self.getType(ast.retType, c)))] +c[0]] + c[1:]

    def visitMethodDecl(self,ast:MethodDecl, c):
        rec = [Symbol(ast.receiver, self.getType(ast.recType, c), None)]
        t = self.visit(ast.fun, [[]]+[rec] +c)
        struct = self.lookup(rec[0].mtype.name, c[-1], lambda x: x.name)
        methods = struct.mtype.methods
        field = struct.mtype.elements
        if self.lookup(ast.fun.name, methods, lambda x: x.name):
            raise Redeclared(Method(), ast.fun.name)
        if self.lookup(ast.fun.name, field, lambda x: x[0]):
            raise Redeclared(Method(), ast.fun.name)       
        methods.append(Symbol(ast.fun.name, t[0][0].mtype,None))  
        return c   
            
    def visitPrototype(self,ast: Prototype, c):
        res = self.lookup(ast.name, c[0], lambda x: x.name)
        if res is not None: raise Redeclared(Prototype(), ast.name)
        params = []
        for i in ast.params:
            res = self.visit(i,c)
            params.append(res)
        return [[Symbol(ast.name, MType(params,self.getType(ast.retType,c)), None)] + c[0]] + c[1:]


    
    
    def visitIntType(self,ast, c):
        return IntType()
    
    def visitFloatType(self,ast, c):
        return FloatType()
    
    def visitBoolType(self,ast, c):
        return BoolType()
    
    def visitStringType(self,ast, c):
        return StringType()
    
    def visitVoidType(self,ast, c):
        return VoidType()
    
    def visitArrayType(self,ast, c):
        raise ValueError('do nothing array')
    
    def visitStructType(self,ast: StructType, c):
        res = self.lookup(ast.name, c[-1], lambda x : x.name)
        if res is not None:
            raise Redeclared(Type(), ast.name)
        field = []
        for i in ast.elements:
            res = self.lookup(i[0], field, lambda x: x[0])
            if res is not None:
                raise Redeclared(Field(), i[0])
            fieldType = self.getType(i[1],c)
            field.append([i[0], fieldType])
        method = []
        return [[Symbol(ast.name, StructType(ast.name, field, method))] +c[0]] + c[1:]


    def visitInterfaceType(self,ast: InterfaceType, c):
        res = self.lookup(ast.name, c[-1], lambda x : x.name)
        if res is not None:
            raise Redeclared(Type(), ast.name)
        t = [[]] +c
        for i in ast.methods:
            t = self.visit(i, t)
        return self.addToLocal(Symbol(ast.name, InterfaceType(ast.name, t[0])),c)

            
    
    def visitBlock(self,ast: Block, c):
        block =[[]]
        if self.ForBlock:
            block = [self.ForBlock]

        reduce(lambda acc, ele: self.visit(ele, acc), ast.member, block + c)
        return c
 
    def visitAssign(self,ast: Assign, c):
        rhsType, rhsValue= self.visit(ast.rhs, c)
        try:
            lhsType, lhsValue = self.visit(ast.lhs,c)
        except:
            if type(ast.lhs) is Id:
               return [[Symbol(ast.lhs.name, rhsType,rhsValue)] + c[0]] + c[1:]
        if not self.CheckTypeComplex(lhsType, rhsType, c):
            raise TypeMismatch(ast)
        if type(ast.lhs) is Id:
            # xu li viec cap nhat gia tri
            pass
        return c
   
    def visitIf(self,ast: If, c):
        conditionType, conditionValue = self.visit(ast.expr, c)
        if type(conditionType) is not BoolType:
            raise TypeMismatch(ast)
        self.visit(ast.thenStmt, c)
        if ast.elseStmt:
            self.visit(ast.elseStmt, c)
        return c
    
    def visitForBasic(self,ast: ForBasic, c):
        conditionType, conditionValue = self.visit(ast.cond, c)
        if type(conditionType) is not BoolType:
            raise TypeMismatch(ast)
        self.visit(ast.loop, c)
        return c
 
    def visitForStep(self,ast: ForStep, c):
        init = self.visit(ast.init, [[]]+ c)
        temp = c 
        if init is not None:
            temp = init
        conditionType, conditionValue = self.visit(ast.cond, temp)
        #moi tham thoi con chua co xu li neu tao moi bien bang assign
        update = self.visit(ast.upda, temp)
        if type(conditionType) is not BoolType:
            raise TypeMismatch(ast)
        self.ForBlock = init[0]
        self.visit(ast.loop, c)

        return c

    def visitForEach(self,ast: ForEach, c):
        arrType, arrValue = self.visit(ast.arr, c)
        if type(arrType) is not ArrayType:
            raise TypeMismatch(ast)
        self.ForBlock = [Symbol(ast.idx.name, IntType(), None), Symbol(ast.value.name, self.getType(arrType.eleType, c), None)]
        self.visit(ast.loop, c)
        return c

    def visitContinue(self,ast, c):
        return c
    
    def visitBreak(self,ast, c):
        return c
    
    def visitReturn(self,ast: Return, c):
        if self.currentFunc is not None:
            funcRetype = self.currentFunc.mtype.rettype
            if type(funcRetype) is VoidType:
                if ast.expr:
                    raise TypeMismatch(ast)
                return c
            exprType, exprValue = self.visit(ast.expr,c )
            if not self.CheckTypeBasic(exprType, funcRetype):
                raise TypeMismatch(ast)
        return c

    def visitBinaryOp(self,ast: BinaryOp, c):
        leftType, leftValue = self.visit(ast.left, c)
        rightType, rightValue = self.visit(ast.right, c)
        if type(leftType) is VoidType or type(rightType) is VoidType:
            raise TypeMismatch(ast)
        if ast.op == '+':
            if type(leftType) is StringType and type(rightType) is StringType:
                return StringType(), None
            if type(leftType) is IntType and type(rightType) is IntType:
                # tam thoi de None roi tinh gia tri sau
                if leftValue is not None and rightValue is not None:
                   return IntType(), leftValue + rightValue
                return IntType(), None
            if type(leftType) in [IntType, FloatType] and type(rightType) in [IntType, FloatType]:
                if leftValue is not None and rightValue is not None:
                    return FloatType(), leftValue + rightValue
                return FloatType(), None
                    
                
            raise TypeMismatch(ast)
        if ast.op in ['-', '*', '/']:
            if type(leftType) is IntType and type(rightType) is IntType:
                if leftValue is not None and rightValue is not None:
                    return IntType(), leftValue - rightValue
                return IntType(), None
            if type(leftType) in [IntType, FloatType] and type(rightType) in [IntType, FloatType]:
                if leftValue is not None and rightValue is not None:
                    return FloatType(), leftValue - rightValue
                return FloatType(), None
            raise TypeMismatch(ast)
        if ast.op == '%':
            if type(leftType) is IntType and type(rightType) is IntType:
                return IntType(), leftValue % rightValue
            raise TypeMismatch(ast)
        if ast.op in ['==', '!=', '<=', '>=', '<', '>']:
            if type(leftType) is StringType and type(rightType) is StringType:
                return BoolType(), None
            if type(leftType) is IntType and type(rightType) is IntType:
                # tam thoi de None roi tinh gia tri sau
                return BoolType(), None
            if type(leftType) in [ FloatType] and type(rightType) in [FloatType]:
                return BoolType(), None
            raise TypeMismatch(ast)
        if ast.op in ['&&', '||'] :
            if type(leftType) is BoolType and type(rightType) is BoolType:
                return BoolType(), None
            raise TypeMismatch(ast)
    
    def visitUnaryOp(self,ast: UnaryOp, c):
        utype, uvalue = self.visit(ast.body, c)
        if ast.op == '!':
            if type(utype) is not BoolType:
                raise TypeMismatch(ast)
            return BoolType(), None
        if ast.op == '-':
            if type(utype) not in [IntType, FloatType]:
                raise TypeMismatch(ast)
            if uvalue is None:
                return utype, None
            return  utype, -uvalue
            
    def visitFuncCall(self,ast: FuncCall, c):
        func = None
        for scope in c:
            func = self.lookup(ast.funName, scope, lambda x: x.name)
            if func is not None and type(func.mtype) is not MType:
            # chua duoc confirm tren forum
                raise TypeMismatch(ast)
        if func is None:
            raise Undeclared(Function(), ast.funName)
        #khac so luong
        func_call_params = ast.args
        func_params = func.mtype.partype
        if len(func_call_params) != len(func_params):
            raise TypeMismatch(ast)
        for i in range(len(func_call_params)):
            func_call_params_i_type, func_call_value = self.visit(func_call_params[i],c )
            if not self.CheckTypeBasic(func_call_params_i_type, self.getType(func_params[i].mtype, c)):
                raise TypeMismatch(ast)
        return func.mtype.rettype, None

    def visitMethCall(self,ast, c):
        raise ValueError('chua lam dau e')
    
    def visitId(self,ast: Id, c):
        for block in c:
            res :Symbol = self.lookup(ast.name, block, lambda x: x.name)
            if res is not None:
                return res.mtype, res.value
        raise Undeclared(Identifier(), ast.name)
    
    def visitArrayCell(self,ast, c):
        raise ValueError('chua lam dau e')
    
    def visitFieldAccess(self,ast, c):
        raise ValueError('chua lam dau e')
    
    def visitIntLiteral(self,ast: IntLiteral, c):
        return IntType(), int(ast.value)
    
    def visitFloatLiteral(self,ast: FloatLiteral, c):
        return FloatType(), float(ast.value)
    
    def visitBooleanLiteral(self,ast: BooleanLiteral, c):
        return BoolType(), bool(ast.value)
    
    def visitStringLiteral(self,ast: StringLiteral, c):
        return StringType(), ast.value

    def visitArrayLiteral(self,ast, c):
        raise ValueError('chua lam dau e')

    def visitStructLiteral(self,ast: StructLiteral, c):
        struct = None
        for block in c:
            struct = self.lookup(ast.name, block, lambda x: x.name)
            if struct is not None and type(struct.mtype) is not StructType:
                raise TypeMismatch(ast)
        for i in ast.elements:
            structType, structValue = self.visit(i[1], c)
            res = self.lookup(i[0], struct.mtype.elements, lambda x: x[0])
            if res is None:
                raise Undeclared(Field(), i[0])
            ok = self.CheckTypeBasic(structType, self.getType(res[1], c))
            if not self.CheckTypeBasic(structType, self.getType(res[1], c)):
                raise TypeMismatch(ast)
        return (struct.mtype, None)
            
    def visitNilLiteral(self,ast, c):
        raise ValueError('chua lam dau e')
