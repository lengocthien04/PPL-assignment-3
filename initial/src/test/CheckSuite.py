
import unittest
from TestUtils import TestChecker
from AST import *

class CheckSuite(unittest.TestCase):
    def test_redeclared_var(self):
        input = """var a int; var b int; var a int = a; """
        expect = "Redeclared Variable: a\n"
        self.assertTrue(TestChecker.test(input,expect,400))

    def test_type_mismatch_vardecl(self):
        input = """var a int = 1.2;"""
        expect = "Type Mismatch: VarDecl(a,IntType,FloatLiteral(1.2))\n"
        self.assertTrue(TestChecker.test(input,expect,401))

    def test_undeclared_identifier(self):
        input = Program([VarDecl("a",IntType(),Id("b"))])
        expect = "Undeclared Identifier: b\n"
        self.assertTrue(TestChecker.test(input,expect,402))
        
    def test_redeclared_const(self):
        input = """var a int; const a = 12; """
        expect = "Redeclared Constant: a\n"
        self.assertTrue(TestChecker.test(input,expect,403))
        
    def test_param_and_local_same_name(self):
        input = """func a(a,b int) int { var a int = a; }; """
        expect = ""
        self.assertTrue(TestChecker.test(input,expect,404))
        
    def test_undeclared_in_func(self):
        input = """func a(b int) int { var a int = c; }; """
        expect = "Undeclared Identifier: c\n"
        self.assertTrue(TestChecker.test(input,expect,405))
        
    def test_type_coercion_int_to_float(self):
        input = """func a(b int, c float) int { var a float = b; }; """
        expect = ""
        self.assertTrue(TestChecker.test(input,expect,406))
        
    def test_type_mismatch_float_to_int(self):
        input = """func a(b int, c float) int { var a int = c; }; """
        expect = "Type Mismatch: VarDecl(a,IntType,Id(c))\n"
        self.assertTrue(TestChecker.test(input,expect,407))
        
    def test_valid_int_expression(self):
        input = """func a(b int, c float) int { var a int = 1 + 2;}; """
        expect = ""
        self.assertTrue(TestChecker.test(input,expect,408))
        
    def test_type_mismatch_float_in_int_expression(self):
        input = """func a(b int, c float) int { var a int = 1 + b*2 + 2.2;}; """
        expect = "Type Mismatch: VarDecl(a,IntType,BinaryOp(BinaryOp(IntLiteral(1),+,BinaryOp(Id(b),*,IntLiteral(2))),+,FloatLiteral(2.2)))\n"
        self.assertTrue(TestChecker.test(input,expect,409))
        
    def test_valid_float_expression(self):
        input = """func a(b int, c float) int { var a float = 1 + 2.2+c;}; """
        expect = ""
        self.assertTrue(TestChecker.test(input,expect,410))
        
    def test_redeclared_builtin(self):
        input = """var getInt int;"""
        expect = "Redeclared Variable: getInt\n"
        self.assertTrue(TestChecker.test(input,expect,411))
        
    def test_valid_int_complex_expression(self):
        input = """var a int = 3; var b int = a*3+4/4;"""
        expect = ""
        self.assertTrue(TestChecker.test(input,expect,412))
        
    def test_type_mismatch_float_in_complex_expression(self):
        input = """var a int = 3; var b int = a+3*1.0;"""
        expect = "Type Mismatch: VarDecl(b,IntType,BinaryOp(Id(a),+,BinaryOp(IntLiteral(3),*,FloatLiteral(1.0))))\n"
        self.assertTrue(TestChecker.test(input,expect,413))
        
    def test_undeclared_type(self):
        input = """var a Car = 10; var b int = 10;"""
        expect = "Undeclared Type: Car\n"
        self.assertTrue(TestChecker.test(input,expect,414))
        
    def test_valid_recursive_call(self):
        input = """ 
                func m (a int) { var a int; m(a);};"""
        expect = ""
        self.assertTrue(TestChecker.test(input,expect,415))
        
    def test_valid_if_statement(self):
        input = """func main (a int) { 
            var a int = 3;
            if (a==5+2-4) {
                return;
            }
        
        };"""
        expect = ""
        self.assertTrue(TestChecker.test(input,expect,416))
        
    def test_type_mismatch_if_condition(self):
        input = """func main (a int) { 
            var a int = 3;
            if (3+2) {
                return ;
            }
        
        };"""
        expect = "Type Mismatch: If(BinaryOp(IntLiteral(3),+,IntLiteral(2)),Block([Return()]))\n"
        self.assertTrue(TestChecker.test(input,expect,417))
        
    def test_valid_nested_if(self):
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
        
    def test_scope_undeclared_variable(self):
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
        
    def test_valid_if_with_type_coercion(self):
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
        
    def test_scope_in_else_undeclared(self):
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
        
    def test_valid_interface_definition(self):
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
        self.assertTrue(TestChecker.test(input,expect,422))
        
    def test_redeclared_prototype(self):
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
        self.assertTrue(TestChecker.test(input,expect,423))
        
    def test_valid_struct_definition(self):
        input = """
                 type Person struct {
                    name string
                    height float
                    weight int
                 }
                """
        expect = ""
        self.assertTrue(TestChecker.test(input,expect,424))  
        
    def test_redeclared_field(self):
        input = """
                 type Person struct {
                    name string
                    height float
                    weight int
                    name int
                 }
                """
        expect = "Redeclared Field: name\n"
        self.assertTrue(TestChecker.test(input,expect,425))
        
    def test_valid_struct_instance(self):
        input = """
                 type Employee struct {
                    name string
                    salary float
                    id int
                    active boolean
                 }
                 var e Employee;
                """
        expect = ""
        self.assertTrue(TestChecker.test(input,expect,426))
        
    def test_valid_struct_with_field_init(self):
        input = """
                 type Employee struct {
                    name string
                    salary float
                    id int
                    active boolean
                 }
                 var e Employee = Employee {name:"John"};
                """
        expect = ""
        self.assertTrue(TestChecker.test(input,expect,427))
        
    def test_undeclared_field(self):
        input = """
                 type Employee struct {
                    name string
                    salary float
                    id int
                    active boolean
                 }
                 var e Employee = Employee {name:"John",position:"Manager"};
                """
        expect = "Undeclared Field: position\n"
        self.assertTrue(TestChecker.test(input,expect,428))
        
    def test_type_mismatch_struct_field(self):
        input = """
                 type Employee struct {
                    name string
                    salary float
                    id int
                    active boolean
                 }
                 var e Employee = Employee {name:"John",salary:"High"};
                """
        expect = """Type Mismatch: StructLiteral(Employee,[(name,StringLiteral("John")),(salary,StringLiteral("High"))])\n"""
        self.assertTrue(TestChecker.test(input,expect,429))
        
    def test_valid_nested_struct(self):
        input = """
                type Department struct {
                    code int
                 }
                 type Employee struct {
                    name string
                    dept Department
                    id int
                    active boolean
                 }

                 var e Employee = Employee {name:"John",dept: Department { code: 101 }};
                """
        expect = """"""
        self.assertTrue(TestChecker.test(input,expect,430))
        
    def test_type_mismatch_nested_struct(self):
        input = """
                type Department struct {
                    code int
                 }
                 type Division struct {
                    code int
                 }
                 type Employee struct {
                    name string
                    dept Department
                    id int
                    active boolean
                 }

                 var e Employee = Employee {name:"John",dept: Division { code: 101 }};
                """
        expect = """Type Mismatch: StructLiteral(Employee,[(name,StringLiteral("John")),(dept,StructLiteral(Division,[(code,IntLiteral(101))]))])\n"""
        self.assertTrue(TestChecker.test(input,expect,431))
        
    def test_valid_deep_nested_struct(self):
        input = """
                type Department struct {
                    code int
                 }
                 type Company struct {
                    dept Department
                 }
                 type Employee struct {
                    name string
                    dept Department
                    company Company
                    active boolean
                 }

                 var e Employee = Employee {name:"John",dept: Department { code: 101 },company: Company { dept: Department { code: 101 }}};
                """
        expect = """"""
        self.assertTrue(TestChecker.test(input,expect,432))
        
    def test_undeclared_field_in_nested_struct(self):
        input = """
                type Department struct {
                    code int
                 }
                 type Company struct {
                    dept Department
                 }
                 type Employee struct {
                    name string
                    dept Department
                    company Company
                    active boolean
                 }

                 var e Employee = Employee {name:"John",dept: Department { code: 101 },company: Company { dept: Company { code: 101 }}};
                """
        expect = """Undeclared Field: code\n"""
        self.assertTrue(TestChecker.test(input,expect,433))
        
    def test_valid_struct_assignment(self):
        input = """
                type Department struct {
                    code int
                 }
                 type Company struct {
                    dept Department
                 }
                 type Employee struct {
                    name string
                    dept Department
                    company Company
                    active boolean
                 }

                 var e Employee = Employee {name:"John",dept: Department { code: 101 },company: Company { dept: Department { code: 101 }}};
                 var f Employee = e;
                """
        expect = """"""
        self.assertTrue(TestChecker.test(input,expect,434))
        
    def test_valid_interface_implementation(self):
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
                var v Vehicle = Car { speed: 10};
                """
        expect = """"""
        self.assertTrue(TestChecker.test(input,expect,435))
        
    def test_incomplete_interface_implementation(self):
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
                var v Vehicle = Car { speed: 10};
                """
        expect = """Type Mismatch: VarDecl(v,Id(Vehicle),StructLiteral(Car,[(speed,IntLiteral(10))]))\n"""
        self.assertTrue(TestChecker.test(input,expect,436))
        
    def test_function_as_variable(self):
        input = """
                func Test() int {
                    var a int = 3;
                    return a;
                }
                var a int = Test;
                """
        expect = """Type Mismatch: VarDecl(a,IntType,Id(Test))\n"""
        self.assertTrue(TestChecker.test(input,expect,437))
        
    def test_function_call_as_variable(self):
        input = """
                func Test() int {
                    var a int = 3;
                    return a;
                }
                var a int = Test();
                """
        expect = """"""
        self.assertTrue(TestChecker.test(input,expect,438))
        
    def test_valid_if_return(self):
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
                """
        expect = """"""
        self.assertTrue(TestChecker.test(input,expect,439))
        
    def test_type_mismatch_function_return(self):
        input = """
                func Test() int {
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
        self.assertTrue(TestChecker.test(input,expect,440))
        
    def test_valid_struct_return(self):
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
        self.assertTrue(TestChecker.test(input,expect,441))
        
    def test_type_mismatch_float_to_int_return(self):
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
        self.assertTrue(TestChecker.test(input,expect,442))
        
    def test_method_with_return_value(self):
        input = """
                type Person interface {
                    GetName() string
                }
                type Student struct {
                    name string
                }
                func (s Student) GetName() string {
                    return s.name
                }
                type Vehicle interface {
                    GetSpeed() int
                    SetSpeed(speed int)
                    GetDriver() Person
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
                func (c Car) GetDriver() Person {
                    return Student { name: "John" };
                }
                """
        expect = """Type Mismatch: Return(StructLiteral(Student,[(name,StringLiteral("John"))]))\n"""
        self.assertTrue(TestChecker.test(input,expect,443))
        
    def test_undeclared_function_call(self):
        input = """
                func Test() int {
                    var a int = 3;
                    return a;
                }
                var x = 12;
                var a int = calculate();
                """
        expect = """Undeclared Function: calculate\n"""
        self.assertTrue(TestChecker.test(input,expect,444))
        
    def test_invalid_function_call_args(self):
        input = """
                func Test() int {
                    var a int = 3;
                    return a;
                }
                var x = 12;
                var a int = Test(2);
                """
        expect = """Type Mismatch: FuncCall(Test,[IntLiteral(2)])\n"""
        self.assertTrue(TestChecker.test(input,expect,445))
        
    def test_valid_function_call_params(self):
        input = """
                func Calculate(a float, b int) int {
                    var x int = 3;
                    return x;
                }
                var x = 12;
                var a int = Calculate(1.2,2);
                """
        expect = """"""
        self.assertTrue(TestChecker.test(input,expect,446))
        
    def test_type_mismatch_function_param(self):
        input = """
                func Calculate(a float, b int) int {
                    var x int = 3;
                    return x;
                }
                var x = 12;
                var a int = Calculate(1,2);
                """
        expect = """Type Mismatch: FuncCall(Calculate,[IntLiteral(1),IntLiteral(2)])\n"""
        self.assertTrue(TestChecker.test(input,expect,447))
        
    def test_valid_complex_function_call(self):
        input = """
                func Calculate(a int, b int) int { 
                    var x int = 3;
                    return x;
                }
                var x = 12;
                var a int = Calculate(1,2)+12-3*6-Calculate(1,-2);
                """
        expect = """"""
        self.assertTrue(TestChecker.test(input,expect,448))
        
    def test_invalid_field_access_primitive(self):
        input = """
                type Car struct {
                    speed int
                }
                func Test(a int, b int) int { 
                    var x int = 3;
                    var c Car = Car { speed: x };
                    return a.speed;
                }
                """
        expect = """Type Mismatch: FieldAccess(Id(a),speed)\n"""
        self.assertTrue(TestChecker.test(input,expect,449))
        
    def test_valid_field_access_struct(self):
        input = """
                type Car struct {
                    speed int
                    model string
                }
                func Test(a int, b int) int { 
                    var x int = 3;
                    var c Car = Car { speed: x };
                    return c.speed;
                }
                """
        expect = """"""
        self.assertTrue(TestChecker.test(input,expect,450))
        
    def test_type_mismatch_field_access(self):
        input = """
                type Car struct {
                    speed int
                    model string
                }
                func Test(a int, b int) int { 
                    var x int = 3;
                    var c Car = Car { speed: x };
                    return c.model;
                }
                """
        expect = """Type Mismatch: Return(FieldAccess(Id(c),model))\n"""
        self.assertTrue(TestChecker.test(input,expect,451))
        
    def test_undeclared_field_access(self):
        input = """
                type Car struct {
                    speed int
                    model string
                }
                func Test(a int, b int) int { 
                    var x int = 3;
                    var c Car = Car { speed: x };
                    return c.color;
                }
                """
        expect = """Undeclared Field: color\n"""
        self.assertTrue(TestChecker.test(input,expect,452))
        
    def test_valid_nested_field_access(self):
        input = """
                type Person struct {
                    name string
                }
                type Car struct {
                    speed int
                    model string
                    owner Person
                }
                func Test(a int, b int) string { 
                    var x int = 3;
                    var c Car = Car { speed: x };
                    return c.owner.name;
                }
                """
        expect = """"""
        self.assertTrue(TestChecker.test(input,expect,453))
        
    def test_valid_struct_initialization_with_fields(self):
        input = """
                type Person struct {
                    name string
                }
                type Car struct {
                    speed int
                    model string
                    owner Person
                }
                func Test(a int, b int) string { 
                    var x int = 3;
                    var c Car = Car { speed: x, owner: Person { name: "John" } };
                    return c.owner.name;
                }
                """
        expect = """"""
        self.assertTrue(TestChecker.test(input,expect,454))
        
    def test_valid_complex_if_with_struct(self):
        input = """
                type Person struct {
                    name string
                }
                type Car struct {
                    speed int
                    model string
                    owner Person
                }
                type Company struct {
                    age int
                }
                func Test(a int, b int) string { 
                    var x int = 3;
                    var c Car = Car { speed: x, owner: Person { name: "John" } };
                    if (x == c.speed) {
                        return c.owner.name;
                    } else {
                        var z = Company { age: x };
                        var i = z.age+x;
                        return "ok";
                    }
                    return c.owner.name;
                }
                """
        expect = """"""
        self.assertTrue(TestChecker.test(input,expect,455))
        
    def test_valid_method_call(self):
        input = """
                type Person struct {
                    name string
                    age int
                }
                func (p Person) getName() string {
                    return p.name
                }
                func main() {
                    var p = Person { name: "John", age: 30 };
                    var n string = p.getName();
                }
                """
        expect = """"""
        self.assertTrue(TestChecker.test(input,expect,456))
        
    def test_type_mismatch_method_call(self):
        input = """
                type Person struct {
                    name string
                    age int
                }
                func (p Person) getName() string {
                    return p.name
                }
                func main() {
                    var p = Person { name: "John", age: 30 };
                    p.getName();
                }
                """
        expect = """Type Mismatch: MethodCall(Id(p),getName,[])\n"""
        self.assertTrue(TestChecker.test(input,expect,457))
        
    def test_valid_void_method_call(self):
        input = """
                type Student struct {
                    name string
                    age int
                }
                func (s Student) printInfo() {
                    return 
                }
                func main() {
                    var s = Student { name: "John" };
                    s.printInfo();
                }
                """
        expect = """"""
        self.assertTrue(TestChecker.test(input,expect,458))
        
    def test_valid_array_declaration(self):
        input = """
                type Student struct {
                    name string
                    grades [3] int
                }
                func (s Student) getName() {
                    return 
                }
                func create() [3] int {
                    var a [3] int;
                    return a
                }
                """
        expect = """"""
        self.assertTrue(TestChecker.test(input,expect,459))
        
    def test_type_mismatch_array_return(self):
        input = """
                type Student struct {
                    name string
                    grades [3] int
                }
                func (s Student) getName() {
                    return 
                }
                func create() [3] float {
                    var a [3] int;
                    return a
                }
                """
        expect = """Type Mismatch: Return(Id(a))\n"""
        self.assertTrue(TestChecker.test(input,expect,460))
        
    def test_type_mismatch_array_size(self):
        input = """
                type Student struct {
                    name string
                    grades [3] int
                }
                func (s Student) getName() {
                    return 
                }
                func create() [5] int {
                    var a [3] int;
                    return a
                }
                """
        expect = """Type Mismatch: Return(Id(a))\n"""
        self.assertTrue(TestChecker.test(input,expect,461))
        
    def test_valid_multidim_array(self):
        input = """
                type Student struct {
                    name string
                    grades [3][4][2] int
                }
                func (s Student) getName() {
                    return 
                }
                func create() [3][4][2] int {
                    var a [3][4][2] int;
                    return a
                }
                """
        expect = """"""
        self.assertTrue(TestChecker.test(input,expect,462))
        
    def test_valid_array_with_const_size(self):
        input = """
                func create() [3] int {
                    const c = 3;
                    var a [c] int;
                    return a
                }
                """
        expect = """"""
        self.assertTrue(TestChecker.test(input,expect,463))
        
    def test_valid_array_with_expr_size(self):
        input = """
                func create() [3] int {
                    const c = 1+2;
                    var a [c] int;
                    return a
                }
                """
        expect = """"""
        self.assertTrue(TestChecker.test(input,expect,464))
        
    def test_type_mismatch_array_size_expr(self):
        input = """
                func create() [4] int {
                    const c = 1+2;
                    var a [c] int;
                    return a
                }
                """
        expect = """Type Mismatch: Return(Id(a))\n"""
        self.assertTrue(TestChecker.test(input,expect,465))

    def test_type_mismatch_method_param(self):
        input = """
                type Student struct {
                    name string
                    grades [3] int
                }
                func (s Student) getGrades(a [4] int) [3] int {
                    return s.grades               
                }
                func main() {
                    var s = Student { name:"John" }
                    var g [3] int;
                    var r = s.getGrades(g);
                }
                """
        expect = """Type Mismatch: MethodCall(Id(s),getGrades,[Id(g)])\n"""
        self.assertTrue(TestChecker.test(input,expect,466))
        
    def test_redeclared_method(self):
        input = """
                type Student struct {
                    name string
                    grades [3] int
                }
                const c = 3;
                func (s Student) grades(a [c] int) [c] int {
                    return s.grades                
                }
                func main() {
                    var s = Student { name:"John" }
                    var g [c] int;
                    var r = s.grades(g);
                }
                """
        expect = """Redeclared Method: grades\n"""
        self.assertTrue(TestChecker.test(input,expect,467))
        
    def test_valid_const_in_array(self):
        input = """
                type Student struct {
                    name string
                    grades [5] int
                }
                const c = 5;
                func (s Student) getGrades() [c] int {
                    return s.grades                
                }
                var nameVal = "John"
                func main() {
                    var s = Student { name:nameVal }
                    var g [c] int = s.getGrades();
                }
                """
        expect = ""
        self.assertTrue(TestChecker.test(input,expect,468))
        
    def test_assignment_operators(self):
        input = """
                const c = 5;

                type Student struct {
                    name string
                    grades [c] int
                }
                func (s Student) getGrades() [c] int {
                    return s.grades                
                }
                func createStudent() Student {
                    return Student { name:"John" }
                }
               func main() {
                    var a int;
                    var b float;
                    var t string;
                    var d boolean;
                    var e Student;
                    var g [c] int;
                    
                    a := 1;
                    b += 2;
                    t += "abc";
                    d := !true;
                    e := createStudent();
                    e := Student { name:"John" };
                    g := e.getGrades();
                }
                """
        expect = ""
        self.assertTrue(TestChecker.test(input,expect,469))
        
    def test_valid_array_literals(self):
        input = """
                var bools = [3][4] boolean { {true,false,true,false},{false,true,false,true},{true,false,true,false}}
                var floats = [3][4] float { {1.1,2.2,3.3,4.4},{5.5,6.6,7.7,8.8},{9.9,10.1,11.2,12.3}}
                """
        expect = ""
        self.assertTrue(TestChecker.test(input,expect,470))
        
    def test_valid_array_declaration_with_literal(self):
        input = """
                var nums [3] int = [3] int {1,2,3}
                """
        expect = ""
        self.assertTrue(TestChecker.test(input,expect,471))
        
    def test_type_mismatch_array_literal(self):
        input = """
                var nums [3] int = [3] int {1,2.2,3}
                """
        expect = """Type Mismatch: ArrayLiteral([IntLiteral(3)],IntType,[IntLiteral(1),FloatLiteral(2.2),IntLiteral(3)])\n"""
        self.assertTrue(TestChecker.test(input,expect,472))
        
    def test_dynamic_array_size(self):
        input = """
                var c = 6/2 + 3 - 1*2;
                var nums [4] int = [c] int {1,c,3}
                """
        expect = ""
        self.assertTrue(TestChecker.test(input,expect,473))
        
    def test_array_size_mismatch(self):
        input = """
                var c = 6/2 + 3 - 1*2;
                var nums [5] int = [c] int {1,c,3}
                """
        expect = """Type Mismatch: VarDecl(nums,ArrayType(IntType,[IntLiteral(5)]),ArrayLiteral([Id(c)],IntType,[IntLiteral(1),Id(c),IntLiteral(3)]))\n"""
        self.assertTrue(TestChecker.test(input,expect,474))
        
    def test_valid_array_type_coercion(self):
        input = """
                var c = 6/2 + 3 - 1*2;
                var nums [4] float = [c] int {1,c,3}
                """
        expect = ""
        self.assertTrue(TestChecker.test(input,expect,475))
        
    def test_multidim_array_type_mismatch(self):
        input = """
                var c = 6/2 + 3 - 1*2;
                var matrix [4][3] float = [c] [2] int { {1,c,3},{1,c,3}}
                """
        expect = """Type Mismatch: VarDecl(matrix,ArrayType(FloatType,[IntLiteral(4),IntLiteral(3)]),ArrayLiteral([Id(c),IntLiteral(2)],IntType,[[IntLiteral(1),Id(c),IntLiteral(3)],[IntLiteral(1),Id(c),IntLiteral(3)]]))\n"""
        self.assertTrue(TestChecker.test(input,expect,476))
        
    def test_valid_struct_array(self):
        input = """
                type Student struct {
                    name string
                    grades [3] int
                }
                var c = 6/2 + 3 - 1*2;
                var students [4] Student = [c] Student { Student { name:"Alice" }, Student { name:"Bob" }, Student { name:"Charlie" }, Student { name:"David" } }
                """
        expect = ""
        self.assertTrue(TestChecker.test(input,expect,477))
        
    def test_invalid_interface_array(self):
        input = """
                type Person interface {
                    getName() string
                    getGrades() [3]int
                }
                type Student struct {
                    name string
                    grades [3] int
                }
                func (s Student) getName() string {
                    return s.name
                }
                func (s Student) getGrades() [3]int {
                    return s.grades
                }
                var c = 6/2 + 3 - 1*2;
                var people [4] Person = [c] Student { Student { name:"Alice" }, Student { name:"Bob" }, Student { name:"Charlie" }, Student { name:"David" } }
                """
        expect = """Type Mismatch: VarDecl(people,ArrayType(Id(Person),[IntLiteral(4)]),ArrayLiteral([Id(c)],Id(Student),[StructLiteral(Student,[(name,StringLiteral("Alice"))]),StructLiteral(Student,[(name,StringLiteral("Bob"))]),StructLiteral(Student,[(name,StringLiteral("Charlie"))]),StructLiteral(Student,[(name,StringLiteral("David"))])]))\n"""
        self.assertTrue(TestChecker.test(input,expect,478))
        
    def test_struct_type_mismatch_array(self):
        input = """
                type Car struct {
                    model string
                }
                type Student struct {
                    name string
                    grades [3] int
                }
                func (s Student) getName() string {
                    return s.name
                }
                func (s Student) getGrades() [3]int {
                    return s.grades
                }
                var c = 6/2 + 3 - 1*2;
                var vehicles [4] Car = [c] Student { Student { name:"Alice" }, Student { name:"Bob" }, Student { name:"Charlie" }, Student { name:"David" } }
                """
        expect = """Type Mismatch: VarDecl(vehicles,ArrayType(Id(Car),[IntLiteral(4)]),ArrayLiteral([Id(c)],Id(Student),[StructLiteral(Student,[(name,StringLiteral("Alice"))]),StructLiteral(Student,[(name,StringLiteral("Bob"))]),StructLiteral(Student,[(name,StringLiteral("Charlie"))]),StructLiteral(Student,[(name,StringLiteral("David"))])]))\n"""
        self.assertTrue(TestChecker.test(input,expect,479))
        
    def test_valid_struct_array_with_expr(self):
        input = """
                type Student struct {
                    name string
                    age int
                }
                func (s Student) getName() string {
                    return s.name
                }
                func (s Student) getAge() int {
                    return s.age
                }        
                var bob = Student { name:"Bob", age:25 }
                var c = 6/2 + 3 - 1*2;
                var students [4] Student = [c] Student { bob, Student { name:"Alice" }, Student { name:"Charlie" }, Student { name:"David" } }
                """ 
        expect = ""
        self.assertTrue(TestChecker.test(input,expect,480))
        
    def test_array_element_type_mismatch(self):
        input = """
                type Student struct {
                    name string
                    age int
                }
                func (s Student) getName() string {
                    return s.name
                }
                type Teacher struct {
                    name string
                    age int
                }
                func (s Student) getAge() int {
                    return s.age
                }        
                var teacher = Teacher { name:"Mr. Smith", age:45 }
                var c = 6/2 + 3 - 1*2;
                var students [4] Student = [c] Student { teacher, Student { name:"Alice" }, Student { name:"Charlie" }, Student { name:"David" } }
                """ 
        expect = """Type Mismatch: ArrayLiteral([Id(c)],Id(Student),[Id(teacher),StructLiteral(Student,[(name,StringLiteral("Alice"))]),StructLiteral(Student,[(name,StringLiteral("Charlie"))]),StructLiteral(Student,[(name,StringLiteral("David"))])])\n"""
        self.assertTrue(TestChecker.test(input,expect,481))
        
    def test_valid_for_condition(self):
        input = """
                func main() {
                    for (true) {
                        return
                    }
                }
                """ 
        expect = ""
        self.assertTrue(TestChecker.test(input,expect,482))
        
    def test_valid_for_with_var_condition(self):
        input = """
                func main() {
                    var isValid boolean
                    for (isValid) {
                        return
                    }
                }
                """ 
        expect = ""
        self.assertTrue(TestChecker.test(input,expect,483))
        
    def test_valid_for_with_complex_condition(self):
        input = """
                func main() {
                    var isValid boolean
                    for (1+2*3.2<122.9) {
                        return
                    }
                }
                """ 
        expect = ""
        self.assertTrue(TestChecker.test(input,expect,484))
        
    def test_valid_for_with_complex_boolean_condition(self):
        input = """
                func main() {
                    var isValid boolean
                    var count = 5;
                    for (1+2*3.2<122.9+count||isValid) {
                        return
                    }
                }
                """ 
        expect = ""
        self.assertTrue(TestChecker.test(input,expect,485))
        
    def test_valid_nested_for_and_if(self):
        input = """
                func main() {
                    var isValid boolean
                    var count = 5;
                    if (isValid){
                        for (1+2*3.2<122.9+count||isValid) {
                            return
                        }   
                    }
                }
                """ 
        expect = ""
        self.assertTrue(TestChecker.test(input,expect,486))
        
    def test_valid_deep_nested_for_with_scopes(self):
        input = """
                func main() {
                    var isValid boolean
                    var count = 5;
                    var something = 5;
                    if (isValid){
                        var something float
                        for (1+2*3.2<122.9+count||isValid) {
                            var something boolean
                            for (something) {
                                var something string
                                continue
                            }
                            return
                        }   
                    }
                }
                """ 
        expect = ""
        self.assertTrue(TestChecker.test(input,expect,487))
        
    def test_undeclared_index_var_in_range(self):
        input = """
                func main() {
                    var isValid boolean
                    var count = 5;
                    var something = 5;
                    for i,_ := range [3] int { 1, 2, 3 } {
                        for var j = 0; j < 3; j+=1 {
                            var something string
                            continue
                        }
                    }
                }
                """ 
        expect = """Undeclared Identifier: i\n"""
        self.assertTrue(TestChecker.test(input,expect,488))
        
    def test_type_mismatch_range(self):
        input = """
                func main() {
                    var isValid boolean
                    var count = 5;
                    var something = 5;
                    var idx int;
                    var val int;
                    for idx, val := range isValid {
                        return
                    }
                }
                """ 
        expect = """Type Mismatch: ForEach(Id(idx),Id(val),Id(isValid),Block([Return()]))\n"""
        self.assertTrue(TestChecker.test(input,expect,489))
        
    def test_valid_foreach_with_string_array(self):
        input = """
                func main() {
                    var isValid boolean
                    var count = 5;
                    var something = 5;
                    var names [3] string = [3] string {"Alice", "Bob", "Charlie"}
                    var idx = 0;
                    var name = "default";
                    for idx, name := range names {
                        if (idx<3) {
                            return
                        }
                    }
                }
                """ 
        expect = ""
        self.assertTrue(TestChecker.test(input,expect,490))
        
    def test_type_mismatch_foreach_value(self):
        input = """
                func main() {
                    var isValid boolean
                    var count = 5;
                    var something = 5;
                    var names [3] string = [3] string {"Alice", "Bob", "Charlie"}
                    var val = names[0];
                    var idx = 0;
                    for idx, val := range names {
                        if (idx<3) {
                            count += val
                            return
                        }
                    }
                }
                """ 
        expect = """Type Mismatch: BinaryOp(Id(count),+,Id(val))\n"""
        self.assertTrue(TestChecker.test(input,expect,491))
        
    def test_valid_foreach_with_int_array(self):
        input = """
                func main() {
                    var isValid boolean
                    var count = 5;
                    var something = 5;
                    var numbers [3] int = [3] int { 1,2,3}
                    var val = numbers[0];
                    var idx = 1;
                    for idx, val := range numbers {
                        if (idx<3) {
                            count %= val
                            return
                        }
                    }
                }
                """ 
        expect = ""
        self.assertTrue(TestChecker.test(input,expect,492))
        
    def test_undeclared_value_var(self):
        input = """
                func main() {
                    var isValid boolean
                    var count = 5;
                    var something = 5;
                    var numbers [3] int = [3] int { 1,2,3}
                    for _, val := range numbers {
                        return
                    }
                }
                """ 
        expect = """Undeclared Identifier: val\n"""
        self.assertTrue(TestChecker.test(input,expect,493))
        
    def test_valid_nested_for_loops(self):
        input = """
                func main() {
                    var isValid boolean
                    var count = 5;
                    var something = 5;
                    var names [3] string = [3] string {"Alice", "Bob", "Charlie"}
                    var idx = 12;
                    val := names[idx];
                    for idx, val := range names {
                        for j:= 0; count < 3; count+= 3 {
                            return
                        }
                    }
                }
                """ 
        expect = ""
        self.assertTrue(TestChecker.test(input,expect,494))
        
    def test_valid_for_with_init(self):
        input = """
                func main() {
                    var isValid boolean
                    var count = 5;
                    var something = 5;
                    var names [3] string = [3] string {"Alice", "Bob", "Charlie"}
                    var idx = 12;
                    for var j= 0; j < 3; j+= 3 {
                            return
                    }
                }
                """ 
        expect = ""
        self.assertTrue(TestChecker.test(input,expect,495))
        
    def test_valid_array_indexing(self):
        input = """
                func main() {
                    var isValid boolean
                    var count = 5;
                    var something = 5;
                    var names [3] string = [3] string {"Alice", "Bob", "Charlie"}
                    var idx = 12;
                    var name = names[0]
                }
                """ 
        expect = ""
        self.assertTrue(TestChecker.test(input,expect,496))
        
    def test_valid_nested_struct_array_access(self):
        input = """
                type Student struct {
                    name string
                    scores [3] int
                }
                type School struct {
                    name string
                    students [5] Student
                }
                func main() {
                    var mySchool = School { name:"Central High"}
                    var score int = mySchool.students[0].scores[0]
                }
                """ 
        expect = ""
        self.assertTrue(TestChecker.test(input,expect,497))
        
    def test_type_mismatch_nested_array_access(self):
        input = """
                type Student struct {
                    name string
                    scores [3] float
                }
                type School struct {
                    name string
                    students [5] Student
                }
                func main() {
                    var mySchool = School { name:"Central High"}
                    var score int = mySchool.students[0].scores[0]
                }
                """ 
        expect = """Type Mismatch: VarDecl(score,IntType,ArrayCell(FieldAccess(ArrayCell(FieldAccess(Id(mySchool),students),[IntLiteral(0)]),scores),[IntLiteral(0)]))\n"""
        self.assertTrue(TestChecker.test(input,expect,498))
        
    def test_valid_multidim_array_index(self):
        input = """
                type Student struct {
                    name string
                    scores [3] float
                }
                type School struct {
                    name string
                    students [5] Student
                }
                func main() {
                    var mySchool = School { name:"Central High"}
                    var matrix [3][4] int;
                    var row [4] int = matrix[0]
                }
                """ 
        expect = ""
        self.assertTrue(TestChecker.test(input,expect,499))
