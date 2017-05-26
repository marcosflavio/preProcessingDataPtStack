#Classe desenvolvida por Gustavo Aires, retirada do Framework senttex
#https://github.com/gustavoaires/senttext
import re
import nltk
from nltk import RegexpParser
from nltk.corpus import stopwords
from nltk.tokenize.regexp import WhitespaceTokenizer

global corpus, sent_tags, tagger

# corpus = TaggedCorpusReader('/root/adail/python/names',r'.*\.txt',word_tokenizer=PunktWordTokenizer(),sep="_") PATH no linux
# corpus = TaggedCorpusReader('C:/Users/jose.adail/workspace/TextProcessor/names', r'.*\.txt', word_tokenizer=WhitespaceTokenizer(), sep="_")
# name_tags = corpus.tagged_sents()  # Recebe as senten�as marcadas com POS_Tags.
# tagger = UnigramTagger(name_tags)  # UnigramTagger � treinado com essas senten�as marcadas que o s�o repassadas.


class RegexpReplacer(object):
    def __init__(self):
        self.replacement_patterns = [(r'rs[rs]+', 'rs'), (r'ha[ha]+', 'haha'), (r's[s]+', 'sxs'), (r'r[r]+', 'rxr'), (r'k[k]+', 'kxkxk'), (r'a[a]+', 'aqa'), (r'e[e]+', 'eqe'),
                                     (r'o[o]+', 'oqo'), (r'sdds', 'saudade'), (r'sdd', 'saudade'), (r':d', 'feliz'), (r'<3', 'love'), (r':3', 'feliz'), (r';d', 'feliz'),
                                     (r':p', 'feliz'), (r':\)*', 'feliz'), (r'o\/', 'feliz'), (r'\\o\/', 'feliz'), (r'\\o', 'feliz'), (r'\*\_*\*', 'feliz'),
                                     (r'\*-*\*', 'feliz'), (r'\*o*\*', 'feliz'), (r'\>.\<', 'feliz'), (r":'\(*", 'triste'),
                                     (r':\(*', 'triste'), (r':o*', 'uau'), (r'=o*', 'uau'), (r':v', 'feliz'), (r';\)*', 'feliz'), (r'd\+', 'demais'), (r'[\W\d\_]', ' ')]
    # Para cada emoticon e outras express�es mapeadas nas regex encontradas em replacement_patterns,
    # realizar substitui��o.
    def replaceEmoticon(self, text):
        for r, s in self.replacement_patterns:
            text = re.sub(r, s, text)
            return text


class TextCleaner(object):
    def __init__(self):
        self.repeat_regexp = re.compile(r'(\w*)(\w)\2(\w*)')
        self.repl = r'\1\2\3'
        self.pt_stemmer = nltk.stem.RSLPStemmer()
        self.tokenizer = WhitespaceTokenizer()
        self.cached_stopwords = stopwords.words('portuguese')
        self.symbols = [u"\"", u"'", u"!", u"?", u".", u",", u";", u">", u"_", u"<", u"-", u"[",
                        u"]", u"{", u"}", u"/", u"\\", u"^", u"~", u"�",  u"`", u"``", u"\u2026",
                        u":", u"(", u")", u"|", u"#", u"$", u"%", u"&", u"*", u"=", u"+", u"\u2013",
                        u"\u201c", u"\u201d", u"\u300b\u300b", u"\u2019", u"\u2018", u"\u00b0",
                        u"\u00ba", u"\u200b", u"\u00b7", u"\u2014", u"\u00bb", u"\u221a", u"\u00aa",
                        u"\ufe0f", u"\u2794", u"\u2192", u"\u00a8", u"\u2022", u"\u300a", u"\u00bf",
                        u"\u25a0", u"\u00af", u"\u22b3", u"\u2060", u"\u261b", u"\u00ad", u"\u00ab"]
        self.more_stopwords = ['ja', 'q', 'd', 'ai', 'desse', 'dessa', 'disso', 'nesse', 'nessa', 'nisso', 'esse', 'essa', 'isso', 'so', 'mt', 'vc', 'voce', 'ne', 'ta', 'to', 'pq',
                               'cade', 'kd', 'la', 'e', 'eh', 'dai', 'pra', 'vai', 'olha', 'pois', 'rt', 'retweeted',
                               'fica', 'muito', 'muita', 'muitos', 'muitas', 'onde', 'mim', 'oi', 'ola', 'ate']
        self.unicode_replace = [(u'�', u'a'), (u'�', u'a'), (u'�', u'a'), (u'�', u'a'), (u'�', u'e'), (u'�', u'e'),
                                (u'�', u'e'), (u'�', u'i'), (u'�', u'o'), (u'�', u'o'), (u'�', u'o'), (u'�', u'o'),
                                (u'�', u'u'), (u'�', u'u'), (u'�', u'c'), (u'�', u'a'), (u'�', u'e'), (u'�', u'i'),
                                (u'�', u'u'), (u'�', u'a'), (u'�', u'a'), (u'�', u'a'), (u'�', u'a'), (u'�', u'e'),
                                (u'�', u'e'), (u'�', u'e'), (u'�', u'i'), (u'�', u'o'), (u'�', u'o'), (u'�', u'o'),
                                (u'�', u'o'), (u'�', u'o'), (u'�', u'o'), (u'�', u'u'), (u'�', u'c'), (u'�', u'n'), (u'�', u'n')]
        self.link_patterns = [('http'), ('www'), ('w3c')]
        self.normal = [(r'kxkxk', 'kkk'), (r'nao ', ' nao_'), (r' ir ', '_ir '), (r'bom demal', ' bomdemais '), (r'\s*insan\s*', ' insano '), (r'\s*saudad\s*', ' saudade ')]
        self.digraph = [(r'rxr', 'rr'), (r'sxs', 'ss'), (r'aqa', 'aa'), (r'eqe', 'ee'), (r'oqo', 'oo')]

    # Remover caracteres repetidos seguidamente, para que o modelo n�o seja prejudicado
    # por falta de padr�o na escrita.
    def removeRepChar(self, word):
        repl_word = self.repeat_regexp.sub(self.repl, word)
        if repl_word != word:
            return self.removeRepChar(repl_word)
        else:
            return repl_word

    # Remover caracteres especiais (Ex: ?, !, " ...).
    def removeSymbols(self, text):
        for symbol in self.symbols:
            text = text.replace(symbol, ' ')
        return text

    # Remover sufixo das palavras da lingua portuguesa.
    def removeSufPort(self, para):
        para = para.split()
        text = ''
        for w in para:
            text = text + self.pt_stemmer.stem(w) + ' '
        return text

    # Substituir caracateres acentuados por caracteres sem acentos.
    def removeAccent(self, text):
        para = text
        for (lat, asc) in self.unicode_replace:
            para = para.replace(lat, asc)
        return para

    # Remover stopwords dos textos.
    def removeStopwords(self, text):
        text = ' '.join([word for word in text.split() if word not in self.cached_stopwords])
        text = ' '.join([word for word in text.split() if word not in self.more_stopwords])
        return text

    # Remover links dos textos.
    def removeLinks(self, text):
        for l in self.link_patterns:
            text = text.split(l, 1)[0]
        return text

    # Reescrever os digrafos na sua forma original. Exemplo: rxr -> rr
    def normalizeDigraph(self, text):
        for a, d in self.digraph:
            text = re.sub(a, d, text)
        return text

    # Reescrever algumas palavras para dar melhor sem�ntica e legibilidade aos resultados do modelo.
    def normalizeText(self, text):
        for a, b in self.normal:
            text = re.sub(a, b, text)
        return text

    def removeOneCharacter(self, text):
        text = self.tokenizeWords(text)
        for i in range(len(text)):
            if len(text[i]) <= 2:
                text[i] = ''
        return ' '.join(text)

    def tokenizeWords(self, text):
        text = self.tokenizer.tokenize(text)
        return text


class NamedEntity(object):
    def __init__(self):
        self.tokenizer = WhitespaceTokenizer()

    # Remover do texto duas ou mais palavras pr�prias em sequ�ncia.
    def removeName(self, text):
        i = 0
        j = 1
        words = text.split()
        lim = len(words) - 1
        while j <= lim:
            if not words[i].isupper() and not words[i].islower():
                if not words[j].isupper() and not words[j].islower():
                    words[i] = words[i].replace(words[i], "")
                    words[j] = words[j].replace(words[j], "")
                    i += 1
                    j += 1
            words = ' '.join(words)
        return words

    # Remover nomes pr�prios dos textos. Para isso, recebe o texto, que em seguida � dividido em palavras,
    #  que posteriormente recebem POS_Tags.
    # Para cada palavra/tag, � verificado se a tag nao corresponde a de nome proprio 'NPROP'.
    # Ao final, forma-se um texto sem palavras com tags
    # 'NPROP', sendo assim retornado pelo m�todo.
    def removePersonName(self, text):
        final_text = ''
        tokenized_text = self.tokenizeWords(text)
        tagged_text = self.tagWords(tokenized_text)
        for w, t in tagged_text:
            if t != "NPROP":
                final_text = final_text + ''.join(w) + ' '
        return final_text

    # Remover men��es de usu�rios de tweets. Os mesmos s�o identificados pelo caractere '@'.
    # O texto original � repassado ao m�todo e divido em palavras,
    # em seguida. Ap�s isso, � verificado para cada palavra do texto se a mesma se inicia com o caractere '@'.
    # Caso sim, essa palavra � removida do texto.
    # Ao final, o texto � retornado, sem os nomes de usu�rios.
    def removeTwitterUsername(self, text):
        text = text.split()
        for w in text:
            if w[0] == '@':
                text.remove(w)
        return ' '.join(text)

    # Marcar as palavras de uma senten�a tokenizada com POS_Tags.
    # O texto � repassado ao m�todo tag da classe UnigramTagger, que marca as palavras do texto com
    # POS_Tags. Retorna uma lista com palavras/tags.
    def tagWords(self, tokenized_text):
        tagged_words = tagger.tag(tokenized_text)
        return tagged_words

    # Desenhar arvore que destaca um determinado padr�o gramatical do texto.
    def drawNamedEntityTree(self, text):
        tokenized_text = self.tokenizer.tokenize(text)
        tagged_text = self.tagWords(tokenized_text)
        grammar = "ENT: {<PESSOA>*}"
        cp = RegexpParser(grammar)
        res = cp.parse(tagged_text)
        res.draw()

    # Tokenizar senten�as em palavras. Retorna uma lista com as palavras que formam o texto.
    def tokenizeWords(self, text):
        text = self.tokenizer.tokenize(text)
        return text