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
        self.isMethod = False
        self.turn = 0
        self.isCheck = False
        self.inExpr = False
    
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
        return self.CheckTypeBasic(aType, bType)
    
    def getType(self, tp, c):
        parType = self.visit(tp,c)
        if type(parType) is Tuple:
            parType = parType[0]
        return parType
    
        

    # def visitProgram(self,ast, c):
    #     reduce(lambda acc,ele: [self.visit(ele,acc)] + acc , ast.decl,c)
    #     return c

    # def visitVarDecl(self, ast, c):
    #     res = self.lookup(ast.varName, c, lambda x: x.name)
    #     if not res is None:
    #         raise Redeclared(Variable(), ast.varName) 
    #     if ast.varInit:
    #         initType = self.visit(ast.varInit, c)
    #         if ast.varType is None:
    #             ast.varType = initType
    #         if not type(ast.varType) is type(initType):
    #             raise TypeMismatch(ast)
    #     return Symbol(ast.varName, ast.varType,None)
        

    # def visitFuncDecl(self,ast, c):
    #     res = self.lookup(ast.name, c, lambda x: x.name)
    #     if not res is None:
    #         raise Redeclared(Function(), ast.name)
    #     return Symbol(ast.name, MType([], ast.retType))

    # def visitIntLiteral(self,ast, c):
    #     return IntType()
    
    # def visitFloatLiteral(self,ast, c):
    #     return FloatType()
    
    # def visitId(self,ast,c):
    #     res = self.lookup(ast.name, c, lambda x: x.name)
    #     if res is None:
    #         raise Undeclared(Identifier(), ast.name)
    #     return res.mtype

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
            varType = self.visit(ast.varType, c)
            
        if ast.varInit :
            print(ast)
            varInitType, varInitValue = self.visit(ast.varInit, c)
            if varType is None: 
                varType = self.visit(varInitType)
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
        # chua xu ly reType error
        self.visit(ast.body, [paramBlock] + [[Symbol(ast.name, MType(paramBlock, self.getType(ast.retType, c)))] +c[0]] + c[1:])
        return [[Symbol(ast.name, MType(paramBlock, self.getType(ast.retType, c)))] +c[0]] + c[1:]

    def visitMethodDecl(self,ast, c):
        
        raise ValueError('chua lam dau e')

    def visitPrototype(self,ast: Prototype, c):
        res = self.lookup(ast.name, c[0], lambda x: x.name)
        if res is not None: raise Redeclared(Prototype(), ast.name )
        raise ValueError('chua lam dau e')
        return c
    
    
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
        return ArrayType()
    
    def visitStructType(self,ast, c):
        raise ValueError('do nothing struct')

        raise ValueError('chua lam dau e')

    def visitInterfaceType(self,ast, c):
        raise ValueError('do nothing interface')

        raise ValueError('chua lam dau e')
    
    def visitBlock(self,ast: Block, c):
        reduce(lambda acc, ele: self.visit(ele, acc), ast.member,[[]]+ c)
        return c
 
    def visitAssign(self,ast, c):
        raise ValueError('chua lam dau e')
   
    def visitIf(self,ast, c):
        raise ValueError('chua lam dau e')
    
    def visitForBasic(self,ast, c):
        raise ValueError('chua lam dau e')
 
    def visitForStep(self,ast, c):
        raise ValueError('chua lam dau e')

    def visitForEach(self,ast, c):
        raise ValueError('chua lam dau e')

    def visitContinue(self,ast, c):
        raise ValueError('chua lam dau e')
    
    def visitBreak(self,ast, c):
        raise ValueError('chua lam dau e')
    
    def visitReturn(self,ast, c):
        raise ValueError('chua lam dau e')

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
                return IntType(), leftValue + rightValue
            if type(leftType) in [IntType, FloatType] and type(rightType) in [IntType, FloatType]:
                return FloatType(), leftValue + rightValue
            raise TypeMismatch(ast)
        if ast.op in ['-', '*', '/']:
            if type(leftType) is IntType and type(rightType) is IntType:
                return IntType(), leftValue - rightValue
            if type(leftType) in [IntType, FloatType] and type(rightType) in [IntType, FloatType]:
                return FloatType(), leftValue - rightValue
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
                return BoolType, None
            raise TypeMismatch(ast)
    
    def visitUnaryOp(self,ast, c):
        raise ValueError('chua lam dau e')
    
    def visitFuncCall(self,ast, c):
        raise ValueError('chua lam dau e')

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

    def visitStructLiteral(self,ast, c):
        raise ValueError('chua lam dau e')

    def visitNilLiteral(self,ast, c):
        raise ValueError('chua lam dau e')
