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
        self.step = 0
    
    def check(self):
        return self.visit(self.ast,self.global_envi)
    
    def CheckTypeBasic(self, aType, bType):
        if type(aType) is ArrayType and type(bType) is ArrayType:
            if len(aType.dimens) != len(bType.dimens):
                return False
            if not self.CheckTypeBasic(aType.eleType, bType.eleType):
                return False
            for i in range(len(aType.dimens)):
                if aType.dimens[i] != bType.dimens[i]:
                    return False
            return True
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

            struct_method = bType.methods

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
        if type(aType) is ArrayType and type(bType) is ArrayType:
            if len(aType.dimens) != len(bType.dimens):
                return False
            if type(aType.eleType) is FloatType and type(bType.eleType) is IntType:
                pass
            elif not self.CheckTypeBasic(aType.eleType, bType.eleType):
                return False 
            for i in range(len(aType.dimens)):
                if aType.dimens[i] != bType.dimens[i]:
                    return False
            return True
        return self.CheckTypeBasic(aType, bType)
    
    def getType(self, tp, c):

        parType = tp
        if self.step == 0:
            return tp
        if isinstance(tp, tuple):
            parType = tp[0]
        # try:
        if type(parType) is Id:
            res = self.lookup(parType.name, c[-1], lambda x: x.name)
            if res is None:
                raise Undeclared(Type(), parType.name)
            return res.mtype
        if type(parType) is Symbol:
            parType = parType.mtype
            return parType
        if type(parType) is StructType or type(parType) is InterfaceType:
            return parType
        parType = self.visit(parType, c)
        if type(parType) is tuple:
            parType = parType[0]
        if isinstance(parType, tuple):
            parType = parType[0]

        # except Exception as e:
        #    if isinstance(e, Redeclared):
        #     return parType
           
        #    raise Undeclared(Type(), parType.name)
        return parType
    
    def addToLocal(self, ele, c):
        return [[ele] +c[0]] + c[1:]
    

    def updateGlobal(self, ele, c):
            
        res = self.lookup(ele.name, c[0], lambda x: x.name)
        if res is None:
            return self.addToLocal(ele,c)
        res.name = ele.name
        
        res.mtype = ele.mtype
        res.value = ele.value
        return c
    
    def checkArrayEletype(self, eleList, eleType,c ):
        if self.step == 0:
            return True
        if type(eleList) is list:
            if len(eleList) == 0:
                return True
            for i in eleList:
                if type(i) is not list and type(i) is not List:
                    type_, value = self.visit(i,c)
                    if not self.CheckTypeBasic(type_, eleType):
                        return False
                res = self.checkArrayEletype(i, eleType, c)
                if not res:
                    return False
        return True
    


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
        t = [[
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
        self.step = 0
        for i in ast.decl:
            if type(i) not in[MethodDecl]:
                t = self.visit(i,t)
        for i in ast.decl:
            if type(i) in [InterfaceType,StructType]:
                c = self.visit(i,c)
        for i in ast.decl:
            if type(i) not in[InterfaceType, StructType,VarDecl, ConstDecl]:
                c = self.visit(i,c)
        self.step = 1

        reduce(lambda acc, ele: self.visit(ele, acc), ast.decl, c)
        return None
    
    def visitVarDecl(self,ast: VarDecl, c):
        # var a int ( a = 0 )
        # var a People ()
        # var a[3] int
        # var a = 12 (infertype a  = int)
        # var a float = 12 ( force type int to float)
        # var a string = 12 (type mismatch)
        if self.step == 0 :
            res = self.lookup(ast.varName, c[0], lambda x: x.name)
            if res is not None:
                raise Redeclared(Variable(), ast.varName)
            return self.addToLocal(Symbol(ast.varName, None, None), c)

        res = self.lookup(ast.varName, c[0], lambda x: x.name)
        varType = None
        varInitType = None
        varInitValue = 0
        if res is not None: raise Redeclared(Variable(), ast.varName )
        if ast.varType :
            varType = self.getType(ast.varType, c)
            
        if ast.varInit :
            varInitType, varInitValue = self.visit(ast.varInit, c)

            if type(varInitType) is VoidType:
                raise TypeMismatch(ast.varInit)
            if varType is None: 
                varType = self.getType(varInitType,c )
                return [[Symbol(ast.varName, varType, varInitValue)] + c[0]] + c[1:]
            if not self.CheckTypeComplex(varType, varInitType, c):
                raise TypeMismatch(ast)
        return self.addToLocal(Symbol(ast.varName, varType, varInitValue), c)

    def visitConstDecl(self,ast: ConstDecl, c):
        if self.step == 0:
            res = self.lookup(ast.conName, c[0], lambda x: x.name)
            if res is not None:
                raise Redeclared(Constant(), ast.conName)
            return self.addToLocal(Symbol(ast.conName, None, None), c)
        
        res = self.lookup(ast.conName, c[0], lambda x: x.name)
        if res is not None: raise Redeclared(Constant(), ast.conName)
        constType, constValue = self.visit(ast.iniExpr, c)
        return [[Symbol(ast.conName, constType, constValue)] + c[0]] + c[1:]
       
    def visitFuncDecl(self,ast: FuncDecl, c):
        if self.step == 0:
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
        if self.step ==1:
            self.visit(ast.body, [paramBlock] + self.updateGlobal(Symbol(ast.name, MType(paramBlock, self.getType(ast.retType, c))),c))
        self.currentFunc = None
        return self.updateGlobal(Symbol(ast.name, MType(paramBlock, self.getType(ast.retType, c))), c)

    def visitMethodDecl(self,ast:MethodDecl, c):
        rec = [Symbol(ast.receiver, self.getType(ast.recType, c), None)]
        t = self.visit(ast.fun, [[]]+[rec] +c)
        struct = self.lookup(rec[0].mtype.name, c[-1], lambda x: x.name)
        methods = struct.mtype.methods
        field = struct.mtype.elements
        if self.step == 0:
            if self.lookup(ast.fun.name, methods, lambda x: x.name):
                raise Redeclared(Method(), ast.fun.name)
            if self.lookup(ast.fun.name, field, lambda x: x[0]):
                raise Redeclared(Method(), ast.fun.name)
        struct.mtype.methods = self.updateGlobal(Symbol(ast.fun.name, t[0][0].mtype,None), [struct.mtype.methods])[0]       
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
    
    def visitArrayType(self,ast: ArrayType, c):

        if self.step == 0:
            return ast
        dim = []
        for i in ast.dimens:
            if type(i) is int:
               dim.append(int(i))
            else:
               typ_, value = self.visit(i,c)
               if type(typ_) is not IntType:
                   return ast, None
               dim.append(int(value))
        eletype = self.getType(ast.eleType,c)
        return ArrayType(dim, eletype), None
                
    def visitStructType(self,ast: StructType, c):
        if self.step == 0:
            res = self.lookup(ast.name, c[-1], lambda x : x.name)
            if res is not None:
                raise Redeclared(Type(), ast.name)
        field = []


        for i in ast.elements:
            res = self.lookup(i[0], field, lambda x: x[0])
            if res is not None:
                raise Redeclared(Field(), i[0])
            fieldType = self.getType(i[1], c)

            field.append([i[0], fieldType])
        method = []
        if self.step == 1:
            method = self.lookup(ast.name, c[-1], lambda x : x.name).mtype.methods

        return self.updateGlobal(Symbol(ast.name, StructType(ast.name, field, method)), c)


    def visitInterfaceType(self,ast: InterfaceType, c):
        if self.step ==0:
            res = self.lookup(ast.name, c[-1], lambda x : x.name)
            if res is not None:
                raise Redeclared(Type(), ast.name)
        t = [[]] +c
        for i in ast.methods:
            t = self.visit(i, t)
        return self.updateGlobal(Symbol(ast.name, InterfaceType(ast.name, t[0])),c)

            
    
    def visitBlock(self,ast: Block, c):
        block =[[]]+c
        if self.ForBlock:
            block = [self.ForBlock] +c
        for i in ast.member:
            res = self.visit(i, block)
            if isinstance(res,list): 
               block = res
            elif type(i) is MethCall or type(i) is FuncCall:
                if type(res[0]) is not VoidType:
                    raise TypeMismatch(i)
        return c
 
    def visitAssign(self,ast: Assign, c):
        rhsType, rhsValue= self.visit(ast.rhs, c)
        if type(rhsType) is VoidType:
            raise TypeMismatch(ast)
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
        if ast.idx.name != '_':
            res = None
            for block in c:
                res = self.lookup(ast.idx.name, block, lambda x: x.name)
                if res is not None:
                    if type(res.mtype) is not IntType:
                        raise TypeMismatch(ast)
                    break
            if res is None:
                raise Undeclared(Identifier(), ast.idx.name)
        if ast.value.name != '_':

            res = None
            for block in c:
                res = self.lookup(ast.value.name, block, lambda x: x.name)
                if res is not None:
                    if not self.CheckTypeBasic(res.mtype, arrType.eleType):
                        raise TypeMismatch(ast)
                    break
            if res is None:
                raise Undeclared(Identifier(), ast.value.name)
            
            
            
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
        if type(leftType) is VoidType:
            raise TypeMismatch(ast.left)
        if type(rightType) is VoidType:
            raise TypeMismatch(ast.right)
        
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
                    if ast.op == '-':
                        return IntType(), leftValue - rightValue
                    elif ast.op == '*':
                        return IntType(), leftValue * rightValue
                    else:  # ast.op == '/'
                        return IntType(), leftValue // rightValue  # Integer division for int types
                return IntType(), None
            if type(leftType) in [IntType, FloatType] and type(rightType) in [IntType, FloatType]:
                if leftValue is not None and rightValue is not None:
                    if ast.op == '-':
                        return FloatType(), leftValue - rightValue
                    elif ast.op == '*':
                        return FloatType(), leftValue * rightValue
                    else:  # ast.op == '/'
                        return FloatType(), leftValue / rightValue  # Float division
                return FloatType(), None
            raise TypeMismatch(ast)
        if ast.op == '%':
            if type(leftType) is IntType and type(rightType) is IntType:
                if leftValue is not None and rightValue is not None:
                    return IntType(), leftValue % rightValue
                return IntType(), None
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
        if type(utype) is VoidType:
            raise TypeMismatch(ast.body)
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
                raise Undeclared(Function(),ast.funName)
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

    def visitMethCall(self,ast: MethCall, c):
        structType, structValue = self.visit(ast.receiver, c)
        if type(structType) is not StructType and type(structType) is not InterfaceType:
            raise TypeMismatch(ast)
        struct = self.lookup(structType.name, c[-1], lambda x: x.name)
        if struct is None:
            raise Undeclared(Type(), struct.name)
        if type(struct.mtype) is StructType or type(structType) is InterfaceType:
            method = self.lookup(ast.metName, struct.mtype.methods, lambda x: x.name)

            if method is None:
                raise Undeclared(Method(), ast.metName)
            if len(ast.args) != len(method.mtype.partype):
                raise TypeMismatch(ast)
            for i in range(len(ast.args)):
                method_param_type = self.getType(method.mtype.partype[i].mtype,c )
                argsType, argsValue = self.visit(ast.args[i],c)
                if not self.CheckTypeBasic(method_param_type, argsType):
                    raise TypeMismatch(ast)        
            return method.mtype.rettype, None

            
    
    def visitId(self,ast: Id, c):
        for block in c:
            res :Symbol = self.lookup(ast.name, block, lambda x: x.name)
            if res is not None:
                return res.mtype, res.value
        raise Undeclared(Identifier(), ast.name)
    
    def visitArrayCell(self,ast: ArrayCell, c):
        arrType, arrValue = self.visit(ast.arr, c)
        if type(arrType) is not ArrayType:
            raise TypeMismatch(ast)
        if len(ast.idx) > len(arrType.dimens):
            raise TypeMismatch(ast)
        for i in ast.idx:
            idxType, idxValue = self.visit(i, c)
            if type(idxType) is not IntType:
                raise TypeMismatch(ast)
        if len(arrType.dimens) > len(ast.idx) :
            return ArrayType(arrType.dimens[len(arrType.dimens) - len(ast.idx)  :], arrType.eleType), None
        return arrType.eleType, None
            
    def visitFieldAccess(self,ast: FieldAccess, c):
        structType, structValue = self.visit(ast.receiver, c)
        if type(structType) is not StructType:
            raise TypeMismatch(ast)
        struct = self.lookup(structType.name, c[-1], lambda x: x.name)
        if struct is None:
            raise Undeclared(Type(), struct.name)
        fields = struct.mtype.elements
        res = self.lookup(ast.field, fields,lambda x: x[0])
        if res is None:
            raise Undeclared(Field(),ast.field)
        return self.getType(res[1],c), None    
    
    def visitIntLiteral(self,ast: IntLiteral, c):
        return IntType(), int(ast.value)
    
    def visitFloatLiteral(self,ast: FloatLiteral, c):
        return FloatType(), float(ast.value)
    
    def visitBooleanLiteral(self,ast: BooleanLiteral, c):
        return BoolType(), bool(ast.value)
    
    def visitStringLiteral(self,ast: StringLiteral, c):
        return StringType(), ast.value

    def visitArrayLiteral(self,ast: ArrayLiteral, c):
        dimens = []
        for i in ast.dimens:
            type_, value = self.visit(i, c)
            if type(type_) is not IntType:
                raise TypeMismatch(ast)
            dimens.append(int(value))
        eleType = self.getType(ast.eleType,c)
        if not self.checkArrayEletype(ast.value, eleType, c):
            raise TypeMismatch(ast)
        return ArrayType(dimens, eleType), None
        
    def visitStructLiteral(self,ast: StructLiteral, c):
        struct = None
        for block in c:
            struct = self.lookup(ast.name, block, lambda x: x.name)
            if struct is not None and type(struct.mtype) is not StructType:
                raise TypeMismatch(ast)
        if struct is None:
            raise Undeclared(Type(), ast.name)
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
        return NilLiteral(), None
