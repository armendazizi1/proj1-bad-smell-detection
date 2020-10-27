import os
import sys
from owlready2 import *
import rdflib
import rdflib.plugins.sparql as sq
import javalang
import pytest
from rdflib import Literal

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
            } GROUP BY ?c
            HAVING (COUNT(?s) >= 20)
        """,
        initNs={"tree": "http://test.org/onto.owl#"})

    # for row in g.query(q):
    #     print(row.cn, "::", row.mn, "::", int(row.tot))
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

    # for row in g.query(q):
    #     print(row.cn, "::", row.mn, "::", int(row.tot))
    constructors = g.query(q)
    return constructors


def main():
    get_ontology("tree2.owl").load()
    g = rdflib.Graph()
    # findLongMethods(g)




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






# unit_tests()