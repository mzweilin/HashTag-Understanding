from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals
from sumy.parsers.html import HtmlParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
from sumy.utils import cached_property
from sys import stderr
from sumy.models.dom._sentence import Sentence

# This is a hack so that we can summarize documents together, 
# as lexrank does not account for the origin of sentences, 
# just common words between them.
class DocumentCollection:
    def __init__(self):
        self.documents = []

    def add(self, document):
        self.documents.append(document)

    @cached_property
    def sentences(self):
        result = ()
        for doc in self.documents:
            try:
                result += cutoffSentences(doc.sentences)
            except UnicodeDecodeError: #covers problem in sumy library
                print("Problem with unicode encountered\n")
        return result

def getSentencesFrom(url):
    lang = "english"
    try:
        parser = HtmlParser.from_url(url, Tokenizer(lang))
    except:
        print("HTTP ERROR @ " + url)
    sentences = list(parser.document.sentences)
    sentences = map(unicode, sentences)
    return sentences

def cutoffSentences(sentences, threshold = 7):
    result = []
    tokenizer = Tokenizer("english")
    sentences = list(sentences)
    sentences = map(unicode, sentences)
    for sentence in sentences:
        if (len(sentence.split()) > threshold):
            result.append(Sentence(sentence, tokenizer))

    return tuple(result)

def summarize(urls, num_sentences):
    documents = DocumentCollection()
    lang = "english"
    summary = ""
   
    for url in urls:
        try:
            parser = HtmlParser.from_url(url, Tokenizer(lang))
            documents.add(parser.document)
        except: 
            print("HTTP ERROR @ " + url)
        
    stemmer = Stemmer(lang)
    summarizer = Summarizer(stemmer)
    summarizer.stop_words = get_stop_words(lang)
    for sentence in summarizer(documents, num_sentences):
        summary += unicode(sentence) + " "
    return summary

if __name__ == "__main__":
    urls = ["http://en.wikipedia.org/wiki/Automatic_summarization",
            "http://en.wikipedia.org/wiki/Abstract_%28summary%29"]
    print(summarize(urls, 10))
    #print(getSentencesFrom(urls[0]))
