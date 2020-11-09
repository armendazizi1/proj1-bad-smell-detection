
from owlready2 import *
import rdflib
import rdflib.plugins.sparql as sq
import javalang
import pytest

def populateOntology(onto, tree):
    for path, node in tree.filter(javalang.tree.ClassDeclaration):
        cd = onto["ClassDeclaration"]()
        cd.jname = [node.name]
        for member in node.body:
            if (type(member)== javalang.tree.FieldDeclaration):
                for field in member.declarators:
                    fd = onto['FieldDeclaration']()
                    fd.jname = [field.name]
                    cd.body.append(fd)
            elif (type(member)== javalang.tree.ConstructorDeclaration):
                cod = onto['ConstructorDeclaration']()
                cod.jname = [member.name]
                populateWithStatements(cod, member, onto)
                populateWithParameters(cod, member, onto)
                cd.body.append(cod)
            elif (type(member) == javalang.tree.MethodDeclaration):
                md = onto['MethodDeclaration']()
                md.jname = [member.name]
                populateWithStatements(md,member,onto)
                populateWithParameters(md, member, onto)
                cd.body.append(md)


def populateWithParameters(memberDeclaration, member, onto):
    for _, param in member.parameters:
        parameter = onto[param[0][0].__class__.__name__]()
        memberDeclaration.parameters.append(parameter)

def populateWithStatements(memberDeclaration, member, onto):
    for _, stm in member.filter(javalang.tree.Statement):
        statement = onto[stm.__class__.__name__]()
        memberDeclaration.body.append(statement)


def findLongMethods(g):
    q = sq.prepareQuery(
        """SELECT ?cn ?mn ?s (COUNT(*)AS ?tot) WHERE {
                ?c a tree:ClassDeclaration .
                ?c tree:jname ?cn .
                ?c tree:body ?m .
                ?m a tree:MethodDeclaration .
                ?m tree:jname ?mn .
                ?m tree:body ?s .
                ?s a/rdfs:subClassOf* tree:Statement .
            } GROUP BY ?m
            HAVING (COUNT(?s) >= 20)
        """,
        initNs={"tree": "http://test.org/onto.owl#"})

    methods = g.query(q)
    return methods


def findMethodWithManyParameters(g):
    q = sq.prepareQuery(
        """SELECT ?cn ?mn (COUNT(*)AS ?tot) WHERE {
                ?c a tree:ClassDeclaration .
                ?c tree:jname ?cn .
                ?c tree:body ?m .
                ?m a tree:MethodDeclaration .
                ?m tree:jname ?mn .
                ?m tree:parameters ?p .
                ?p a tree:FormalParameter .
            } GROUP BY ?m
            HAVING (COUNT(?p) >= 5)
        """,
        initNs={"tree": "http://test.org/onto.owl#"})

    methods = g.query(q)
    return methods


def findConstructorWithManyParameters(g):
    q = sq.prepareQuery(
        """SELECT ?cn ?constr (COUNT(*)AS ?tot) WHERE {
                ?c a tree:ClassDeclaration .
                ?c tree:jname ?cn .
                ?c tree:body ?m .
                ?m a tree:ConstructorDeclaration .
                ?m tree:jname ?constr .
                ?m tree:parameters ?p .
                ?p a tree:FormalParameter .
            } GROUP BY ?m
            HAVING (COUNT(?p) >= 5)
        """,
        initNs={"tree": "http://test.org/onto.owl#"})

    constructors = g.query(q)
    return constructors


def findMethodsWithSwitch(g):
    q = sq.prepareQuery(
        """SELECT ?cn ?mn (COUNT(*)AS ?tot) WHERE {
                ?c a tree:ClassDeclaration .
                ?c tree:jname ?cn .
                ?c tree:body ?m .
                ?m a tree:MethodDeclaration .
                ?m tree:jname ?mn .
                ?m tree:body ?s .
                ?s a tree:SwitchStatement .
            } GROUP BY ?m
            HAVING (COUNT(?s) >= 1)
        """,
        initNs={"tree": "http://test.org/onto.owl#"})

    methods = g.query(q)
    return methods



def findLargeClasses(g):
    q = sq.prepareQuery(
        """SELECT ?cn (COUNT(*)AS ?tot) WHERE {
                ?c a tree:ClassDeclaration .
                ?c tree:jname ?cn .
                ?c tree:body ?m .
                ?m a tree:MethodDeclaration .
                
            } GROUP BY ?cn
            HAVING (COUNT(?m) >= 10)
        """,
        initNs={"tree": "http://test.org/onto.owl#"})

    classes = g.query(q)
    return classes


def findClassesWithOnlyGettersAndSetters(g):
    q = sq.prepareQuery(
        """SELECT ?cn (COUNT(*)AS ?tot) WHERE {
                ?c a tree:ClassDeclaration .
                ?c tree:jname ?cn .
                ?c tree:body ?m .
                ?m a tree:MethodDeclaration .
                ?m tree:jname ?mn .
                {FILTER (regex(?mn, "get.*"))} UNION {FILTER (regex(?mn, "set.*"))}
            } GROUP BY ?cn
        """,
        initNs={"tree": "http://test.org/onto.owl#"})

    classes = g.query(q)
    return classes

def findAllMethods(g):
    q = sq.prepareQuery(
        """SELECT ?cn (COUNT(*)AS ?tot) WHERE {
                ?c a tree:ClassDeclaration .
                ?c tree:jname ?cn .
                ?c tree:body ?m .
                ?m a tree:MethodDeclaration .
                ?m tree:jname ?mn .
            } GROUP BY ?cn
        """,
        initNs={"tree": "http://test.org/onto.owl#"})
    classes = g.query(q)
    return classes


def findLongConstructors(g):
    q = sq.prepareQuery(
        """SELECT ?cn ?mn ?s (COUNT(*)AS ?tot) WHERE {
                ?c a tree:ClassDeclaration .
                ?c tree:jname ?cn .
                ?c tree:body ?m .
                ?m a tree:ConstructorDeclaration .
                ?m tree:jname ?mn .
                ?m tree:body ?s .
                ?s a/rdfs:subClassOf* tree:Statement .
            } GROUP BY ?m
            HAVING (COUNT(?s) >= 20)
        """,
        initNs={"tree": "http://test.org/onto.owl#"})

    constructors = g.query(q)
    return constructors


def findConstructorsWithSwitch(g):
    q = sq.prepareQuery(
        """SELECT ?cn ?mn (COUNT(*)AS ?tot) WHERE {
                ?c a tree:ClassDeclaration .
                ?c tree:jname ?cn .
                ?c tree:body ?m .
                ?m a tree:ConstructorDeclaration .
                ?m tree:jname ?mn .
                ?m tree:body ?s .
                ?s a tree:SwitchStatement .
            } GROUP BY ?m
        """,
        initNs={"tree": "http://test.org/onto.owl#"})

    constructors = g.query(q)
    return constructors


def main():
    g = rdflib.Graph()
    g.load("tree2.owl")

    # LONG METHODS
    longMethods = findLongMethods(g)
    file = open('log.txt', 'w')
    file.write('\t Long Methods \t \n')
    file.write('-------------------------------------------------- \n')
    file.write("{: <18} {: <18} {: <18}\n".format("Class", "Method", "#Statements"))
    file.write('-------------------------------------------------- \n')
    for row in longMethods:
        file.write("{: <18} {: <18} {: <18}\n".format(row.cn, row.mn, row.tot))

    # LONG CONSTRUCTORS
    longConstructors = findLongConstructors(g)
    file.write('\n\n \t Long Constructors \t \n')
    file.write('-------------------------------------------------- \n')
    file.write("{: <18} {: <18} {: <18}\n".format("Class", "Constructor", "#Statements"))
    file.write('-------------------------------------------------- \n')
    for row in longConstructors:
        file.write("{: <18} {: <18} {: <18}\n".format(row.cn, row.mn, row.tot))

    # LARGE CLASS
    largeClasses = findLargeClasses(g)
    file.write('\n\n \t Long Classes \t \n')
    file.write('-------------------------------------------------- \n')
    file.write("{: <18} {: <18}\n".format("Class",  "#Methods"))
    file.write('-------------------------------------------------- \n')
    for row in largeClasses:
        file.write("{: <18} {: <18}\n".format(row.cn, row.tot))

    # METHODS WITH SWITCH
    methodsWithSwitch = findMethodsWithSwitch(g)
    file.write('\n\n \t Methods with switch statement \t \n')
    file.write('-------------------------------------------------- \n')
    file.write("{: <18} {: <18} {: <18} \n".format("Class","Method" ,"#SwitchStatements"))
    file.write('-------------------------------------------------- \n')
    for row in methodsWithSwitch:
        file.write("{: <18} {: <18} {: <18}\n".format(row.cn,row.mn, row.tot))

    # Constructors WITH SWITCH
    constructorsWithSwitch = findConstructorsWithSwitch(g)
    file.write('\n\n \t Constructors with switch statement \t \n')
    file.write('-------------------------------------------------- \n')
    file.write("{: <18} {: <18} {: <18} \n".format("Class","Constructor", "#SwitchStatements"))
    file.write('-------------------------------------------------- \n')
    for row in constructorsWithSwitch:
        file.write("{: <18} {: <18} {: <18}\n".format(row.cn,row.mn, row.tot))


    # METHOD WITH LONG PARAMETERS LIST

    methodsWithManyParemeters = findMethodWithManyParameters(g)
    file.write('\n\n \t Methods with many Parameters \t \n')
    file.write('-------------------------------------------------- \n')
    file.write("{: <18} {: <18} {: <18} \n".format("Class","Method", "#Paramteres"))
    file.write('-------------------------------------------------- \n')
    for row in methodsWithManyParemeters:
        file.write("{: <18} {: <18} {: <18}\n".format(row.cn,row.mn, row.tot))

    # CONSTRUCTORS WITH LONG PARAMETERS LIST

    constructorsWithManyParemeters = findConstructorWithManyParameters(g)
    file.write('\n\n \t Constructors with many Parameters \t \n')
    file.write('-------------------------------------------------- \n')
    file.write("{: <18} {: <18} {: <18} \n".format("Class", "Constructor", "#Paramteres"))
    file.write('-------------------------------------------------- \n')
    for row in constructorsWithManyParemeters:
        file.write("{: <18} {: <18} {: <18}\n".format(row.cn, row.constr, row.tot))


    # DATA CLASSES

    dataClasses = findClassesWithOnlyGettersAndSetters(g)
    allClasses = findAllMethods(g)
    file.write('\n\n \t Data Classes \t \n')
    file.write('-------------------------------------------------- \n')
    file.write("{: <18} {: <18} {: <18} \n".format("Class", "#methods", "#gettersSetters"))
    file.write('-------------------------------------------------- \n')
    for row in dataClasses:
        for row2 in allClasses:
            if row.cn.value == row2.cn.value:
                if row.tot.value == row2.tot.value:
                    file.write("{: <18} {: <18} {: <18}\n".format(row.cn, row2.tot, row.tot))

    file.close()

if __name__ == "__main__":
    main()



##################################
#       TESTING
##################################


@pytest.fixture
def setup_ontology():
    onto = get_ontology("tree.owl").load()
    yield onto
    for e in onto['ClassDeclaration'].instances(): destroy_entity(e)

def test_method(setup_ontology):
    onto = setup_ontology
    tree = javalang.parse.parse("class A { int f(int x) { x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++; } }")
    populateOntology(onto, tree)
    onto.save(file="tmp.owl", format="rdfxml")
    g = rdflib.Graph()
    g.load("tmp.owl")

    methods = findLongMethods(g)
    assert len(methods) == 1
    for row in methods:
        assert(row.cn.value == 'A')
        assert (row.mn.value == 'f')
        assert (row.tot.value == 21)

def test_data_class(setup_ontology):
    onto = setup_ontology
    tree = javalang.parse.parse("class A { int setNum(int x) { } int getNum(){} int getNum2(){} }")
    populateOntology(onto, tree)
    onto.save(file="tmp.owl", format="rdfxml")
    g = rdflib.Graph()
    g.load("tmp.owl")

    dataclasses = findClassesWithOnlyGettersAndSetters(g)
    normalclasses = findAllMethods(g)
    assert len(dataclasses) == len(normalclasses)
    for row in dataclasses:
        for row2 in normalclasses:
            assert (row.cn.value == row2.cn.value)
            assert (row.tot.value == row2.tot.value)




def test_method_with_many_parameters(setup_ontology):
    onto = setup_ontology
    tree = javalang.parse.parse("class A { int f2(int a, int b, int c, int d, int e, int f){} int f3(){}}")
    populateOntology(onto, tree)
    onto.save(file="tmp.owl", format="rdfxml")
    g = rdflib.Graph()
    g.load("tmp.owl")

    methods = findMethodWithManyParameters(g)
    assert len(methods) == 1
    for row in methods:
        assert (row.mn.value == 'f2')
        assert (row.tot.value == 6)



def test_construcotr_with_many_parameters(setup_ontology):
    onto = setup_ontology
    tree = javalang.parse.parse("class A { public A(int a, int b, int c, int d, int e, int g) { }  int f2(int a, int b, int c, int d, int e, int f){} int f3(){}}")
    populateOntology(onto, tree)
    onto.save(file="tmp.owl", format="rdfxml")
    g = rdflib.Graph()
    g.load("tmp.owl")

    constructors = findConstructorWithManyParameters(g)
    assert len(constructors) == 1
    for row in constructors:
        assert (row.constr.value == 'A')
        assert (row.tot.value == 6)


def test_method_with_switch(setup_ontology):
    onto = setup_ontology
    tree = javalang.parse.parse("class A { int f2(int "
                                "x) { switch(expression) { case x: break; default: }  switch(expression) { case x: "
                                "break; default: } switch(expression) { case x: break; default: }}  int f3(){} }")
    populateOntology(onto, tree)
    onto.save(file="tmp.owl", format="rdfxml")
    g = rdflib.Graph()
    g.load("tmp.owl")

    methods = findMethodsWithSwitch(g)
    assert len(methods) == 1
    for row in methods:
        assert (row.mn.value == 'f2')
        assert (row.tot.value == 3)


def test_constructor_with_switch(setup_ontology):
    onto = setup_ontology
    tree = javalang.parse.parse("class A { public A (int x) { switch(expression) { case x: break; default: } } int f2(int "
                                "x) { switch(expression) { case x: break; default: }  switch(expression) { case x: "
                                "break; default: } switch(expression) { case x: break; default: }}  int f3(){} }")
    populateOntology(onto, tree)
    onto.save(file="tmp.owl", format="rdfxml")
    g = rdflib.Graph()
    g.load("tmp.owl")

    constructors = findConstructorsWithSwitch(g)
    assert len(constructors) == 1
    for row in constructors:
        assert (row.mn.value == 'A')
        assert (row.tot.value == 1)



def test_constructor(setup_ontology):
    onto = setup_ontology
    tree = javalang.parse.parse("class A { public A (int x) { x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++; } }")
    populateOntology(onto, tree)
    onto.save(file="tmp.owl", format="rdfxml")
    g = rdflib.Graph()
    g.load("tmp.owl")

    constructors = findLongConstructors(g)
    assert len(constructors) == 1
    for row in constructors:
        assert(row.cn.value == 'A')
        assert (row.mn.value == 'A')
        assert (row.tot.value == 22)


def test_classes(setup_ontology):
    onto = setup_ontology
    tree = javalang.parse.parse("class A { void a(){} void b(){} void c(){} void d(){} void e(){} void f(){} void g(){} void h(){} void i(){} void j(){} void k(){}  void l(){}}")
    populateOntology(onto, tree)
    onto.save(file="tmp.owl", format="rdfxml")
    g = rdflib.Graph()
    g.load("tmp.owl")

    classes = findLargeClasses(g)
    assert len(classes) == 1
    for row in classes:
        assert(row.cn.value == 'A')
        assert (row.tot.value == 12)




