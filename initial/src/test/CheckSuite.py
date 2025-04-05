import unittest
from TestUtils import TestChecker
from AST import *

class CheckSuite(unittest.TestCase):
    def test_redeclared(self):
        input = """var a int; var b int; var a int; """
        expect = "Redeclared Variable: a\n"
        self.assertTrue(TestChecker.test(input,expect,400))

    def test_type_mismatch(self):
        input = """var a int = 1.2;"""
        expect = "Type Mismatch: VarDecl(a,IntType,FloatLiteral(1.2))\n"
        self.assertTrue(TestChecker.test(input,expect,401))

    def test_undeclared_identifier(self):
        input = Program([VarDecl("a",IntType(),Id("b"))])
        expect = "Undeclared Identifier: b\n"
        self.assertTrue(TestChecker.test(input,expect,402))

    def test_func(self):
        input = """func a(a,b int) int { var a int = a; }; """
        expect = ""
        self.assertTrue(TestChecker.test(input,expect,404))        



    def test_func2(self):
        input = """func a(b int) int { var a int = c; }; """
        expect = "Undeclared Identifier: c\n"
        self.assertTrue(TestChecker.test(input,expect,405))
    def test_func3(self):
        input = """func a(b int, c float) int { var a float = b; }; """
        expect = ""
        self.assertTrue(TestChecker.test(input,expect,406))
    def test_func4(self):
        input = """func a(b int, c float) int { var a int = c; }; """
        expect = "Type Mismatch: VarDecl(a,IntType,Id(c))\n"
        self.assertTrue(TestChecker.test(input,expect,407))
    def test_408(self):
        input = """func a(b int, c float) int { var a int = 1 + 2;}; """
        expect = ""
        self.assertTrue(TestChecker.test(input,expect,408))
    # def test_409(self):
    #     input = """func a(b int, c float) int { var a int = 1 + b*2 + 2.2;}; """
    #     expect = "Type Mismatch: VarDecl(a,IntType,BinaryOp(BinaryOp(IntLiteral(1),+,BinaryOp(Id(b),*,IntLiteral(2))),+,FloatLiteral(2.2)))\n"
    #     self.assertTrue(TestChecker.test(input,expect,409))
    # def test_410(self):
    #     input = """func a(b int, c float) int { var a float = 1 + 2.2+c;}; """
    #     expect = ""
    #     self.assertTrue(TestChecker.test(input,expect,410))
    # def test_411(self):
    #     input = """var getInt int;"""
    #     expect = "Redeclared Variable: getInt\n"
    #     self.assertTrue(TestChecker.test(input,expect,411))
    def test_412(self):
        input = """var a int = 3; var b int = a*3+4/4;"""
        expect = ""
        self.assertTrue(TestChecker.test(input,expect,412))
    # def test_413(self):
    #     input = """var a int = 3; var b int = a+3*1.0;"""
    #     expect = "Type Mismatch: VarDecl(b,IntType,BinaryOp(Id(a),+,BinaryOp(IntLiteral(3),*,FloatLiteral(1.0))))\n"
    #     self.assertTrue(TestChecker.test(input,expect,413))

#     def test_414(self):
#         input = """var a Car = 10; var b int = 10;"""
#         expect = "Undeclared Type: Car\n"
#         self.assertTrue(TestChecker.test(input,expect,414))
#     def test_415(self):
#         input = """ 
#                     func m (a int) { var a int; m(a);};"""
#         expect = ""
#         self.assertTrue(TestChecker.test(input,expect,415))
#     def test_416(self):
#         input = """func main (a int) { 
#             var a int = 3;
#             if (a==5+2-4) {
#                 return;
#             }
        
#         };"""
#         expect = ""
#         self.assertTrue(TestChecker.test(input,expect,416))
#     def test_417(self):
#         input = """func main (a int) { 
#             var a int = 3;
#             if (3+2) {
#                 return ;
#             }
        
#         };"""
#         expect = "Type Mismatch: If(BinaryOp(IntLiteral(3),+,IntLiteral(2)),Block([Return()]))\n"
#         self.assertTrue(TestChecker.test(input,expect,417))
#     def test_418(self):
#         input = """func main (a int) { 
#             var a int = 3;
#             if (a==3) {
#                 var b int;
#                 if (b==4){
#                     var c = a+b;
#                 }
#             }
        
#         };"""
#         expect = ""
#         self.assertTrue(TestChecker.test(input,expect,418))
#     def test_419(self):
#         input = """func main (a int) { 
#             var a int = 3;
#             if (a==3) {
#                 var b int;
#                 if (b==4){
#                     var c = a+b;
#                 }
#                 var d int= c+b;
#             }
        
#         };"""
#         expect = "Undeclared Identifier: c\n"
#         self.assertTrue(TestChecker.test(input,expect,419))
#     def test_420(self):
#         input = """func main (a int) { 
#             if (a==3) {
#                 var b int;
#                 if (b==4){
#                     var c = a+b;
#                 }
#                 var d float= b*a;
#             }
        
#         };"""
#         expect = ""
#         self.assertTrue(TestChecker.test(input,expect,420))
#     def test_421(self):
#         input = """func main (a int) { 
#             if (a==3) {
#                 var b int;
#                 if (b==4){
#                     var c = a+b;
                    
#                 }
#                 var d float= b*a;
#             } else if (a==4) {
#                 var b int = 3;
#             } else {
#                 var d = b+c;
#             }
        
#         };"""
#         expect = "Undeclared Identifier: b\n"
#         self.assertTrue(TestChecker.test(input,expect,421))
#     def test_422(self):
#         input = """func main (a int) { 
#             if (a==3) {
#                 var b int;
#                 if (b==4){
#                     var c = a+b;
                    
#                 }
#                 var d float= b*a;
#             } else if (b==4) {
#                 var b int = 3;
#             } else {
#                 var d = b+c;
#             }
        
#         };"""
#         expect = "Undeclared Identifier: b\n"
#         self.assertTrue(TestChecker.test(input,expect,422))
#     def test_423(self):
#         input = """
#                  type A interface {
#                      Add(x, y int) int;
#                      Subtract(a, b float, c int) float;
#                      Reset()
#                      test_boolean(a boolean) boolean
#                      SayHello(name string) string
#                  }
#                 """
#         expect = ""
#         self.assertTrue(TestChecker.test(input,expect,423))
#     def test_424(self):
#         input = """
#                  type A interface {
#                      Add(x, y int) int;
#                      Subtract(a, b float, c int) float;
#                      Add()
#                      test_boolean(a boolean) boolean
#                      SayHello(name string) string
#                  }
#                 """
#         expect = "Redeclared Prototype: Add\n"
#         self.assertTrue(TestChecker.test(input,expect,424))
#     def test_425(self):
#         input = """
#                  type A struct {
#                     a string
#                     b float
#                     c int
#                  }
#                 """
#         expect = ""
#         self.assertTrue(TestChecker.test(input,expect,425))         
  