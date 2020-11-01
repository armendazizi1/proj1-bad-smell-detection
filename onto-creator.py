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
                        # print(x.id)
                        # print(onto[x.id])
                        types.new_class(node.name, (onto[x.id],))
            elif (type(node) == ast.Assign):
                for value in node.value.elts:
                    # print(value.s)
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



main()

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



