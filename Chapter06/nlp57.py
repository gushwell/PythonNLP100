from xml.etree import ElementTree
import os
import pydot_ng as pydot

class CollapsedDependencies:
    def __init__(self, filepath):
        xdoc = ElementTree.parse(filepath)
        root = xdoc.getroot()
        self.sentences = root.find('document/sentences')
        self.coreference = root.find('document/coreference')

    def enumCoreference(self):
        for e in self.coreference:
            yield e

    @staticmethod
    def toDot(deps):
        edges = []
        for dep in deps:
            governor = dep.find('governor')
            dependent = dep.find('dependent')
            if dependent.text != '.' and dependent.text != ',':
                edges.append((governor.text, dependent.text))
        return edges

    def getDependence(self, sentenceId):
        strid = str(sentenceId)
        sentences = self.sentences.find("sentence[@id='" + strid + "']")
        deps = sentences.find('dependencies[@type="collapsed-dependencies"]')
        return self.toDot(deps)

    def enumDependencies(self):
        dependencies = self.sentences.findall('sentence/dependencies[@type="collapsed-dependencies"]')
        for deps in dependencies:
            yield self.toDot(deps)

    @staticmethod
    def toGraph(dot, filepath):
        #os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'

        graph = pydot.Dot(graph_type='digraph')
        graph.set_node_defaults(fontname='Meiryo UI', fontsize='10')

        for s, t in dot:
            graph.add_edge(pydot.Edge(s, t))
        graph.write_png(filepath)

def main():
    cd = CollapsedDependencies('nlp.txt.xml')
    # sentenceId = 1
    # for dot in cd.enumDependencies():
    #     cd.toGraph(dot, "g57_{}.png".format(sentenceId))
    #     sentenceId += 1

    # このコメントアウトしてあるコードは、sentenceIdを指定して１文だけを処理するコード
    sentenceId = 7
    dot = cd.getDependence(sentenceId)
    cd.toGraph(dot, "ag57_{}.png".format(sentenceId))

if __name__ == '__main__':
    main()
