import ast
from owlready2 import *
import types
import pytest

onto = get_ontology("http://test.org/onto.owl")


class AstVisitor(ast.NodeVisitor):

    def generic_visit(self, node):
        super().generic_visit(node)

        with onto:
            if (type(node) == ast.ClassDef):
                for x in node.bases:
                    if (x.id == 'Node'):
                        types.new_class(node.name, (Thing,))
                    else:
                        types.new_class(node.name, (onto[x.id],))
            elif (type(node) == ast.Assign):
                for value in node.value.elts:
                    if (value.s in ['parameters', 'body']):
                        types.new_class(value.s, (ObjectProperty,))
                    else:
                        if value.s == 'name':
                            types.new_class('jname', (DataProperty,))
                        else:
                            types.new_class(value.s, (DataProperty,))


def main():
    file = open("./tree.py", 'r').read()
    astree = ast.parse(file);
    AstVisitor().generic_visit(astree)
    onto.save('./tree.owl', format="rdfxml")


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


def test_unit(setup_ontology):
    onto = setup_ontology
    cd = onto["ClassDeclaration"]

    assert cd.name == "ClassDeclaration"
    assert len(cd.is_a) == 1
    assert cd.is_a[0].name == 'TypeDeclaration'


def test_constructorDeclaration(setup_ontology):
    onto = setup_ontology
    cd = onto["ConstructorDeclaration"]

    assert cd.name == "ConstructorDeclaration"
    assert len(cd.is_a) == 2
    assert cd.is_a[0].name == 'Declaration'
    assert cd.is_a[1].name == 'Documented'


def test_methodDeclaration(setup_ontology):
    onto = setup_ontology
    cd = onto["MethodDeclaration"]

    assert cd.name == "MethodDeclaration"
    assert len(cd.is_a) == 2
    assert cd.is_a[1].name == 'Declaration'
    assert cd.is_a[0].name == 'Member'


def test_fieldDeclaration(setup_ontology):
    onto = setup_ontology
    cd = onto["FieldDeclaration"]

    assert cd.name == "FieldDeclaration"
    assert len(cd.is_a) == 2
    assert cd.is_a[1].name == 'Declaration'
    assert cd.is_a[0].name == 'Member'


def test_fieldDeclaration(setup_ontology):
    onto = setup_ontology
    cd = onto["Statement"]

    assert cd.name == "Statement"
    assert len(cd.is_a) == 1
    assert cd.is_a[0].name == 'Thing'


def test_whileStatement(setup_ontology):
    onto = setup_ontology
    cd = onto["WhileStatement"]

    assert cd.name == "WhileStatement"
    assert len(cd.is_a) == 1
    assert cd.is_a[0].name == 'Statement'


def test_formalParamter(setup_ontology):
    onto = setup_ontology
    cd = onto["FormalParameter"]

    assert cd.name == "FormalParameter"
    assert len(cd.is_a) == 1
    assert cd.is_a[0].name == 'Declaration'


def test_ifStatement(setup_ontology):
    onto = setup_ontology
    cd = onto["IfStatement"]

    assert cd.name == "IfStatement"
    assert len(cd.is_a) == 1
    assert cd.is_a[0].name == 'Statement'


def test_switchStatement(setup_ontology):
    onto = setup_ontology
    cd = onto["SwitchStatement"]

    assert cd.name == "SwitchStatement"
    assert len(cd.is_a) == 1
    assert cd.is_a[0].name == 'Statement'


def test_parameter(setup_ontology):
    onto = setup_ontology
    cd = onto["parameter"]

    assert cd.name == "parameter"
    assert len(cd.is_a) == 1
    assert cd.is_a[0].name == 'DatatypeProperty'


def test_arguments(setup_ontology):
    onto = setup_ontology
    cd = onto["arguments"]

    assert cd.name == "arguments"
    assert len(cd.is_a) == 1
    assert cd.is_a[0].name == 'DatatypeProperty'


def test_throws(setup_ontology):
    onto = setup_ontology
    cd = onto["throws"]

    assert cd.name == "throws"
    assert len(cd.is_a) == 1
    assert cd.is_a[0].name == 'DatatypeProperty'
