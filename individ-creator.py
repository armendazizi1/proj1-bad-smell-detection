import javalang
import sys
from owlready2 import *
import os



def populateOntology(onto, tree):
    for path, node in tree.filter(javalang.tree.ClassDeclaration):
        # print(node.body)
        cd = onto["ClassDeclaration"]()
        cd.jname = [node.name]

        for _, fields in tree.filter(javalang.tree.FieldDeclaration):
            for field in fields.declarators:
                fd = onto['FieldDeclaration']()
                # print(field.name)
                fd.jname = [field.name]
                cd.body.append(fd)

        for _, constructor in tree.filter(javalang.tree.ConstructorDeclaration):
            cod = onto['ConstructorDeclaration']()
            cod.jname = [constructor.name]
            cd.body.append(cod)

        for _, method in tree.filter(javalang.tree.MethodDeclaration):
            md = onto['MethodDeclaration']()
            md.jname = [method.name]
            cd.body.append(md)



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

# def unit_tests():
#     onto2 = get_ontology("tree3.owl").load()
#     tree = javalang.parse.parse("class A { int x, y; }")
#     populateOntology(onto2, tree)
#     a = onto2['ClassDeclaration'].instances()[0]
#     assert a.body[0].is_a[0].name == 'FieldDeclaration'
#     assert a.body[0].jname[0] == 'x'
#     assert a.body[1].is_a[0].name == 'FieldDeclaration'
#     assert a.body[1].jname[0] == 'y'
#
# unit_tests()








