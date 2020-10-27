import javalang
import sys

import pytest
from owlready2 import *
import os



def populateOntology(onto, tree):
    for path, node in tree.filter(javalang.tree.ClassDeclaration):
        # print(node.body)
        cd = onto["ClassDeclaration"]()
        cd.jname = [node.name]
        # Got help from Gregory Wullimann here with his idea to populate the ontology in order, NOT SURE about this yet.
        for member in node.body:
            if (type(member)== javalang.tree.FieldDeclaration):
                for field in member.declarators:
                    fd = onto['FieldDeclaration']()
                    # print(field.name)
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
        # print(param[0][0].__class__.__name__)
        parameter = onto[param[0][0].__class__.__name__]()
        memberDeclaration.parameters.append(parameter)

def populateWithStatements(memberDeclaration, member, onto):
    for _, stm in member.filter(javalang.tree.Statement):
        # print(type(stm))
        # print(stm.__class__.__name__)
        statement = onto[stm.__class__.__name__]()
        memberDeclaration.body.append(statement)




def main():
    onto = get_ontology("tree.owl").load()

    for root, dirs, files in os.walk(sys.argv[1]):
        directory = root[-6:]
        if(directory == 'chess/'):
            for name in files:
                if name[-5:] == ".java":
                    str = open(os.path.join(root, name), 'r').read()
                    tree = javalang.parse.parse(str)
                    populateOntology(onto, tree)


    onto.save('./tree2.owl', format="rdfxml")


main()


@pytest.fixture
def setup_ontology():
    onto = get_ontology("tree.owl").load()
    yield onto
    for e in onto['ClassDeclaration'].instances(): destroy_entity(e)

def test_unit(setup_ontology):
    # onto = get_ontology("tree.owl").load()
    onto = setup_ontology
    tree = javalang.parse.parse("class A { int x, y; public A(){} public A(int a, int b){} void m(){} void m2(int k, int j){if(true){} while(false){} return; } }")
    populateOntology(onto, tree)
    a = onto['ClassDeclaration'].instances()[0]
    # print(tree)
    # Test Fields
    assert a.body[0].is_a[0].name == 'FieldDeclaration'
    assert a.body[0].jname[0] == 'x'
    assert a.body[1].is_a[0].name == 'FieldDeclaration'
    assert a.body[1].jname[0] == 'y'


    # Test Constructor
    assert a.body[2].is_a[0].name == 'ConstructorDeclaration'
    assert a.body[2].jname[0] == 'A'

    # Test Second Constructor
    assert a.body[3].is_a[0].name == 'ConstructorDeclaration'
    assert a.body[3].jname[0] == 'A'

    # Test Parameters of second constructor
    # print(a.body[3]
    assert a.body[3].parameters[0].is_a[0].name == 'FormalParameter'
    # print(a.body[3].parameters[0].name)
    assert a.body[3].parameters[0].name == 'formalparameter1'
    assert a.body[3].parameters[1].name == 'formalparameter2'

    # Test Method
    assert a.body[4].is_a[0].name == 'MethodDeclaration'
    assert a.body[4].jname[0] == 'm'



    # Test second method
    assert a.body[5].is_a[0].name == 'MethodDeclaration'
    assert a.body[5].jname[0] == 'm2'

    # Test Method statements
    assert a.body[5].body[0].is_a[0].name == 'IfStatement'
    assert a.body[5].body[1].is_a[0].name == 'BlockStatement'
    assert a.body[5].body[2].is_a[0].name == 'WhileStatement'
    # print(a.body[5].body[4].is_a[0].name)
    assert a.body[5].body[4].is_a[0].name == 'ReturnStatement'





# unit_tests()





