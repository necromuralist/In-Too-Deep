# from python
from argparse import Namespace

import os
import re
import string

# pypi
import attr

Environment = Namespace(
    training_corpus="WALL_STREET_JOURNAL_POS",
    vocabulary="WALL_STREET_JOURNAL_VOCABULARY",
    test_corpus= "WALL_STREET_JOURNAL_TEST_POS",
    test_words="WALL_STREET_JOURNAL_TEST_WORDS",
)

Suffixes = Namespace(
    noun = ["action", "age", "ance", "cy", "dom", "ee", "ence", "er", "hood",
            "ion", "ism", "ist", "ity", "ling", "ment", "ness", "or", "ry",
            "scape", "ship", "ty"],
    verb = ["ate", "ify", "ise", "ize"],
    adjective = ["able", "ese", "ful", "i", "ian", "ible", "ic", "ish", "ive",
                 "less", "ly", "ous"],
    adverb = ["ward", "wards", "wise"]
)

UNKNOWN = "--unknown-{}--"
Label = Namespace(
    digit=UNKNOWN.format("digit"),
    punctuation=UNKNOWN.format("punctuation"),
    uppercase=UNKNOWN.format("uppercase"),
    noun=UNKNOWN.format("noun"),    
    verb=UNKNOWN.format("verb"),
    adjective=UNKNOWN.format("adjective"),
    adverb=UNKNOWN.format("adverb"),
    unknown="--unknown--",
 )

Unknown = Namespace(
    punctuation = set(string.punctuation),
    suffix = Suffixes,
    label=Label,
    has_digit=re.compile(r"\d"),
    has_uppercase=re.compile("[A-Z]")
)

Empty = Namespace(
    word="--n--",
    tag="--s--",
)


@attr.s(auto_attribs=True)
class CorpusProcessor:
    """Pre-processes the corpus

    Args:
     vocabulary: holder of our known words
    """
    vocabulary: dict

    def split_tuples(self, lines: list):
        """Generates tuples
    
        Args:
         lines: iterable of lines from the corpus
    
        Yields:
         whitespace split of line
        """
        for line in lines:
            yield line.split()
        return

    def handle_empty(self, tuples: list):
        """checks for empty strings
    
        Args:
         tuples: tuples of corpus lines
    
        Yields:
         line with empty string marked
        """
        for line in tuples:
            if not line:
                yield Empty.word, Empty.tag
            else:
                yield line
        return

    def label_unknowns(self, tuples: list) -> str:
        """
        Assign tokens to unknown words
    
        Args:
         tuples: word, tag tuples
    
        Yields:
         word or label for the word if unknown, tag
        """
        for word, tag in tuples:
            if word in self.vocabulary:
                yield word, tag
                
            elif Unknown.has_digit.search(word):
                yield Unknown.label.digit, tag
        
            elif not Unknown.punctuation.isdisjoint(set(word)):
                yield Unknown.label.punctuation, tag
        
            elif Unknown.has_uppercase.search(word):
                yield Unknown.label.uppercase, tag
        
            elif any(word.endswith(suffix) for suffix in Unknown.suffix.noun):
                yield Unknown.label.noun, tag
        
            elif any(word.endswith(suffix) for suffix in Unknown.suffix.verb):
                yield Unknown.label.verb, tag
        
            elif any(word.endswith(suffix) for suffix in Unknown.suffix.adjective):
                yield Unknown.label.adjective, tag
        
            elif any(word.endswith(suffix) for suffix in Unknown.suffix.adverb):
                yield Unknown.label.adverb, tag
            else:
                yield Unknown.label.unknown, tag
        return

    def __call__(self, tuples: list) -> list:
        """preprocesses the words and tags
    
        Args:
         tuples: list of words and tags to process
        
        Returns:
         preprocessed version of words, tags
        """
        processed = self.split_tuples(tuples)
        processed = self.handle_empty(processed)
        processed = [word for word in self.label_unknowns(processed)]
        return processed


@attr.s(auto_attribs=True)
class DataPreprocessor:
    """A pre-processor for the data

    Args:
     vocabulary: holder of our known words
     empty_token: what to use if a line is an empty string
    """
    vocabulary: dict

    def handle_empty(self, words: list):
        """replace empty strings withh empty_token
    
        Args:
         words: list to process
         empty_token: what to replace empty strings with
    
        Yields:
         processed words
        """
        for word in words:
            if not word.strip():
                yield Empty.word
            else:
                yield word
        return

    def label_unknowns(self, words: list) -> str:
        """
        Assign tokens to unknown words
    
        Args:
         words: iterable of words to check
    
        Yields:
         word or label for the word if unknown
        """
        for word in words:
            if word in self.vocabulary:
                yield word
                
            elif Unknown.has_digit.search(word):
                yield Unknown.label.digit
        
            elif not Unknown.punctuation.isdisjoint(set(word)):
                yield Unknown.label.punctuation
        
            elif Unknown.has_uppercase.search(word):
                yield Unknown.label.uppercase
        
            elif any(word.endswith(suffix) for suffix in Unknown.suffix.noun):
                yield Unknown.label.noun
        
            elif any(word.endswith(suffix) for suffix in Unknown.suffix.verb):
                yield Unknown.label.verb
        
            elif any(word.endswith(suffix) for suffix in Unknown.suffix.adjective):
                yield Unknown.label.adjective
        
            elif any(word.endswith(suffix) for suffix in Unknown.suffix.adverb):
                yield Unknown.label.adverb
            else:
                yield Unknown.label.unknown
        return

    def __call__(self, words: list) -> list:
        """preprocesses the words
    
        Args:
         words: list of words to process
        
        Returns:
         preprocessed version of words
        """
        processed = (word.strip() for word in words)
        processed = self.handle_empty(processed)
        processed = [word for word in self.label_unknowns(processed)]
        return processed



@attr.s(auto_attribs=True)
class DataLoader:
    """Loads the traning and test data

    Args:
     environment: namespace with keys for the environment to load paths
    """
    environment: Namespace=Environment
    _preprocess: DataPreprocessor=None
    _vocabulary_words: list=None
    _vocabulary: dict=None
    _training_corpus: list=None
    _processed_training: list=None
    _test_corpus: list=None
    _test_words: list=None

    @property
    def preprocess(self) -> DataPreprocessor:
        """The Preprocessor for the data"""
        if self._preprocess is None:
            self._preprocess = DataPreprocessor(self.vocabulary)
        return self._preprocess

    @property
    def vocabulary_words(self) -> list:
        """The list of vocabulary words for tranining"""
        if self._vocabulary_words is None:
            self._vocabulary_words = sorted(
                self.load(os.environ[self.environment.vocabulary]))
        return self._vocabulary_words

    @property
    def training_corpus(self) -> list:
        """The corpus  for tranining"""
        if self._training_corpus is None:
            self._training_corpus = self.load(os.environ[self.environment.training_corpus])
        return self._training_corpus

    @property
    def processed_training(self) -> list:
        """Pre-processes the training corpus"""
        if self._processed_training is None:
            processor = CorpusProcessor(self.vocabulary)
            self._processed_training = processor(self.training_corpus)
        return self._processed_training

    @property
    def vocabulary(self) -> dict:
        """Converts the vocabulary list of words to a dict
    
        Returns:
         word to index of word in vocabulary words
        """
        if self._vocabulary is None:
            self._vocabulary = {
                word: index
                for index, word in enumerate(self.vocabulary_words)}
        return self._vocabulary

    @property
    def test_corpus(self) -> list:
        """The corpus  for tranining"""
        if self._test_corpus is None:
            self._test_corpus = self.load(os.environ[self.environment.test_corpus])
        return self._test_corpus

    @property
    def test_words(self) -> list:
        """The pre-processed test words"""
        if self._test_words is None:
            self._test_words = self.load(os.environ[self.environment.test_words])
            self._test_words = self.preprocess(self._test_words)
        return self._test_words

    def load(self, path: str) -> list:
        """Loads the strings from the file
    
        Args:
         path: path to the text file
    
        Returns:
         list of lines from the file
        """
        with open(path) as reader:
            lines = reader.read().split("\n")
        return lines
