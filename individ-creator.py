import javalang
import sys
from owlready2 import *
import os



def populateOntology(onto, tree):
    for path, node in tree.filter(javalang.tree.ClassDeclaration):
        # print(node.body)
        cd = onto["ClassDeclaration"]()
        cd.jname = [node.name]

        # for _, fields in tree.filter(javalang.tree.FieldDeclaration):
        #     for field in fields.declarators:
        #         fd = onto['FieldDeclaration']()
        #         # print(field.name)
        #         fd.jname = [field.name]
        #         cd.body.append(fd)
        #
        # for _, constructor in tree.filter(javalang.tree.ConstructorDeclaration):
        #     cod = onto['ConstructorDeclaration']()
        #     cod.jname = [constructor.name]
        #     cd.body.append(cod)
        #
        # for _, method in tree.filter(javalang.tree.MethodDeclaration):
        #     md = onto['MethodDeclaration']()
        #     md.jname = [method.name]
        #     cd.body.append(md)

        # Got help from Gregory Wullimann here with his idea to populate the ontology in order.
        for member in node.body:
            if (type(member)== javalang.tree.FieldDeclaration):
                for field in member.declarators:
                    fd = onto['FieldDeclaration']()
                    print(field.name)
                    fd.jname = [field.name]
                    cd.body.append(fd)
            elif (type(member)== javalang.tree.ConstructorDeclaration):
                cod = onto['ConstructorDeclaration']()
                cod.jname = [member.name]
                cd.body.append(cod)
            elif (type(member) == javalang.tree.MethodDeclaration):
                md = onto['MethodDeclaration']()
                md.jname = [member.name]
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


# main()

def unit_tests():
    onto = get_ontology("tree.owl").load()
    tree = javalang.parse.parse("class A { int x, y; public A(){} public A(int a, int b){} void m(){} void m2(){} int z;}")
    populateOntology(onto, tree)
    a = onto['ClassDeclaration'].instances()[0]

    # Test Fields
    assert a.body[0].is_a[0].name == 'FieldDeclaration'
    assert a.body[0].jname[0] == 'x'
    assert a.body[1].is_a[0].name == 'FieldDeclaration'
    assert a.body[1].jname[0] == 'y'


    # Test Constructor
    assert a.body[2].is_a[0].name == 'ConstructorDeclaration'
    assert a.body[2].jname[0] == 'A'
    assert a.body[3].is_a[0].name == 'ConstructorDeclaration'
    assert a.body[3].jname[0] == 'A'


    # Test Method
    assert a.body[4].is_a[0].name == 'MethodDeclaration'
    assert a.body[4].jname[0] == 'm'



    # Test method and field order
    assert a.body[5].is_a[0].name == 'MethodDeclaration'
    assert a.body[5].jname[0] == 'm2'
    assert a.body[6].is_a[0].name == 'FieldDeclaration'
    assert a.body[6].jname[0] == 'z'



unit_tests()








