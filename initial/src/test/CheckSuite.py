import unittest
from TestUtils import TestChecker
from AST import *

class CheckSuite(unittest.TestCase):
    def test_redeclared(self):
        input = """var a int; var b int; var a int = a; """
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
    def test_s(self):
        input = """var a int; const a = 12; """
        expect = "Redeclared Constant: a\n"
        self.assertTrue(TestChecker.test(input,expect,403))
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
    def test_409(self):
        input = """func a(b int, c float) int { var a int = 1 + b*2 + 2.2;}; """
        expect = "Type Mismatch: VarDecl(a,IntType,BinaryOp(BinaryOp(IntLiteral(1),+,BinaryOp(Id(b),*,IntLiteral(2))),+,FloatLiteral(2.2)))\n"
        self.assertTrue(TestChecker.test(input,expect,409))
    def test_410(self):
        input = """func a(b int, c float) int { var a float = 1 + 2.2+c;}; """
        expect = ""
        self.assertTrue(TestChecker.test(input,expect,410))

    def test_411(self):
        input = """var getInt int;"""
        expect = "Redeclared Variable: getInt\n"
        self.assertTrue(TestChecker.test(input,expect,411))
    def test_412(self):
        input = """var a int = 3; var b int = a*3+4/4;"""
        expect = ""
        self.assertTrue(TestChecker.test(input,expect,412))
    def test_413(self):
        input = """var a int = 3; var b int = a+3*1.0;"""
        expect = "Type Mismatch: VarDecl(b,IntType,BinaryOp(Id(a),+,BinaryOp(IntLiteral(3),*,FloatLiteral(1.0))))\n"
        self.assertTrue(TestChecker.test(input,expect,413))
    def test_414(self):
        input = """var a Car = 10; var b int = 10;"""
        expect = "Undeclared Type: Car\n"
        self.assertTrue(TestChecker.test(input,expect,414))
    def test_415(self):
        input = """ 
                    func m (a int) { var a int; m(a);};"""
        expect = ""
        self.assertTrue(TestChecker.test(input,expect,415))
    def test_416(self):
        input = """func main (a int) { 
            var a int = 3;
            if (a==5+2-4) {
                return;
            }
        
        };"""
        expect = ""
        self.assertTrue(TestChecker.test(input,expect,416))
    def test_417(self):
        input = """func main (a int) { 
            var a int = 3;
            if (3+2) {
                return ;
            }
        
        };"""
        expect = "Type Mismatch: If(BinaryOp(IntLiteral(3),+,IntLiteral(2)),Block([Return()]))\n"
        self.assertTrue(TestChecker.test(input,expect,417))
    def test_418(self):
        input = """func main (a int) { 
            var a int = 3;
            if (a==3) {
                var b int;
                if (b==4){
                    var c = a+b;
                }
            }
        
        };"""
        expect = ""
        self.assertTrue(TestChecker.test(input,expect,418))


    def test_419(self):
        input = """func main (a int) { 
            var a int = 3;
            if (a==3) {
                var b int;
                if (b==4){
                    var c = a+b;
                }
                var d int= c+b;
            }
        
        };"""
        expect = "Undeclared Identifier: c\n"
        self.assertTrue(TestChecker.test(input,expect,419))
    def test_420(self):
        input = """func main (a int) { 
            if (a==3) {
                var b int;
                if (b==4){
                    var c = a+b;
                }
                var d float= b*a;
            }
        
        };"""
        expect = ""
        self.assertTrue(TestChecker.test(input,expect,420))
    def test_421(self):
        input = """func main (a int) { 
            if (a==3) {
                var b int;
                if (b==4){
                    var c = a+b;
                    
                }
                var d float= b*a;
            } else if (a==4) {
                var b int = 3;
            } else {
                var d = b+c;
            }
        
        };"""
        expect = "Undeclared Identifier: b\n"
        self.assertTrue(TestChecker.test(input,expect,421))
    def test_422(self):
        input = """func main (a int) { 
            if (a==3) {
                var b int;
                if (b==4){
                    var c = a+b;
                    
                }
                var d float= b*a;
            } else if (b==4) {
                var b int = 3;
            } else {
                var d = b+c;
            }
        
        };"""
        expect = "Undeclared Identifier: b\n"
        self.assertTrue(TestChecker.test(input,expect,422))
    def test_423(self):
        input = """
                 type A interface {
                     Add(x, y int) int;
                     Subtract(a, b float, c int) float;
                     Reset()
                     test_boolean(a boolean) boolean
                     SayHello(name string) string
                 }
                """
        expect = ""
        self.assertTrue(TestChecker.test(input,expect,423))
    def test_424(self):
        input = """
                 type A interface {
                     Add(x, y int) int;
                     Subtract(a, b float, c int) float;
                     Add()
                     test_boolean(a boolean) boolean
                     SayHello(name string) string
                 }
                """
        expect = "Redeclared Prototype: Add\n"
        self.assertTrue(TestChecker.test(input,expect,424))
    def test_425(self):
        input = """
                 type A struct {
                    a string
                    b float
                    c int
                 }
                """
        expect = ""
        self.assertTrue(TestChecker.test(input,expect,425))  
    def test_426(self):
        input = """
                 type A struct {
                    a string
                    b float
                    c int
                    a int
                 }
                """
        expect = "Redeclared Field: a\n"
        self.assertTrue(TestChecker.test(input,expect,426))        
    def test_427(self):
        input = """
                 type A struct {
                    a string
                    b float
                    c int
                    d boolean
                 }
                 var a A;
                """
        expect = ""
        self.assertTrue(TestChecker.test(input,expect,427))

    def test_428(self):
        input = """
                 type A struct {
                    a string
                    b float
                    c int
                    d boolean
                 }
                 var a A = A {a:"string"};
                """
        expect = ""
        self.assertTrue(TestChecker.test(input,expect,428))
    def test_429(self):
        input = """
                 type A struct {
                    a string
                    b float
                    c int
                    d boolean
                 }
                 var a A = A {a:"string",z:"hello"};
                """
        expect = "Undeclared Field: z\n"
        self.assertTrue(TestChecker.test(input,expect,429))
    def test_430(self):
        input = """
                 type A struct {
                    a string
                    b float
                    c int
                    d boolean
                 }
                 var a A = A {a:"string",b:"hello"};
                """
        expect = """Type Mismatch: StructLiteral(A,[(a,StringLiteral("string")),(b,StringLiteral("hello"))])\n"""
        self.assertTrue(TestChecker.test(input,expect,430))
    def test_431(self):
        input = """
                type B struct {
                    a int
                 }
                 type A struct {
                    a string
                    b B
                    c int
                    d boolean
                 }

                 var a A = A {a:"string",b: B { a: 3 }};
                """
        expect = """"""
        self.assertTrue(TestChecker.test(input,expect,431))
    def test_432(self):
        input = """
                type B struct {
                    a int
                 }
                 type C struct {
                    a int
                 }
                 type A struct {
                    a string
                    b B
                    c int
                    d boolean
                 }

                 var a A = A {a:"string",b: C { a: 3 }};
                """
        expect = """Type Mismatch: StructLiteral(A,[(a,StringLiteral("string")),(b,StructLiteral(C,[(a,IntLiteral(3))]))])\n"""
        self.assertTrue(TestChecker.test(input,expect,432))
    def test_433(self):
        input = """
                type B struct {
                    a int
                 }
                 type C struct {
                    b B
                 }
                 type A struct {
                    a string
                    b B
                    c C
                    d boolean
                 }

                 var a A = A {a:"string",b: B { a: 3 },c: C { b: B { a: 3 }}};
                """
        expect = """"""
        self.assertTrue(TestChecker.test(input,expect,433))
    def test_434(self):
        input = """
                type B struct {
                    a int
                 }
                 type C struct {
                    b B
                 }
                 type A struct {
                    a string
                    b B
                    c C
                    d boolean
                 }

                 var a A = A {a:"string",b: B { a: 3 },c: C { b: C { a: 30 }}};
                """
        expect = """Undeclared Field: a\n"""
        self.assertTrue(TestChecker.test(input,expect,434))
    def test_435(self):
        input = """
                type B struct {
                    a int
                 }
                 type C struct {
                    b B
                 }
                 type A struct {
                    a string
                    b B
                    c C
                    d boolean
                 }

                 var a A = A {a:"string",b: B { a: 3 },c: C { b: B { a: 3 }}};
                 var b A = a;
                """
        expect = """"""
        self.assertTrue(TestChecker.test(input,expect,435))
    def test_436(self):
        input = """
                type B struct {
                    a int
                 }
                 type C struct {
                    b B
                 }
                 type A struct {
                    a string
                    b B
                    c C
                    d boolean
                 }
                 var z int;
                 var a A = A {a:"string",b: B { a: 3 },c: C { b: B { a: 3 }}};
                 var b B = B {a:z};
                 var c A = A {b: b}
                """
        expect = """"""
        self.assertTrue(TestChecker.test(input,expect,436))
    def test_437(self):
        input = """
                type B struct {
                    a int
                 }
                 type C struct {
                    b B
                 }
                 type A struct {
                    a string
                    b B
                    c C
                    d boolean
                 }
                 var z int;
                 var a A = A {a:"string",b: B { a: 3 },c: C { b: B { a: 3 }}};
                 var b B = B {a:z};
                 var c A = b
                """
        expect = """Type Mismatch: VarDecl(c,Id(A),Id(b))\n"""
        self.assertTrue(TestChecker.test(input,expect,437))





    def test_438(self):
        input = """
                type Vehicle interface {
                    GetSpeed() int
                    SetSpeed(speed int)
                }
                type Car struct {
                    speed int
                }
                func (c Car) GetSpeed() int {
                    return 3
                }
                func (c Car) SetSpeed(speed int) {
                    var a = 12;
                }
                var a Vehicle = Car { speed: 10};
                """
        expect = """"""
        self.assertTrue(TestChecker.test(input,expect,438))
    def test_439(self):
        input = """
                type Vehicle interface {
                    GetSpeed() int
                    SetSpeed(speed int)
                }
                type Car struct {
                    speed int
                }
                func (c Car) GetSpeed() int {
                    return 3
                }
                var a Vehicle = Car { speed: 10};
                """
        expect = """Type Mismatch: VarDecl(a,Id(Vehicle),StructLiteral(Car,[(speed,IntLiteral(10))]))\n"""
        self.assertTrue(TestChecker.test(input,expect,439))
    def test_440(self):
        input = """
                func Test() int {
                    var a int = 3;
                    return a;
                }
                var a int = Test;
                """
        expect = """Type Mismatch: VarDecl(a,IntType,Id(Test))\n"""
        self.assertTrue(TestChecker.test(input,expect,440))
    # def test_441(self):
    #     input = """
    #             func Test() int {
    #                 var a int = 3;
    #                 return a;
    #             }
    #             var a int = Test();
    #             """
    #     expect = """"""
    #     self.assertTrue(TestChecker.test(input,expect,441))
    # def test_442(self):
    #     input = """
    #             func Test() int {
    #                 var a int = 3;
    #                 if (a <= 5) {
    #                     var b int = 4;
    #                     if (b <= 5) {
    #                         return a;
    #                     } else {
    #                         return b;
    #                     }
    #                     return b;
    #                 }
    #                 return a;
    #             }
    #             """
    #     expect = """"""
    #     self.assertTrue(TestChecker.test(input,expect,442))
    def test_443(self):
        input = """
                func Test() int {
                    var a int = 3;
                    if (a <= 5) {
                        var b int = 4;
                        if (b <= 5) {
                            return a;
                        } else {
                            return b;
                        }
                        return b;
                    }
                    return a;
                }
                func foo(a int, b,c float) int {
                    var a int = 3;
                    if (a <= 5) {
                        var b int = 4;
                        if (b <= 5) {
                            return a;
                        } else if (b > 5) {
                            return b;
                        } else {
                            return a+b;
                        }
                        return b;
                    }
                    return a;
                }
                """
        expect = """"""
        self.assertTrue(TestChecker.test(input,expect,443))
    def test_444(self):
        input = """
                func Test() int {
                    var a int = 3;
                    if (a <= 5) {
                        var b int = 4;
                        if (b <= 5) {
                            return a;
                        } else {
                            return b;
                        }
                        return b;
                    }
                    return a;
                }
                func foo(a int, b,c float) int {
                    var a int = 3;
                    if (a <= 5) {
                        var b int = 4;
                        if (b <= 5) {
                            return a;
                        } else if (b > 5) {
                            return b+1.2;
                        } else {
                            return a+b;
                        }
                        return b;
                    }
                    return a+1.2;
                }
                """
        expect = """Type Mismatch: Return(BinaryOp(Id(b),+,FloatLiteral(1.2)))\n"""
        self.assertTrue(TestChecker.test(input,expect,444))
    def test_445(self):
        input = """
                type Vehicle interface {
                    GetSpeed() int
                    SetSpeed(speed int)
                }
                type Car struct {
                    speed int
                }
                func (c Car) GetSpeed() int {
                    return 3
                }
                func Test() Car {
                    var a int = 3;
                    if (a <= 5) {
                        var b Car = Car { speed: 4 };
                        const c = 15;
                        if (c+4 <= 5) {
                            return Car { speed: a };
                        } else {
                            return b;
                        }
                        return b;
                    }
                    return Car { speed: a };
                }
                """
        expect = """"""
        self.assertTrue(TestChecker.test(input,expect,445))
    def test_446(self):
        input = """
                type Vehicle interface {
                    GetSpeed() int
                    SetSpeed(speed int)
                }
                type Car struct {
                    speed int
                }
                func (c Car) GetSpeed() int {
                    return 3
                }
                func Test() float {
                    var a int = 3;
                    if (a <= 5) {
                        var b Car = Car { speed: 4 };
                        const c = 15;
                        if (c+4 <= 5) {
                            return 3;
                        } else {
                            var b = 4;
                            return b;
                        }
                        return 5;
                    }
                    return a;
                }
                """
        expect = """Type Mismatch: Return(IntLiteral(3))\n"""
        self.assertTrue(TestChecker.test(input,expect,446))
    def test_447(self):
        input = """
                type Vehicle interface {
                    GetSpeed() int
                    SetSpeed(speed int)
                }
                type Car struct {
                    speed int
                }
                func (c Car) GetSpeed() int {
                    return 3
                }
                func (c Car) SetSpeed(speed int) {
                    var a = 12;
                }
                func Test() Car {
                    var a int = 3;
                    if (a <= 5) {
                        var b Car = Car { speed: 4 };
                        const c = 15;
                        if (c+4 <= 5) {
                            return Car { speed: a };
                        } else {
                            return b;
                        }
                        return b;
                    }
                    return Car { speed: a };
                }
                """
        expect = """"""
        self.assertTrue(TestChecker.test(input,expect,447))
    def test_448(self):
        input = """
                type Vehicle interface {
                    GetSpeed() int
                    SetSpeed(speed int)
                }
                type Car struct {
                    speed int
                }
                func (c Car) GetSpeed() int {
                    return 3
                }
                func Test() Vehicle {
                    var a int = 3;
                    if (a <= 5) {
                        var b Car = Car { speed: 4 };
                        const c = 15;
                        if (c+4 <= 5) {
                            return Car { speed: a };
                        } else {
                            return b;
                        }
                        return b;
                    }
                    return Car { speed: a };
                }
                """
        expect = """Type Mismatch: Return(StructLiteral(Car,[(speed,Id(a))]))\n"""
        self.assertTrue(TestChecker.test(input,expect,448))
    def test_449(self):
        input = """
                type Vehicle interface {
                    GetSpeed() int
                    SetSpeed(speed int)
                }
                type Car struct {
                    speed int
                }
                func (c Car) GetSpeed() int {
                    return 3
                }
                func (c Car) SetSpeed(speed int) {
                    var a = 12;
                    return a;
                }
                """
        expect = """Type Mismatch: Return(Id(a))\n"""
        self.assertTrue(TestChecker.test(input,expect,449))
    def test_450(self):
        input = """
                type People interface {
                    GetName() string
                }
                type Student struct {
                    name string
                }
                func (s Student) GetName() string {
                    return "s.name"
                }
                type Vehicle interface {
                    GetSpeed() int
                    SetSpeed(speed int)
                    GetPeople() People
                }
                type Car struct {
                    speed int
                }
                func (c Car) GetSpeed() int {
                    return 3
                }
                func (c Car) SetSpeed(speed int) {
                    var a = 12;
                }
                func (c Car) GetPeople() People {
                    return Student { name: "s.name" };
                }
                """
        expect = """Type Mismatch: Return(StructLiteral(Student,[(name,StringLiteral("s.name"))]))\n"""
        self.assertTrue(TestChecker.test(input,expect,450))
    # def test_451(self):
    #     input = """
    #             func Test() int {
    #                 var a int = 3;
    #                 return a;
    #             }
    #             var foo = 12;
    #             var a int = foo();
    #             """
    #     expect = """Type Mismatch: FuncCall(foo,[])\n"""
    #     self.assertTrue(TestChecker.test(input,expect,451))
    # def test_452(self):
    #     input = """
    #             func Test() int {
    #                 var a int = 3;
    #                 return a;
    #             }
    #             var foo = 12;
    #             var a int = getABC();
    #             """
    #     expect = """Undeclared Function: getABC\n"""
    #     self.assertTrue(TestChecker.test(input,expect,452))
    # def test_453(self):
    #     input = """
    #             func Test() int {
    #                 var a int = 3;
    #                 return a;
    #             }
    #             var foo = 12;
    #             var a int = Test(2);
    #             """
    #     expect = """Type Mismatch: FuncCall(Test,[IntLiteral(2)])\n"""
    #     self.assertTrue(TestChecker.test(input,expect,453))
    # def test_454(self):
    #     input = """
    #             func Test(a float, b int) int {
    #                 var a int = 3;
    #                 return a;
    #             }
    #             var foo = 12;
    #             var a int = Test(1.2,2);
    #             """
    #     expect = """"""
    #     self.assertTrue(TestChecker.test(input,expect,454))
    # def test_455(self):
    #     input = """
    #             func Test(a float, b int) int {
    #                 var a int = 3;
    #                 return a;
    #             }
    #             var foo = 12;
    #             var a int = Test(1,2);
    #             """
    #     expect = """Type Mismatch: FuncCall(Test,[IntLiteral(1),IntLiteral(2)])\n"""
    #     self.assertTrue(TestChecker.test(input,expect,455))
    # def test_456(self):
    #     input = """
    #             func Test(a int, b int) int {
    #                 var a int = 3;
    #                 return a;
    #             }
    #             var foo = 12;
    #             var a int = Test(1,2)+12-3*6-Test(1,-2);
    #             """
    #     expect = """"""
    #     self.assertTrue(TestChecker.test(input,expect,456))
    # def test_457(self):
    #     input = """
    #             type Car struct {
    #                 speed int
    #             }
    #             func Test(a int, b int) int {
    #                 var a int = 3;
    #                 var c Car = Car { speed: a };
    #                 return a.speed;
    #             }
    #             """
    #     expect = """Type Mismatch: FieldAccess(Id(a),speed)\n"""
    #     self.assertTrue(TestChecker.test(input,expect,457))
    # def test_458(self):
    #     input = """
    #             type Car struct {
    #                 speed int
    #                 name string
    #             }
    #             func Test(a int, b int) int {
    #                 var a int = 3;
    #                 var c Car = Car { speed: a };
    #                 return c.speed;
    #             }
    #             """
    #     expect = """"""
    #     self.assertTrue(TestChecker.test(input,expect,458))
    # def test_459(self):
    #     input = """
    #             type Car struct {
    #                 speed int
    #                 name string
    #             }
    #             func Test(a int, b int) int {
    #                 var a int = 3;
    #                 var c Car = Car { speed: a };
    #                 return c.name;
    #             }
    #             """
    #     expect = """Type Mismatch: Return(FieldAccess(Id(c),name))\n"""
    #     self.assertTrue(TestChecker.test(input,expect,459))
    # def test_460(self):
    #     input = """
    #             type Car struct {
    #                 speed int
    #                 name string
    #             }
    #             func Test(a int, b int) int {
    #                 var a int = 3;
    #                 var c Car = Car { speed: a };
    #                 return c.height;
    #             }
    #             """
    #     expect = """Undeclared Field: height\n"""
    #     self.assertTrue(TestChecker.test(input,expect,460))
    # def test_461(self):
    #     input = """
    #             type People interface {
    #                 GetName() string
    #             }
    #             type Student struct {
    #                 name string
    #             }
    #             func (s Student) GetName() string {
    #                 return "s.name"
    #             }
    #             type Car struct {
    #                 speed int
    #                 name string
    #                 driver Student
    #             }
    #             func Test(a int, b int) string {
    #                 var a int = 3;
    #                 var c Car = Car { speed: a };
    #                 return c.driver.name;
    #             }
    #             """
    #     expect = """"""
    #     self.assertTrue(TestChecker.test(input,expect,461))





    # def test_462(self):
    #     input = """
    #             type People interface {
    #                 GetName() string
    #             }
    #             type Student struct {
    #                 name string
    #             }
    #             func (s Student) GetName() string {
    #                 return "s.name"
    #             }
    #             type Car struct {
    #                 speed int
    #                 name string
    #                 driver Student
    #             }
    #             func Test(a int, b int) string {
    #                 var a int = 3;
    #                 var c Car = Car { speed: a, driver: Student { name: "s.name" } };
    #                 return c.driver.name;
    #             }
    #             """
    #     expect = """"""
    #     self.assertTrue(TestChecker.test(input,expect,462))

#     def test_463(self):
#         input = """
#                 type People interface {
#                     GetName() string
#                 }
#                 type Student struct {
#                     name string
#                 }
#                 func (s Student) GetName() string {
#                     return "s.name"
#                 }
#                 type Car struct {
#                     speed int
#                     name string
#                     driver Student
#                 }
#                 type Abc struct {
#                     age int
#                 }
#                 func Test(a int, b int) string {
#                     var a int = 3;
#                     var c Car = Car { speed: a, driver: Student { name: "s.name" } };
#                     if (a == c.speed) {
#                         return c.driver.name;
#                     } else {
#                         var z = Abc { age: a };
#                         var i = z.age+a;
#                         return "ok";
#                     }
#                     return c.driver.name;
#                 }
#                 """
#         expect = """"""
#         self.assertTrue(TestChecker.test(input,expect,463))
#     def test_464(self):
#         input = """
#                 type People interface {
#                     GetName() string
#                 }
#                 type Student struct {
#                     name string
#                     age int
#                 }
#                 func (s Student) GetName() string {
#                     return "s.name"
#                 }
#                 type Car struct {
#                     speed int
#                     name string
#                     driver Student
#                 }
#                 type Abc struct {
#                     age int
#                 }
#                 func getDriver(c Car) Student {
#                     return c.driver
#                 }
#                 func main () {

#                     var c = Car{speed:100,name:"abc",driver:Student{ age:20 }}
#                     var d = getDriver(c)
#                     var z string = d.name+"OK";
#                     var t int = d.age*2+4;
#                     return;
#                 }
#                 """
#         expect = """"""
#         self.assertTrue(TestChecker.test(input,expect,464))
#     def test_465(self):
#         input = """
#                 type People interface {
#                     GetName() string
#                 }
#                 type Student struct {
#                     name string
#                     age int
#                 }
#                 func (s Student) GetName() string {
#                     return "s.name"
#                 }
#                 type Car struct {
#                     speed int
#                     name string
#                     driver Student
#                 }
#                 type Abc struct {
#                     age int
#                 }
#                 func getDriver(c Car) Student {
#                     return c.driver
#                 }
#                 func main () {

#                     var c = Car{speed:100,name:"abc",driver:Student{ age:20 }}
#                     var d = getDriver(c.driver)
#                     var z string = d.name+"OK";
#                     var t int = d.age*2+4;
#                     return;
#                 }
#                 """
#         expect = """Type Mismatch: FuncCall(getDriver,[FieldAccess(Id(c),driver)])\n"""
#         self.assertTrue(TestChecker.test(input,expect,465))
#     def test_466(self):
#         input = """
#                 type People interface {
#                     GetName() string
#                 }
#                 type Student struct {
#                     name string
#                     age int
#                 }
#                 func (s Student) GetName() string {
#                     return "s.name"
#                 }
#                 type Car struct {
#                     speed int
#                     name string
#                     driver Student
#                 }
#                 type Abc struct {
#                     age int
#                 }
#                 func getDriver(c People) Student {
#                     return Student { name: "s.name" };
#                 }
#                 func main () {

#                     var c = Car{speed:100,name:"abc",driver:Student{ age:20 }}
#                     var d = getDriver(c.driver)
#                     var z string = d.name+"OK";
#                     var t int = d.age*2+4;
#                     return;
#                 }
#                 """
#         expect = """Type Mismatch: FuncCall(getDriver,[FieldAccess(Id(c),driver)])\n"""
#         self.assertTrue(TestChecker.test(input,expect,466))
#     def test_467(self):
#         input = """
#                 type People interface {
#                     GetName() string
#                 }
#                 type Student struct {
#                     name string
#                     age int
#                 }
#                 func (s Student) GetName() string {
#                     return "s.name"
#                 }
#                 type Car struct {
#                     speed int
#                     name string
#                     driver Student
#                 }
#                 type Abc struct {
#                     age int
#                 }
#                 func (c Car) getDriver() Student {
#                     return Student { name: "s.name" };
#                 }
#                 func main () {

#                     var c = Car{speed:100,name:"abc",driver:Student{ age:20 }}
#                     c.getDriver()                    
#                     return;
#                 }
#                 """
#         expect = """Type Mismatch: MethodCall(Id(c),getDriver,[])\n"""
#         self.assertTrue(TestChecker.test(input,expect,467))
#     def test_468(self):
#         input = """
#                 type People interface {
#                     GetName() string
#                 }
#                 type Student struct {
#                     name string
#                     age int
#                 }
#                 func (s Student) GetName() string {
#                     return "s.name"
#                 }
#                 type Car struct {
#                     speed int
#                     name string
#                     driver Student
#                 }
#                 type Abc struct {
#                     age int
#                 }
#                 func (c Car) getDriver() Student {
#                     return Student { name: "s.name" };
#                 }
#                 func main () {

#                     var c = Car{speed:100,name:"abc",driver:Student{ age:20 }}
#                     var a int ;
#                     a.getDriver()                    
#                     return;
#                 }
#                 """
#         expect = """Type Mismatch: MethodCall(Id(a),getDriver,[])\n"""
#         self.assertTrue(TestChecker.test(input,expect,468))
#     def test_469(self):
#         input = """
#                 type People interface {
#                     GetName() string
#                 }
#                 type Student struct {
#                     name string
#                     age int
#                 }
#                 func (s Student) GetName() string {
#                     return s.name
#                 }
#                 func (s Student) getDriver(a int) Student {
#                     return Student { name: "s.name" };
#                 }
#                 type Car struct {
#                     speed int
#                     name string
#                     driver Student
#                 }
#                 type Abc struct {
#                     age int
#                 }
#                 func (c Car) getDriver() Student {
#                     return Student { name: "s.name" };
#                 }
#                 func main () {

#                     var c = Car{speed:100,name:"abc",driver:Student{ age:20 }}
#                     var d = Student { name: "s.name" };
#                     d.getDriver()                    
#                     return;
#                 }
#                 """
#         expect = """Type Mismatch: MethodCall(Id(d),getDriver,[])\n"""
#         self.assertTrue(TestChecker.test(input,expect,469))
#     def test_470(self):
#         input = """
#                 type People interface {
#                     GetName() string
#                 }
#                 type Student struct {
#                     name string
#                     age int
#                 }
#                 func (s Student) GetName() string {
#                     return s.name
#                 }
#                 func (s Student) getDriver(a int) Student {
#                     return Student { name: "s.name" };
#                 }
#                 type Car struct {
#                     speed int
#                     name string
#                     driver Student
#                 }
#                 type Abc struct {
#                     age int
#                 }
#                 func (c Car) getDriver() Student {
#                     return Student { name: "s.name" };
#                 }
#                 func main () {

#                     var c = Car{speed:100,name:"abc",driver:Student{ age:20 }}
#                     var d = Student { name: "s.name" };
#                     d.doSomething()                    
#                     return;
#                 }
#                 """
#         expect = """Undeclared Method: doSomething\n"""
#         self.assertTrue(TestChecker.test(input,expect,470))
#     def test_471(self):
#         input = """
#                 type People interface {
#                     GetName() string
#                 }
#                 type Student struct {
#                     name string
#                     age int
#                 }
#                 func (s Student) getName() string {
#                     return s.name
#                 }
#                 type Car struct {
#                     speed int
#                     name string
#                     driver Student
#                 }
#                 func (c Car) getDriver() Student {
#                     return Student { name: "s.name" };
#                 }
#                 func (c Car) getSpeed() int {
#                     return c.speed
#                 }
#                 func main () string{

#                     var c = Car{speed:100,name:"abc",driver:Student{ age:20 }}
#                     var d = Student { name: "s.name" };
#                     return d.getName()+c.getDriver().getName();
#                 }
#                 """
#         expect = """"""
#         self.assertTrue(TestChecker.test(input,expect,471))
#     def test_472(self):
#         input = """
#                 type People interface {
#                     GetName() string
#                 }
#                 type Student struct {
#                     name string
#                     age int
#                 }
#                 func (s Student) getName() string {
#                     return s.name
#                 }
#                 type Car struct {
#                     speed int
#                     name string
#                     driver Student
#                 }
#                 func (c Car) getDriver() Student {
#                     return Student { name: "s.name" };
#                 }
#                 func (c Car) getSpeed() int {
#                     return c.speed
#                 }
#                 func create(a string) Student {
#                     return Student { name: a };
#                 }
#                 func main () string{

#                     var c = Car{speed:100,name:"abc",driver:Student{ age:20 }}
#                     var d = Student { name: "s.name" };
#                     return d.getName()+create("abc").getName()+c.getDriver().getName();
#                     return create( d.getName()+create("abc").getName()+c.getDriver().getName()).getName();
#                 }
#                 """
#         expect = """"""
#         self.assertTrue(TestChecker.test(input,expect,472))
#     def test_473(self):
#         input = """
#                 type People interface {
#                     GetName() string
#                 }
#                 type Student struct {
#                     name string
#                     age int
#                 }
#                 func (s Student) getName() string {
#                     return s.name
#                 }
#                 type Car struct {
#                     speed int
#                     name string
#                     driver Student
#                 }
#                 func (c Car) getDriver() Student {
#                     return Student { name: "s.name" };
#                 }
#                 func (c Car) getSpeed(s Student) {
#                     return 
#                 }
#                 func create(a string) Student {
#                     return Student { name: a };
#                 }
#                 func main (){

#                     var c = Car{speed:100,name:"abc",driver:Student{ age:20 }}
#                     c.getSpeed(Student { name: "s.name" });
#                 }
#                 """
#         expect = """"""
#         self.assertTrue(TestChecker.test(input,expect,473))
#     def test_474(self):
#         input = """
#                 type People interface {
#                     GetName() string
#                 }
#                 type Student struct {
#                     name string
#                     age int
#                 }
#                 func (s Student) getName() string {
#                     return s.name
#                 }
#                 type Car struct {
#                     speed int
#                     name string
#                     driver Student
#                 }
#                 func (c Car) getDriver() Student {
#                     return Student { name: "s.name" };
#                 }
#                 func (c Car) getSpeed(s Student,a int,b float, c,d string) int {
#                     return c.speed
#                 }
#                 func create(a string) Student {
#                     return Student { name: a };
#                 }
#                 func main (){

#                     var c = Car{speed:100,name:"abc",driver:Student{ age:20 }}
#                     c.getSpeed(Student { name: "s.name" },1,1.2+2,"abc","abc");
#                 }
#                 """
#         expect = """Type Mismatch: FieldAccess(Id(c),speed)\n"""
#         self.assertTrue(TestChecker.test(input,expect,474))
#     def test_475(self):
#         input = """
#                 type People interface {
#                     GetName() string
#                 }
#                 type Student struct {
#                     name string
#                     age int
#                 }
#                 func (s Student) getName() string {
#                     return s.name
#                 }
#                 type Car struct {
#                     speed int
#                     name string
#                     driver Student
#                 }
#                 func (c Car) getDriver() Student {
#                     return Student { name: "s.name" };
#                 }
#                 func (c Car) getSpeed(s Student,a int,b float, z,d string) int {
#                     return c.speed
#                 }
#                 func create(a string) Student {
#                     return Student { name: a };
#                 }
#                 func main (){

#                     var c = Car{speed:100,name:"abc",driver:Student{ age:20 }}
#                     c.getSpeed(Student { name: "s.name" },1,1.2+2,"abc");
#                 }
#                 """
#         expect = """Type Mismatch: MethodCall(Id(c),getSpeed,[StructLiteral(Student,[(name,StringLiteral("s.name"))]),IntLiteral(1),BinaryOp(FloatLiteral(1.2),+,IntLiteral(2)),StringLiteral("abc")])\n"""
#         self.assertTrue(TestChecker.test(input,expect,475))
#     def test_476(self):
#         input = """
#                 var a  = getInt();
#                 var b int = a
#                 """
#         expect = """"""
#         self.assertTrue(TestChecker.test(input,expect,476))
#     def test_477(self):
#         input = """
#                 func main (){
#                 getInt();
#                 var a = putInt(1);
#                 putIntLn(2);
#                 getFloat();
#                 putFloat(3.0);
#                 putFloatLn(4.0);
#                 getBool();
#                 putBool(true);
#                 putBoolLn(false);
#                 putString("abc");
#                 putStringLn("def");
#                 putLn();
                
#                 }
#                 """
#         expect = """Type Mismatch: FuncCall(getInt,[])\n"""
#         self.assertTrue(TestChecker.test(input,expect,477))
#     def test_478(self):
#         input = """     
#                 var a = putInt(1);
#                 """
#         expect = """Type Mismatch: VarDecl(a,FuncCall(putInt,[IntLiteral(1)]))\n"""
#         self.assertTrue(TestChecker.test(input,expect,478))
#     def test_479(self):
#         input = """     
#                 func main () {
#                     putInt(1);
#                     putIntLn(2);
#                     putFloat(3.0);
#                     putFloatLn(4.0);
#                     putBool(true);
#                     putBoolLn(false);
#                     putString("abc");
#                     putStringLn("def");
#                     putLn();
#                 }
#                 """
#         expect = """"""
#         self.assertTrue(TestChecker.test(input,expect,479))
#     def test_480(self):
#         input = """     
#                 func main () {
#                     putInt(1);
#                     putIntLn(2);
#                     putFloat(3.0);
#                     putFloatLn(4.0);
#                     putBool(true);
#                     putBoolLn(false);
#                     putString("abc");
#                     putStringLn("def");
#                     putLn();
#                     getInt();
#                 }
#                 """
#         expect = """Type Mismatch: FuncCall(getInt,[])\n"""
#         self.assertTrue(TestChecker.test(input,expect,480))
#     def test_481(self):
#         input = """     
#                 type Student struct {
#                     name string
#                     age int
#                 }
#                 func (s Student) getName() string {
#                     return s.name
#                 }
#                 func main () {
#                     var s = Student { name: "s.name" };
#                     s.getName();
#                 }
#                 """
#         expect = """Type Mismatch: MethodCall(Id(s),getName,[])\n"""
#         self.assertTrue(TestChecker.test(input,expect,481))
#     def test_482(self):
#         input = """     
#                 type Student struct {
#                     name string
#                     age int
#                 }
#                 func (s Student) getName() {
#                     return 
#                 }
#                 func main () {
#                     var s = Student { name: "s.name" };
#                     s.getName();
#                 }
#                 """
#         expect = """"""
#         self.assertTrue(TestChecker.test(input,expect,482))
#     def test_483(self):
#         input = """     
#                 type Student struct {
#                     name string
#                     age [3] int
#                 }
#                 func (s Student) getName() {
#                     return 
#                 }
#                 func main () {
#                     var s = Student { name: "s.name" };
#                     s.getName();
#                 }
#                 """
#         expect = """"""
#         self.assertTrue(TestChecker.test(input,expect,483))
#     def test_484(self):
#         input = """     
#                 type Student struct {
#                     name string
#                     age [3] int
#                 }
#                 func (s Student) getName() {
#                     return 
#                 }
#                 func create() [3] float {
#                     var a [3] int;
#                     return a
#                 }
#                 func main () {
#                     var s = Student { name: "s.name" };
#                     s.getName();
#                 }
#                 """
#         expect = """Type Mismatch: Return(Id(a))\n"""
#         self.assertTrue(TestChecker.test(input,expect,484))
#     def test_485(self):
#         input = """     
#                 func create() [3] int {
#                     var a [3] int;
#                     return a
#                 }
#                 """
#         expect = """"""
#         self.assertTrue(TestChecker.test(input,expect,485))
#     def test_486(self):
#         input = """     
#                 type Student struct {
#                     name string
#                     age [3] int
#                 }
#                 func (s Student) getName() {
#                     return 
#                 }
#                 func create() [5] int {
#                     var a [3] int;
#                     return a
#                 }
#                 func main () {
#                     var s = Student { name: "s.name" };
#                     s.getName();
#                 }
#                 """
#         expect = """Type Mismatch: Return(Id(a))\n"""
#         self.assertTrue(TestChecker.test(input,expect,486))
#     def test_487(self):
#         input = """     
#                 type Student struct {
#                     name string
#                     age [3] int
#                 }
#                 func (s Student) getName() {
#                     return 
#                 }
#                 func create() [3][4][4][0] int {
#                     var a [3][4][4][0] int;
#                     return a
#                 }
#                 func main () {
#                     var s = Student { name: "s.name" };
#                     s.getName();
#                 }
#                 """
#         expect = """"""
#         self.assertTrue(TestChecker.test(input,expect,487))
#     def test_488(self):
#         input = """     
#                 func create() [3] int {
#                     const c = 3;
#                     var a [c] int;
#                     return a
#                 }
#                 """
#         expect = """"""
#         self.assertTrue(TestChecker.test(input,expect,488))
#     def test_489(self):
#         input = """     
#                 func create() [3] int {
#                     const c = 1+2;
#                     var a [c] int;
#                     return a
#                 }
#                 """
#         expect = """"""
#         self.assertTrue(TestChecker.test(input,expect,489))
#     def test_490(self):
#         input = """     
#                 func create() [4] int {
#                     const c = 1+2;
#                     var a [c] int;
#                     return a
#                 }
#                 """
#         expect = """Type Mismatch: Return(Id(a))\n"""
#         self.assertTrue(TestChecker.test(input,expect,490))
#     def test_491(self):
#         input = """     
#                 type Student struct {
#                     name string
#                     ages [3] int
#                 }
#                 func (s Student) age(a [3] int) [3] int {
#                     return s.ages                
#                 }
#                 func main () {
#                     var a = Student { name:"abc" }
#                     var z [3] int;
#                     var b = a.age(z);
                
#                 }
#                 """
#         expect = """"""
#         self.assertTrue(TestChecker.test(input,expect,491))
#     def test_492(self):
#         input = """     
#                 type Student struct {
#                     name string
#                     ages [3] int
#                 }
#                 func (s Student) age(a [4] int) [3] int {
#                     return s.ages               
#                 }
#                 func main () {
#                     var a = Student { name:"abc" }
#                     var z [3] int;
#                     var b = a.age(z);
                
#                 }
#                 """
#         expect = """Type Mismatch: MethodCall(Id(a),age,[Id(z)])\n"""
#         self.assertTrue(TestChecker.test(input,expect,492))
#     # def test_492(self):
#     #     input = """     
#     #             type Student struct {
#     #                 name string
#     #                 age [3] int
#     #             }
#     #             const c = 5;
#     #             func (s Student) age(a [c] int) [3] int {
#     #                 return s.age                
#     #             }
#     #             func main () {
#     #                 var a = Student { name:"abc" }
#     #                 var z [c] int;
#     #                 var b = a.age(z);
                
#     #             }
#     #             """
#     #     expect = """"""
#     #     self.assertTrue(TestChecker.test(input,expect,492))
#     def test_493(self):
#         input = """     
#                 type Student struct {
#                     name string
#                     age [3] int
#                 }
#                 const c = 5;
#                 func (s Student) age(a [c] int) [c] int {
#                     return s.age                
#                 }
#                 func main () {
#                     var a = Student { name:"abc" }
#                     var z [c] int;
#                     var b = a.age(z);
                
#                 }
#                 """
#         expect = """Redeclared Method: age\n"""
#         self.assertTrue(TestChecker.test(input,expect,493))
#     def test_494(self):
#         input = """     
#                 type Student struct {
#                     name string
#                     ages [5] int
#                 }
#                 const c = 5;
#                 func (s Student) age() [c] int {
#                     return s.ages                
#                 }
#                 var name = "Name"
#                 func main () {
#                     var a = Student { name:name }
#                     var z [c] int = a.age();
#                 }
#                 """
#         expect = """"""
#         self.assertTrue(TestChecker.test(input,expect,494))
#     def test_495(self):
#         input = """     
#                 const c = 5;

#                 type Student struct {
#                     name string
#                     age [c] int
#                 }
#                 func (s Student) ages() [c] int {
#                     return s.age                
#                 }
#                 func create () Student {
#                     return Student { name:"abc" }
#                 }
#                func main () {
#                     var a int ;
#                     var b float;
#                     var t string;
#                     var d boolean;
#                     var e Student ;
#                     var z [c] int;
                    
#                     a := 1;
#                     b +=2;
#                     t += "abc";
#                     d := !true;
#                     e := create();
#                     e := Student { name:"abc" };
#                     z := e.ages();

#                 }
#                 """
#         expect = """"""
#         self.assertTrue(TestChecker.test(input,expect,495))
#     def test_496(self):
#         input = """     
#                 type Student struct {
#                     name string
#                     ages [5] int
#                 }
#                 const c = 5;
#                 func (s Student) age() [c] int {
#                     return s.ages                
#                 }
#                 var name = "Name"
#                 func main () {
#                     var a = Student { name:name }
#                     var z [c] int = a.age();
#                 }
#                 """
#         expect = """"""
#         self.assertTrue(TestChecker.test(input,expect,496))
#     def test_497(self):
#         input = """
#                 var a = [3][4] boolean { {true,false,true},{false,true,false},{true,false,true}}
#                 var b = [3][4] float { {1.1,2.2,3.34},{4.4,5.5,6.6},{7.7,8.8,9.9}}
            
#                     """
#         expect = """"""
#         self.assertTrue(TestChecker.test(input,expect,497))
#     def test_498(self):
#         input = """
#                 var a [3] int = [3] int {1,2,3}
#                 """
#         expect = """"""
#         self.assertTrue(TestChecker.test(input,expect,498))
#     def test_499(self):
#         input = """
#                 var a [3] int = [3] int {1,2.2,3}
#                 """
#         expect = """Type Mismatch: ArrayLiteral([IntLiteral(3)],IntType,[IntLiteral(1),FloatLiteral(2.2),IntLiteral(3)])\n"""
#         self.assertTrue(TestChecker.test(input,expect,499))
#     def test_500(self):
#         input = """
#                 var c =  6/2 + 3 - 1*2;
#                 var a [4] int = [c] int {1,c,3}
#                 """
#         expect = """"""
#         self.assertTrue(TestChecker.test(input,expect,500))
#     def test_501(self):
#         input = """
#                 var c =  6/2 + 3 - 1*2;
#                 var a [5] int = [c] int {1,c,3}
#                 """
#         expect = """Type Mismatch: VarDecl(a,ArrayType(IntType,[IntLiteral(5)]),ArrayLiteral([Id(c)],IntType,[IntLiteral(1),Id(c),IntLiteral(3)]))\n"""
#         self.assertTrue(TestChecker.test(input,expect,501))
#     def test_502(self):
#         input = """
#                 var c =  6/2 + 3 - 1*2;
#                 var a [4] float = [c] int {1,c,3}
#                 """
#         expect = """"""
#         self.assertTrue(TestChecker.test(input,expect,502))
#     def test_503(self):
#         input = """
#                 var c =  6/2 + 3 - 1*2;
#                 var a [4][3] float = [c] [2] int { {1,c,3},{1,c,3}}
#                 """
#         expect = """Type Mismatch: VarDecl(a,ArrayType(FloatType,[IntLiteral(4),IntLiteral(3)]),ArrayLiteral([Id(c),IntLiteral(2)],IntType,[[IntLiteral(1),Id(c),IntLiteral(3)],[IntLiteral(1),Id(c),IntLiteral(3)]]))\n"""
#         self.assertTrue(TestChecker.test(input,expect,503))
#     def test_504(self):
#         input = """
#                 type Student struct {
#                     name string
#                     age [3] int
#                 }
#                 var c =  6/2 + 3 - 1*2;
#                 var a [4] Student = [c] Student { Student { name:"abc" }, Student { name:"abc" } }
#                 """
#         expect = """"""
#         self.assertTrue(TestChecker.test(input,expect,504))
#     def test_505(self):
#         input = """
#                 type Person interface {
#                     getName() string
#                     getAge() [3]int
#                 }
#                 type Student struct {
#                     name string
#                     age [3] int
#                 }
#                 func (s Student) getName() string {
#                     return s.name
#                 }
#                 func (s Student) getAge() [3]int {
#                     return s.age
#                 }
#                 var c =  6/2 + 3 - 1*2;
#                 var a [4] Person = [c] Student { Student { name:"abc" }, Student { name:"abc" } }
#                 """
#         expect = """Type Mismatch: VarDecl(a,ArrayType(Id(Person),[IntLiteral(4)]),ArrayLiteral([Id(c)],Id(Student),[StructLiteral(Student,[(name,StringLiteral("abc"))]),StructLiteral(Student,[(name,StringLiteral("abc"))])]))\n"""
#         self.assertTrue(TestChecker.test(input,expect,505))
#     def test_506(self):
#         input = """
#                 type Person interface {
#                     getName() string
#                     getAge() [3]int
#                 }
#                 type Car struct {
#                     name string
#                 }
#                 type Student struct {
#                     name string
#                     age [3] int
#                 }
#                 func (s Student) getName() string {
#                     return s.name
#                 }
#                 func (s Student) getAge() [3]int {
#                     return s.age
#                 }
#                 var c =  6/2 + 3 - 1*2;
#                 var a [4] Car = [c] Student { Student { name:"abc" }, Student { name:"abc" } }
#                 """
#         expect = """Type Mismatch: VarDecl(a,ArrayType(Id(Car),[IntLiteral(4)]),ArrayLiteral([Id(c)],Id(Student),[StructLiteral(Student,[(name,StringLiteral("abc"))]),StructLiteral(Student,[(name,StringLiteral("abc"))])]))\n"""
#         self.assertTrue(TestChecker.test(input,expect,506))
#     def test_507(self):
#         input = """
#                 type Student struct {
#                     name string
#                     age int
#                 }
#                 func (s Student) getName() string {
#                     return s.name
#                 }
#                 func (s Student) getAge() int {
#                     return s.age
#                 }        
#                 var b = Student { name:"abc", age:3 }
#                 var c =  6/2 + 3 - 1*2;
#                 var a [4] Student = [c] Student { b, Student { name:"abc" } }
#                 """ 
#         expect =  """"""
#         self.assertTrue(TestChecker.test(input,expect,507))
#     def test_508(self):
#         input = """
#                 type Student struct {
#                     name string
#                     age int
#                 }
#                 func (s Student) getName() string {
#                     return s.name
#                 }
#                 type Car struct {
#                     name string
#                     age int
#                 }
#                 func (s Student) getAge() int {
#                     return s.age
#                 }        
#                 var b = Car { name:"abc", age:3 }
#                 var c =  6/2 + 3 - 1*2;
#                 var a [4] Student = [c] Student { b, Student { name:"abc" } }
#                 """ 
#         expect =  """Type Mismatch: ArrayLiteral([Id(c)],Id(Student),[Id(b),StructLiteral(Student,[(name,StringLiteral("abc"))])])\n"""
#         self.assertTrue(TestChecker.test(input,expect,508))
#     def test_509(self):
#         input = """
#                 func main () {
#                     for (true) {
#                         return
#                     }
#                 }
#                 """ 
#         expect =  """"""
#         self.assertTrue(TestChecker.test(input,expect,509))
    def test_510(self):
        input = """
                func main () {
                    var a boolean
                    for (a) {
                        return
                    }
                }
                """ 
        expect =  """"""
        self.assertTrue(TestChecker.test(input,expect,510))
    def test_511(self):
        input = """
                func main () {
                    var a boolean
                    for (1+2*3.2<122.9) {
                        return
                    }
                }
                """ 
        expect =  """"""
        self.assertTrue(TestChecker.test(input,expect,511))
    def test_512(self):
        input = """
                func main () {
                    var a boolean
                    var b = 5;
                    for (1+2*3.2<122.9+b||a) {
                        return
                    }
                }
                """ 
        expect =  """"""
        self.assertTrue(TestChecker.test(input,expect,512))
    def test_513(self):
        input = """
                func main () {
                    var a boolean
                    var b = 5;
                    if (a){
                        for (1+2*3.2<122.9+b||a) {
                            return
                        }   
                    }

                }
                """ 
        expect =  """"""
        self.assertTrue(TestChecker.test(input,expect,513))
    def test_514(self):
        input = """
                func main () {
                    var a boolean
                    var b = 5;
                    var c = 5;
                    if (a){
                        var c float
                        for (1+2*3.2<122.9+b||a) {
                            var c boolean
                            for (c) {
                                var c string
                                continue
                            }
                            return
                        }   
                    }

                }
                """ 
        expect =  """"""
        self.assertTrue(TestChecker.test(input,expect,514))
# #     def test_515(self):
# #         input = """
# #                 func main () {
# #                     var a boolean
# #                     var b = 5;
# #                     var c = 5;
# #                     for i,_ := range [3] int { 1, 2 } {
# #                         for var i = 0; i < 3; i+=1 {
# #                             var c string
# #                             continue
# #                         }
# #                     }

# #                 }
# #                 """ 
# #         expect =  """"""
# #         self.assertTrue(TestChecker.test(input,expect,515))
#     def test_516(self):
#         input = """
#                 func main () {
#                     var a boolean
#                     var b = 5;
#                     var c = 5;
#                     for i, value := range a {
#                         return
#                     }

#                 }
#                 """ 
#         expect =  """Type Mismatch: ForEach(Id(i),Id(value),Id(a),Block([Return()]))\n"""
#         self.assertTrue(TestChecker.test(input,expect,516))

#     def test_517(self):
#         input = """
#                 func main () {
#                     var a boolean
#                     var b = 5;
#                     var c = 5;
#                     var d [3] string = [3] string {"a", "b", "c"}
#                     for i, value := range d {
#                         if (i<3) {
#                         return
#                         }
#                     }

#                 }
#                 """ 
#         expect =  """"""
#         self.assertTrue(TestChecker.test(input,expect,517))
#     def test_518(self):
#         input = """
#                 func main () {
#                     var a boolean
#                     var b = 5;
#                     var c = 5;
#                     var d [3] string = [3] string {"a", "b", "c"}
#                     for i, value := range d {
#                         if (i<3) {
#                         b += value
#                         return
#                         }
#                     }

#                 }
#                 """ 
#         expect =  """Type Mismatch: BinaryOp(Id(b),+,Id(value))\n"""
#         self.assertTrue(TestChecker.test(input,expect,518))

#     def test_519(self):
#         input = """
#                 func main () {
#                     var a boolean
#                     var b = 5;
#                     var c = 5;
#                     var d [3] int = [3] int { 1,2,3}
#                     for i, value := range d {
#                         if (i<3) {
#                         b %= value
#                         return
#                         }
#                     }

#                 }
#                 """ 
#         expect =  """"""
#         self.assertTrue(TestChecker.test(input,expect,519))

#     def test_520(self):
#         input = """
#                 func main () {
#                     var a boolean
#                     var b = 5;
#                     var c = 5;
#                     var d [3] int = [3] int { 1,2,3}
#                     for _, value := range d {
#                         var a = _;
#                     }

#                 }
#                 """ 
#         expect =  """"""
#         self.assertTrue(TestChecker.test(input,expect,520))
    
#     def test_521(self):
#         input = """
#                 func main () {
#                     var a boolean
#                     var b = 5;
#                     var c = 5;
#                     var d [3] string = [3] string {"a", "b", "c"}
#                     var i = 12;
#                     for i, value := range d {
#                         for i:= 0; c < 3; c+= 3 {
#                             return
#                         }
#                     }

#                 }
#                 """ 
#         expect =  """"""
#         self.assertTrue(TestChecker.test(input,expect,521))
    
#     def test_522(self):
#         input = """
#                 func main () {
#                     var a boolean
#                     var b = 5;
#                     var c = 5;
#                     var d [3] string = [3] string {"a", "b", "c"}
#                     var i = 12;
#                     for var i= 0; i < 3; i+= 3 {
#                             return
#                     }
#                 }
#                 """ 
#         expect =  """"""
#         self.assertTrue(TestChecker.test(input,expect,522))
#     def test_523(self):
#         input = """
#                 func main () {
#                     var a boolean
#                     var b = 5;
#                     var c = 5;
#                     var d [3] string = [3] string {"a", "b", "c"}
#                     var i = 12;
#                     var z = d[0]
#                 }
#                 """ 
#         expect =  """"""
#         self.assertTrue(TestChecker.test(input,expect,523))
#     def test_524(self):
#         input = """
#                 type Student struct {
#                     name string
#                     age [3] int
#                 }
#                 type Car struct {
#                     name string
#                     owner [5] Student
#                 }
#                 func main () {
#                     var a = Car { name:"OK"}
#                     var b int = a.owner[0].age[0]
#                 }
#                 """ 
#         expect =  """"""
#         self.assertTrue(TestChecker.test(input,expect,524))
#     def test_525(self):
#         input = """
#                 type Student struct {
#                     name string
#                     age [3] float
#                 }
#                 type Car struct {
#                     name string
#                     owner [5] Student
#                 }
#                 func main () {
#                     var a = Car { name:"OK"}
#                     var b int = a.owner[0].age[0]
#                 }
#                 """ 
#         expect =  """Type Mismatch: VarDecl(b,IntType,ArrayCell(FieldAccess(ArrayCell(FieldAccess(Id(a),owner),[IntLiteral(0)]),age),[IntLiteral(0)]))\n"""
#         self.assertTrue(TestChecker.test(input,expect,525))
#     def test_526(self):
#         input = """
#                 type Student struct {
#                     name string
#                     age [3] float
#                 }
#                 type Car struct {
#                     name string
#                     owner [5] Student
#                 }
#                 func main () {
#                     var a = Car { name:"OK"}
#                     var b [3][4] int;
#                     var c [4]  int = b[0]
#                 }
#                 """ 
#         expect =  """"""
#         self.assertTrue(TestChecker.test(input,expect,526))
#     def test_527(self):
#         input = """
#                 type Student struct {
#                     name string
#                     age [3] float
#                 }
#                 func main () {
#                     var a = Car { name:"OK"}
#                     var b [3][4] int;
#                     var c [4]  int = b[0]
#                 }
#                 type Car struct {
#                     name string
#                     owner [5] Student
#                 }
#                 """ 
#         expect =  """"""
#         self.assertTrue(TestChecker.test(input,expect,527))

#     def test_528(self):
#         input = """
#                 type Student struct {
#                     name string
#                     age [3] float
#                 }
#                 func main () {
#                     var a = Car { name:"OK"}
#                     var b [3][4] int;
#                     var c [4]  int = b[0]
#                 }

#                 func (c Car) getOwner() [5] Student {
#                     return c.owner
#                 }
#                 type Car struct {
#                     name string
#                     owner [5] Student
#                 }
#                 """ 
#         expect =  """"""
#         self.assertTrue(TestChecker.test(input,expect,528))
#     def test_529(self):
#         input = """
#                 type Student struct {
#                     name string
#                     age [3] float
#                 }
#                 func main () {
#                     var a = Student { name:"OK"}
#                     var b Person = a
#                 }

#                 func (c Car) getOwner() [5] Student {
#                     return c.owner
#                 }
#                 type Car struct {
#                     name string
#                     owner [5] Student
#                 }
#                 type Person interface {
#                     getName() string
#                     getAge() [3]float
#                 }
#                 func (p Student) getName() string {
#                     return p.name
#                 }
#                 func (p Student) getAge() [3]float {
#                     return p.age
#                 }
#                 """ 
#         expect =  """"""
#         self.assertTrue(TestChecker.test(input,expect,529))
#     def test_530(self):
#         input = """
#                 type Student struct {
#                     name string
#                     age [3] float
#                 }
#                 func main () {
#                     var a = Student { name:"OK"}
#                     var b Person = a
#                 }

#                 func (c Car) getOwner() [5] Student {
#                     return c.owner
#                 }
#                 type Car struct {
#                     name string
#                     owner [5] Student
#                 }
#                 type Person interface {
#                     getName() string
#                     getAge() [3]int
#                 }
#                 func (p Student) getName() string {
#                     return p.name
#                 }
#                 """ 
#         expect =  """Type Mismatch: VarDecl(b,Id(Person),Id(a))\n"""
#         self.assertTrue(TestChecker.test(input,expect,530))
#     def test_531(self):
#         input = """
#                 const z = 3+2-1-1;
#                 type Student struct {
#                     name string
#                     age [3] float
#                 }
#                 func main () {
#                     var a = Student { name:"OK"}
#                     var b Person = a
#                 }

#                 func (c Car) getOwner() [z] Student {
#                     return c.owner
#                 }
#                 type Car struct {
#                     name string
#                     owner [3] Student
#                 }
#                 type Person interface {
#                     getName() string
#                     getAge() [3]float
#                 }
#                 func (p Student) getName() string {
#                     return p.name
#                 }
#                func (p Student) getAge() [3]float {
#                     return p.age
#                 }
#                 const m = Car {}
                

#                 """ 
#         expect =  """"""
#         self.assertTrue(TestChecker.test(input,expect,531))
#     def test_532(self):
#         input = """
#                 type Item struct {
#                     items [3][4] string
#                 }
#                 type Student struct {
#                     name string
#                     age [3] float
#                     items [3] Item
#                 }
#                 func main () {
#                     var a = Student { name:"OK"}
#                     var t = 12;
#                     var z string = a.items[0].items[12+0][1+3]
#                     var d string = a.items[0].getName(Car { name:"OK"})
#                     var b Person = a
#                 }

#                 func (c Car) getOwner() [z] Student {
#                     return c.owner
#                 }
#                 type Car struct {
#                     name string
#                     owner [3] Student
#                 }
#                 type Person interface {
#                     getName() string
#                     getAge() [3]float
#                 }
#                 func (i Item) getName(c Car) string {
#                     return c.owner[0].items[0].items[12][z]
#                 }
#                 func (p Student) getName() string {
#                     return p.name
#                 }
#                func (p Student) getAge() [3]float {
#                     return p.age
#                 }
#                 const m = Car {}
#                 const z = 3+2-1-1;

#                 """ 
#         expect =  """Undeclared Identifier: z\n"""
#         self.assertTrue(TestChecker.test(input,expect,532))
#     def test_533(self):
#         input = """
#                 type Item struct {
#                     items [3][4] string
#                 }
#                 """ 
#         expect =  """"""
#         self.assertTrue(TestChecker.test(input,expect,533))
#     def test_534(self):
#         input = """func foo(a int,b int) int { 
#             return foo(foo(a,b),foo(a,b))
#         }
#         """
#         expect =  """"""
#         self.assertTrue(TestChecker.test(input,expect,534))
#     def test_535(self):
#         input = """
#         func foo(a int,b int) int { 
#             var c = Car { name: "abc"}
#             return foo(foo(a,b),foo(a,b))
#         }
#         func (c Car) getName() string {
#             return c.name
#         }
#         type Car struct {
#             name string
#             owner [5] Student
#         }
#         type Vehicle interface {
#             getName() string
#         }
#         func (c Car) getOwner() [5] Student {
#             return c.owner
#         }
#         type Person interface {
#             getName() string
#             getAge() [3]float
#         }
#         func (p Student) getName() string {
#             return p.name
#         }
#         type Student struct {
#             name string
#             age [3] float
#         }

#         func (p Student) getAge() [3]float {
#             return p.age
#         }
#         var a Car = Car { name:"abc" }
#         var b Person = a.getOwner()[0]
#         """
#         expect =  """"""
#         self.assertTrue(TestChecker.test(input,expect,535))
#     def test_536(self):
#         input = """
#         func foo(a boolean) boolean {
#             return a && "abc"=="anc" || "acd" > "s"
#         }
#         var a boolean =1 + 2 > 3 -3 *5 /6 % 7 || foo(1-2/2.3<4.3) || true && false
#         """
#         expect =  """"""
#         self.assertTrue(TestChecker.test(input,expect,536)) 
#     def test_537(self):
#         input = """
#         func foo(a boolean) boolean {
#             return a && "abc"=="anc" || "acd" > "s"
#         }
#         type Student struct {
#             stealLearn [3] boolean
#         }
#         var z = Student { stealLearn:[3] boolean {true,false,true}}
#         var a boolean =! (- 1 + 2 > 3 -3 *5 /6 % 7)|| !z.stealLearn[0] || foo(1-2/2.3<4.3) || true && false
#         """
#         expect =  """"""
#         self.assertTrue(TestChecker.test(input,expect,537))
#         # thêm test cho expr
    def test_538(self):
        input = """
            func main () {
            
            a:= 12; 
            var b = a+5;
            
            }
        """
        expect = """"""
        self.assertTrue(TestChecker.test(input, expect, 538))
    def test_539(self):
        input = """
            func main () {
            
            a+= 12; 
            var b = a+5;
            
            }
           

        """
        expect = """Undeclared Identifier: a\n"""
        self.assertTrue(TestChecker.test(input, expect, 539))
#     def test_540(self):
#         input = """
#             var z B = A { a:12}
#             type A struct {
#                 a int
#             }
#             type B interface {
#                 get() int
#             }
#             type C struct {
#                 a int
#             }
#             func (a A) get() int {
#                 return a.a
#             }

#             func main () {
            
#                 var a B;
#                 a:= A{ a:12};
#                 var z A;
#                 z:= C {a:12}
            
#             }


#         """
#         expect = """Type Mismatch: Assign(Id(z),StructLiteral(C,[(a,IntLiteral(12))]))\n"""
#         self.assertTrue(TestChecker.test(input, expect, 540))
#     def test_541(self):
#         input = """
#         func foo(a int,b int) int { 
#             var c = Car { name: "abc"}
#             return foo(foo(a,b),foo(a,b))
#         }
#         func (c Car) getName() string {
#             return c.name
#         }
#         type Car struct {
#             name string
#             owner [5] Student
#         }
#         type Vehicle interface {
#             getName() string
#         }
#         func (c Car) getOwner() [5] Student {
#             return c.owner
#         }
#         type Person interface {
#             getName() string
#             getAge() [3] float
#             getOwner() [5] Student
#         }
#         func (p Student) getName() string {
#             return p.name
#         }
#         type Student struct {
#             name string
#             age [3] float
#         }

#         func (p Student) getAge() [3]float {
#             return p.age
#         }
#         var a Car = Car { name:"abc" }
#         var b Person = a.getOwner()[0] // getOwner chua duoc implement boi student
#         func main() {
#             a.name := "abc"
#         }
#         """
#         expect =  """Type Mismatch: VarDecl(b,Id(Person),ArrayCell(MethodCall(Id(a),getOwner,[]),[IntLiteral(0)]))\n"""
#         self.assertTrue(TestChecker.test(input,expect,541))
#     def test_542(self):
#         input = """
#             type A struct {
#                 a int
#             }
#             type B interface {
#                 get() int
#             }
#             func (a A) get() int {
#                 return a.a
#             }

#             func main () string {
#             //cho nay chua co bat su kien thieu return
            
#                 var a B;
#                 a:= A{ a:12};
            
#             }


#         """
#         expect = """"""
#         self.assertTrue(TestChecker.test(input, expect, 542))
#     def test_543(self):
#         input = """
#             type A struct {
#                 a int
#             }
#             type B interface {
#                 get() int
#             }
#             func (a A) get() int {
#                 return a.a
#             }

#             func main () {
#                 for i := 0; i < 10; i+=1 {
#                     var a int = i;
#                     return
#                 }
                
#             }

#         """
#         expect = """"""
#         self.assertTrue(TestChecker.test(input, expect, 543))
#     def test_544(self):
#         input = """
#             func main() {
#                 a := [1][1][1] int { {{1}}}
#                 for i,v := range a {
#                     var i = i;
#                     for i:=1.2; i < 10; i+=1 {
#                         var i int = 3;
#                         var v = v;
#                         return
#                     }
#                 }
#                 return;
#             };
#             """
#         expect = """Redeclared Variable: i\n"""
#         self.assertTrue(TestChecker.test(input, expect, 544))
#     def test_545(self):
#         input = """
#             var a int = a;
#             var c = a;
#             var d = a;
#             """
#         expect = """Undeclared Identifier: a\n"""
#         self.assertTrue(TestChecker.test(input, expect, 545))
#     def test_546(self):
#         input = """
#             var a = Car { age: 3}
#             var b =  a.age;
            
#             const d = 12;
#             type B struct {
#                 z Car
#                 t  [d] Car

#             }
#             // dua len truoc const d = 12
#             const c = B {t: [12] Car { Car {age: 3} } }
#             type Car struct {
#                 age int
#             } 
#             func main (a int, b int) {
#                 return
            
#             }
#             func (c Car) foo (a int, b int) {
            
#                 return
#             }
            

#             """
        
#         """B{z Id(Car),t [b] Car },Car{age int},main (int,int) void ,foo (int,int) void

#             a Car {age: }
# type A {}
        
#         """
#         expect = """"""
#         self.assertTrue(TestChecker.test(input, expect, 546))
#     def test_547(self):
#         input = """

#             func main () {
# //                var a = 12;
#                 var b = a([3] int {1,2,3});
#             }
#             func a (b [3] int) int {
#                 return 1
#             }
#             """
#         expect = """"""
#         self.assertTrue(TestChecker.test(input, expect, 547))
#     def test_548(self):
#         input = """
#             type A struct {
#                 a int
#             }
#             type B interface {
#                 get() int
#             }
#             func (a A) get() int {
#                 return a.a
#             }
#             type C struct {
#                 a [3] A
#             }
#             func main () {
#                 var b = foo1([3] int {1,2,3});
#                 var c = foo2([3] A { A{},A{},A{}})
#                 var d = A {a:1}
#                 var e = foo3([3] A{d,d,A{}},2,C{a:[3] A{d,d,A{}}},d)
#             }
#             func foo1 (b [3] int) int {
#                 return 1
#             }
#             func foo2(b [3] A) C {
#                 return C{a:b}
#             }
#             func foo3(b [3] A,c int, z C, g A) int {
#                 return g.a*c+b[0].a+z.a[0].a
#             }
#             """
#         expect = """"""
#         self.assertTrue(TestChecker.test(input, expect, 548))
#     def test_549(self):
#         input = """
#             type A struct {
#                 a int
#             }
#             type B interface {
#                 get() int
#             }
#             func (a A) get(a int) int {
#                 return a
#             }
#             type C struct {
#                 a [3] A
#             }
#             func main () {
#                 var b = foo1([3] int {1,2,3});
#                 var c = foo2([3] A { A{},A{},A{}})
#                 var d = A {a:1}
#                 var e = foo3([3] A{d,d,A{}},2,C{a:[3] A{d,d,A{}}},d)
#             }
#             func foo1 (b [3] int) int {
#                 return 1
#             }
#             func foo2(b [3] A) C {
#                 return C{a:b}
#             }
#             func foo3(b [3] A,c int, z C, g A) int {
#                 return g.a*c+b[0].a+z.a[0].a
#             }
#             """
#         expect = """"""
#         self.assertTrue(TestChecker.test(input, expect, 549))
   

#     def test_550(self):
#         input = """
#                 type Item struct {
#                     items [3][4] string
#                 }
#                 type Student struct {
#                     name string
#                     age [3] float
#                     items [3] Item
#                 }
#                 const z = 3+2-1-1;

#                 func main () {
#                     var a Person = Student { name:"OK"}
#                     return
#                 }

#                 func (c Car) getOwner() [z] Student {
#                     return c.owner
#                 }
#                 type Car struct {
#                     name string
#                     owner [3] Student
#                 }
#                 type Person interface {
#                     getName(z int) Student
#                     getAge() [3]int
#                 }
#                 func (i Item) getName(c Car) string {
#                     return c.owner[0].items[0].getName(c)
#                 }
#                 func (p Student) getName(a int , b int) Car {
#                     return Car { }
#                 }
#                func (p Student) getAge() [3]float {
#                     return p.age
#                 }
#                 const m = Car { }

#                 """ 
#         expect =  """Type Mismatch: VarDecl(a,Id(Person),StructLiteral(Student,[(name,StringLiteral("OK"))]))\n"""
#         self.assertTrue(TestChecker.test(input,expect,550))     
#     def test_550(self):
#             input = """var size = 3 + 1.0 - 2.0*3;
#                 var a [size]int = [4]int {1,2,3,4 };"""
#             expect = """Type Mismatch: VarDecl(a,ArrayType(IntType,[Id(size)]),ArrayLiteral([IntLiteral(4)],IntType,[IntLiteral(1),IntLiteral(2),IntLiteral(3),IntLiteral(4)]))\n"""
#             self.assertTrue(TestChecker.test(input, expect, 550))
#     def test_551(self):
#         input = """var size = 3 + 1.0 - 2.0*3;
#             var a [3]int = [size]int { 1,2,3,4};"""
#         expect = """Type Mismatch: ArrayLiteral([Id(size)],IntType,[IntLiteral(1),IntLiteral(2),IntLiteral(3),IntLiteral(4)])\n"""
#         self.assertTrue(TestChecker.test(input, expect, 551))
#     def test_552(self):
#         input = """var size = "hello";
#             var a [3]int = [size]int { 1,2,3,4};"""
#         expect = """Type Mismatch: ArrayLiteral([Id(size)],IntType,[IntLiteral(1),IntLiteral(2),IntLiteral(3),IntLiteral(4)])\n"""
#         self.assertTrue(TestChecker.test(input, expect, 552))
#     def test_553(self):
#         input = """
#                 func main() { 
#                     var a = 3.0
#                     for i,v := range [a] int { 2,3,4} { 
#                         return
#                     }                
#                 }
            
#             """
#         expect = """Type Mismatch: ArrayLiteral([Id(a)],IntType,[IntLiteral(2),IntLiteral(3),IntLiteral(4)])\n"""
#         self.assertTrue(TestChecker.test(input, expect, 553))
#     def test_554(self):
#         input = """
#                 func main() { 
#                     var a float = 3
#                     a := 4
#                     a:=1.2             
#                 }
            
#             """
#         expect = """"""
#         self.assertTrue(TestChecker.test(input, expect, 554))
#     def test_555(self):
#         input = """
#                 type Item struct {
#                     items [3][4] string
#                 }
#                 type Student struct {
#                     name string
#                     age [3] float
#                     items [3] Item
#                 }
#                 type People interface {
#                     getName() string
#                 }
#                 func (s Student) getName() string {
#                     return s.name
#                 }
#                 func main() { 
#                     var a People = Student { name:"OK"}
#                     var b string = a.getName()
#                 }
            
#             """
#         expect = """"""
#         self.assertTrue(TestChecker.test(input, expect, 555))
#     def test_556(self):
#         input = """
#                 type Item struct {
#                     items [3][4] string
#                 }
#                 type Student struct {
#                     name string
#                     age [3] float
#                     items [3] Item
#                 }
#                 type People interface {
#                     getName() string
#                 }
#                 func (s Student) getName() string {
#                     return s.name
#                 }
#                 func main() { 
#                     var a People
#                     var b string = a.getName()
#                     var z = 3.2
#                     var c [z] int
#                 }
            
#             """
#         expect = """Type Mismatch: VarDecl(c,ArrayType(IntType,[Id(z)]))\n"""
#         self.assertTrue(TestChecker.test(input, expect, 556))
#     def test_557(self):
#         input = """
#                 type Item struct {
#                     items [3][4] string
#                 }
#                 type Student struct {
#                     name string
#                     age [3] float
#                     items [3] Item
#                 }
#                 type People interface {
#                     getName() string
#                 }
#                 type ABC struct {
#                     name string
#                     age [3] float
#                 }
#                 func (s Student) getName() string {
#                     return s.name
#                 }
#                 func (s ABC) getName() string {
#                     return s.name
#                 }
#                 func main() { 
#                     var a [3] People = [3] Student { Student { name:"OK"}, Student { name:"OK"}, Student { name:"OK"}}
#          //           a := [3] ABC { ABC { name:"OK"}, ABC { name:"OK"}, ABC { name:"OK"}}
#            //         b:= [3] ABC { ABC { name:"OK"}, ABC { name:"OK"}, ABC { name:"OK"}}
#                 }
            
#             """
#         expect = """Type Mismatch: VarDecl(a,ArrayType(Id(People),[IntLiteral(3)]),ArrayLiteral([IntLiteral(3)],Id(Student),[StructLiteral(Student,[(name,StringLiteral("OK"))]),StructLiteral(Student,[(name,StringLiteral("OK"))]),StructLiteral(Student,[(name,StringLiteral("OK"))])]))\n"""
#         self.assertTrue(TestChecker.test(input, expect, 557))
#     def test_558(self):
#         input = """
#                 type Item struct {
#                     items [3][4] string
#                 }
#                 const z = 3;
#                 type Student struct {
#                     name string
#                     age [z] float
#                     items [3] Item
#                 }
#                 var a People = Student { name:"OK", age:[3] float {3.0,3.0,3.0}}
#                 type People interface {
#                     getName() string
#                 }
#                 type ABC struct {
#                     name string
#                     age [3] float
#                 }
#                 func (s Student) getName() string {
#                     return s.name
#                 }
#                 func (s ABC) getName( s int) string {
#                     var s = "abc";
#                     return s
#                 }
#                 func main() { 
#                    return
#                 }
            
#             """ 
#         expect = """"""
#         self.assertTrue(TestChecker.test(input, expect, 558))
#     def test_559(self):
#         input = """
#             type A struct  {
#                 a int
#             }
#             var a Z = A{a : 1}
#             type B struct{
#                 a int
#             }
#             func main(){
#                 var a = A{a : 1}
#                 var b = B{a : 2}
#                 a.get();
#                 return
#             }
#             func (a A) get() int {
#                 return a.a
#             }
#             type Z interface {
#                 get() int
#             }
#         """
#         expect = """Type Mismatch: MethodCall(Id(a),get,[])\n"""
#         self.assertTrue(TestChecker.test(input, expect, 559))
#     def test_560(self):
#         input = """
#             type a struct {
#                 a int
#             }
#             func a () {
#                 return
#             }
#         """

#         # """
#         # lần 1 -> duyệt hết nhưng k làm gì hết -> chỉ check tên
#         # lần 2 -> duyệt struct và interface
#         # lần 3 -> duyệt hết mấy cái hàm và method để lấy kiểu
#         # lần 4 -> duyệt hết
#         # """
#         expect = """Redeclared Function: a\n"""
#         self.assertTrue(TestChecker.test(input, expect, 560))
#     def test_561(self):
#         input = """
#         func main(a int, a int ) {
#             return 
#         }
#         """
#         expect = """Redeclared Parameter: a\n"""
#         self.assertTrue(TestChecker.test(input, expect, 561))
#     def test_562(self):
#         input = """
#         type A struct {
#             a int
#         }
#         type A interface {
#             a ()
#         }
#         func (a A) main(a int) {
#             return
#         }
#         func main(a int ) {
#             return 
#         }
#         """
#         expect = """Redeclared Type: A\n"""
#         self.assertTrue(TestChecker.test(input, expect, 562))
#     def test_563(self):
#         input = """
        
#         type A interface {
#             a ()
#         }
#         func (a A) main(a int) {
#             return
#         }
#         type A struct {
#             a int
#         }
#         func main(a int ) {
#             return 
#         }
#         """
#         expect = """Redeclared Type: A\n"""
#         self.assertTrue(TestChecker.test(input, expect, 563))
#     def test_564(self):
#         input = """
        
#         func main(a int ) {
#             return main(1);
#         }
#         """
#         expect = """Type Mismatch: Return(FuncCall(main,[IntLiteral(1)]))\n"""
#         self.assertTrue(TestChecker.test(input, expect, 564))
#     def test_565(self):
#         input = """
#         func main(a int ) {
#             return main(1);
#         }
#         """
#         expect = """Type Mismatch: Return(FuncCall(main,[IntLiteral(1)]))\n"""
#         self.assertTrue(TestChecker.test(input, expect, 565))
#     def test_567(self):
#         input = """
#         func foo() {
#             return
#         }
#         func main(a int ) int {
#             return foo();
#         }
#         """
#         expect = """Type Mismatch: Return(FuncCall(foo,[]))\n"""
#         self.assertTrue(TestChecker.test(input, expect, 567))
#     def test_568(self):
#         input = """
#         type A struct {
#             a int
#         }
#         func foo() {
#             return
#         }
#         func main(a int ) int {
#             var a A = A{ a: 1, a: 1, a: 1}
#             return 1
#         }
#         """
#         expect = """"""
#         self.assertTrue(TestChecker.test(input, expect, 568))
#     def test_569(self):
#         input = """
        
#         func (a A) main(a int) {
#             return
#         }
#         type A struct {
#             a int
#         }
#         func main(a int ) {
#             return 
#         }
#         """
#         expect = """"""
#         self.assertTrue(TestChecker.test(input, expect, 569))
#     def test_570(self):
#         input = """
#         type A struct {
#             a int
#         }
#         func (z A) a(b int ) {
#         return
#         }
#         """
#         expect = """Redeclared Method: a\n"""
#         self.assertTrue(TestChecker.test(input, expect, 570))
#     def test_571(self):
#         input = """
#                 var a int; 
#                 const b = a +10+ 3 -2 *4
#                 var c [5]float = [b]int{1,2,3}
#                 """ 
#         expect =  """"""
#         self.assertTrue(TestChecker.test(input,expect,571))
    
#     def test_572(self):
#         input = """
#                 var a string;
#                 var b float;
#                 const c = a;
#                 """ 
#         expect =  """"""
#         self.assertTrue(TestChecker.test(input,expect,572))
#     def test_573(self):
#         input = Program([StructType("s",[],[]),VarDecl("a",StructType("s",[],[]),None)])
#         expect = ""
#         self.assertTrue(TestChecker.test(input,expect,573))
#     def test_574(self):
#         input = """
#         type A interface {
#             a()
#         }

#         var a A ;
#         var b A;
#         func main() {
#         b:=a;
#         }

# """
#         expect = ""
#         self.assertTrue(TestChecker.test(input,expect,574))
    # def test_575(self):
    #     input = """
    #     func main() {
    #     for var i= 0; i < 3; i+= 3 {
    #         var i int;
    #     }
        
    #     }

    #     """
    #     expect = "Redeclared Variable: i\n"
    #     self.assertTrue(TestChecker.test(input,expect,575))
#     def test_576(self):
#         input = """
#         func a(a int) int{
#             putInt(a(1));
#         }
#         """
#         expect = "Type Mismatch: FuncCall(a,[IntLiteral(1)])\n"
#         self.assertTrue(TestChecker.test(input,expect,576))
#     def test_577(self):
#         input = """
#         func main() {
#         for var i= 0; i < 3; i+= 3 {
#             for i,v := range [3] int {1,2,3} {
#                 for var i= 0; i < 3; i+= 3 {
#                     continue;
#                 }
#             }
#         }
#         }

#         """
#         expect = ""
#         self.assertTrue(TestChecker.test(input,expect,577))
#     def test_578(self):
#         input = """
#         func main() A{
#             var A int;
#             var a A;
#             return a;
        
#         } 
#         type A struct {
#             a int
#         }
#         """
#         expect = ""
#         self.assertTrue(TestChecker.test(input,expect,578))
#     def test_579(self):
#         input = Program([FuncDecl("foo", [], VoidType(), Block([])),
#                          StructType("foo", [("name", StringType())], [])])
#         expect = "Redeclared Type: foo\n"
#         self.assertTrue(TestChecker.test(input,expect,579))
#     def test_580(self):
#         input = """
#         var main int;
#         func main(a int ) {
#             return 
#         }
#         """
#         expect = """Redeclared Variable: main\n"""
#         self.assertTrue(TestChecker.test(input, expect, 580))