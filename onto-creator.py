import ast
from owlready2 import *
import types

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
                    if (value.s in ['parameter', 'body']):
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
