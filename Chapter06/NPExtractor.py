import copy
# from abc import ABCMeta, abstractmethod

# 文字列をTokenに分解し、列挙する
class Tokenizer:
    def __init__(self, exp):
        self.exp = exp.replace('\n', '')
        self.curix = 0
        self.curr = ''
        self.prev = None
        self.gen = self.getTokens()

    def nextChar(self):
        if self.curix < len(self.exp):
            c = self.exp[self.curix]
            self.curix += 1
            return c
        return 0

    def getTokens(self):
        c = self.nextChar()
        token = ''
        while c != 0:
            if c == '(':
                yield c
            elif c == ')':
                if token != '':
                    yield token
                    token = ''
                yield c
            elif c == ' ':
                if token != '':
                    yield token
                    token = ''
            else:
                token += c
            c = self.nextChar()
        if token != '':
            yield token
        yield None

    def moveNext(self):
        if self.prev != None:
            r = copy.copy(self.prev)
            self.prev = None
            return r
        if self.curr != None:
            self.curr = next(self.gen)
        return self.curr

    # 一つ前に戻す （ただし連続しては呼び出せない)
    def movePrev(self):
        self.prev = self.curr

# Node.parseで利用するコンテキスストクラス
class Context:
    def __init__(self, exp):
        self.tokenizer = Tokenizer(exp)
        self.nplist = []

# 抽象クラス 具象クラス(NPExtractor, Sentence)
# class Node(metaclass=ABCMeta):
#     # 抽象メソッド
#     @abstractmethod
#     def parse(self, context, isNp):
#         pass

#<SExpression> :: ( <part>T <sentence> )
#<sentence> :: <word> | { ( <part> <sentence> ) }
#<part> :: ROOT | S | NP | VP | PP | ....

# <SExpression>を表すクラス
class NPExtractor:
    def parse(self, context):
        curr = context.tokenizer.moveNext()
        if curr == '(':
            # <part>を取り出す 取り出したpartは使わない
            context.tokenizer.moveNext()
            # <sentense>のパース
            node = Sentence()
            node.parse(context, False)
            # ) を取り出す
            curr = context.tokenizer.moveNext()
            if curr != ')':
                raise Exception
        else:
            raise Exception
        return ''

# <sentence>を表すクラス
class Sentence:
    def parse(self, context, isNp):
        phrase = []
        # 先読みする
        curr = context.tokenizer.moveNext()
        if curr != '(':
            # <word>の処理 読み取った単語を返す
            return curr
        # { ( <part> <sentence> )  の処理
        while curr == '(':
            # <part>を取り出す
            part = context.tokenizer.moveNext()
            # <sentense>のパース
            node = Sentence()
            w = node.parse(context, part == 'NP')
            # 現在の () の中の句はphraseに追加
            # ∵ (NP (JJ Many) (NNS challenges)) の Many challenges を記録する必要があるから
            phrase.append(w)
            if part == 'NP' and w != '':
                # 名詞句ならば、nplistにも記憶する
                # このpart が  (NP (JJ Many) (NNS challenges)) の NPならば、
                # w には、'Many challenges' が入っている
                context.nplist.append(w)
            # ) の処理
            curr = context.tokenizer.moveNext()
            if curr != ')':
                raise Exception
            # 次を取り出す
            curr = context.tokenizer.moveNext()
        # 先読みした分を戻す
        context.tokenizer.movePrev()
        if isNp:
            # parseが呼び出された時点で処理しているものがNPならば、phraseにある単語を連結し文字列化する
            # 先頭と最後の不要なものを取り除く かなり使わ伎だが...
            while phrase and (phrase[-1] == ',' or phrase[-1] == '' or phrase[-1] == '.'):
                phrase.pop()
            while phrase and (phrase[0] == ',' or phrase[0] == '' or phrase[0] == '.'):
                phrase.pop(0)
            return ' '.join(phrase)
        return ''
