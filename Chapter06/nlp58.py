from xml.etree import ElementTree

class Dependency:
    def __init__(self, dep):
        self.type = dep.attrib['type']
        self.governor_ix = dep.find('governor').attrib['idx']
        self.governor_text = dep.find('governor').text
        self.dependent_ix = dep.find('dependent').attrib['idx']
        self.dependent_text = dep.find('dependent').text

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
        return deps

    def enumDependencies(self):
        dependencies = self.sentences.findall('sentence/dependencies[@type="collapsed-dependencies"]')
        for deps in dependencies:
            yield deps

    @staticmethod
    def toDependencyList(deps):
        lst = []
        for dep in deps:
            lst.append(Dependency(dep))
        return lst


    def extractSVO(self, lst):
        subjs = self.findSubj(lst)
        for subj in subjs:
            objs = self.finObjs(lst, subj)
            for obj in objs:
                yield (subj.dependent_text, subj.governor_text, obj.dependent_text)

    @staticmethod
    def findSubj(lst):
        # subjの親が述語の可能性があるので、それを列挙
        return filter(lambda x: x.type == 'nsubj', lst)

    @staticmethod
    def finObjs(lst, subj):
        # subjと同じ親を持つノードを探す
        filterd = filter(lambda x: x.governor_ix == subj.governor_ix, lst)
        # その中からtypeが、dobjのものだけを取り出す
        return filter(lambda x: x.type == 'dobj', filterd)


    # @staticmethod
    # def toGraph(dot, filepath):
    #     os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'

    #     graph = pydot.Dot(graph_type='digraph')
    #     graph.set_node_defaults(fontname='Meiryo UI', fontsize='10')

    #     for s, t in dot:
    #         graph.add_edge(pydot.Edge(s, t))
    #     graph.write_png(filepath)

def main():
    cd = CollapsedDependencies('nlp.txt.xml')
    sentenceId = 1
    with open('result58.txt', 'w', encoding='utf8') as w:
        for deps in cd.enumDependencies():
            nodes = cd.toDependencyList(deps)
            print(sentenceId)
            for s, v, o in cd.extractSVO(nodes):
                w.write('{}\t{}\t{}\n'.format(s, v, o))
            sentenceId += 1

    # このコメントアウトしてあるコードは、sentenceIdを指定して１文だけを処理するコード
    # sentenceId = 5
    # deps = cd.getDependence(sentenceId)
    # nodes = cd.toNodeList(deps)
    # print(sentenceId)
    # for s, v, o in cd.extractSVO(nodes):
    #     print(s.governor_text, v.governor_text, o.governor_text)
    # sentenceId += 1

if __name__ == '__main__':
    main()
