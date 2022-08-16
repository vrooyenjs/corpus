# Student Number: 5767 661 5
# Author: Jan van Rooyen
#
# Purpose: Contains functions use in the natural language processing assignments.
#
import operator

#
# Global variables used by multiple functions
#
n_gram_frequency = {}
n_gram_frequency_frequency = {}
corpus_length = 0


# Function used to read corpus into memory
#
# Parameter: corpus_library - The name of the file containing the text to be used.
# Returns: corpus - A list of all sentences contained within in the given corpus library.
#
def parse_corpus(corpus_library):
    # Open corpus file
    corpus_file = open(file="corpus/" + corpus_library, mode="r", encoding="UTF-8")
    # Read all data from file.
    corpus = corpus_file.readlines()
    corpus_file.close()
    return corpus
# end parse_corpus(corpus_library)


# Function used to cut up any given phrase into a n-gram of size n
#
# Parameter: phrase - Phrase to cut into n-grams
# Parameter: n - Size of n-gram, 1=unigram, 2=bigram
# Returns a list of word lists of size n
#
def create_n_gram(phrase, n):
    # If this is a bigram or larger, we ensure that we have the start and end tokens on the phrase
    if n > 1:
        phrase = '<s> ' + phrase + ' </s>'
    words = phrase.split()
    n_gram = []
    for min_index in range(0, len(words)):
        max_index = min_index + n
        if min_index + n > len(words):
            break
        gram = []
        for index in range(min_index, max_index):
            gram.append(words[index])
        n_gram.append(gram)
    return n_gram
# end create_n_gram (phrase, n)


# Function used to calculate the number of words in the given corpus and create a dictionary
# containing the frequency of unigram and bigrams in the provided corpus. Function also calculates the
# frequency of frequencies for good-turing smoothing.
#
# Parameter: corpus - list of sentences
#
def compute_n_gram_frequencies (corpus):
    global n_gram_frequency, n_gram_frequency_frequency, corpus_length

    tokenized_corpus = []
    for sentence in corpus:
        tokenized_corpus.extend(sentence.split())
    corpus_length = len(tokenized_corpus)

    # Get a count of all the words in the vacabulary
    for sentence in corpus:
        # unigram
        for word in sentence.split():
            if word in n_gram_frequency:
                n_gram_frequency[word] = n_gram_frequency[word] + 1
            else:
                n_gram_frequency[word] = 1

        # bigram
        for bigram in create_n_gram(sentence, 2):
            bigram = ' '.join(bigram)
            if bigram in n_gram_frequency:
                n_gram_frequency[bigram] = n_gram_frequency[bigram] + 1
            else:
                n_gram_frequency[bigram] = 1


    # Find the number of words that have only one instance.
    n_1 = 0
    for value in n_gram_frequency.values():
        if value in n_gram_frequency_frequency:
            n_gram_frequency_frequency[value] = n_gram_frequency_frequency[value] + 1
        else:
            n_gram_frequency_frequency[value] = 1

    highest_freq_of_freq = max(n_gram_frequency_frequency.items(), key=operator.itemgetter(1))[1]
    for index in range (1, highest_freq_of_freq + 1):
        # If we find that the value is not populate it, we calculate it
        if index not in n_gram_frequency_frequency or n_gram_frequency_frequency[index] == 0:
            if index == highest_freq_of_freq + 1:
                q = index - 3
                r = index
                t = index - 1

                N_q = n_gram_frequency_frequency[q]
                N_r = n_gram_frequency_frequency[r]
                N_t = n_gram_frequency_frequency[t]

                Z_r = N_r / (0.5 * (r - q))
                # print('%d = %d / (0.5 * (%d - %d))' % (Z_r, N_r, t, q))
                n_gram_frequency_frequency[index] = Z_r
            else:
                q = index - 3
                r = index - 2
                t = index - 1

                # N_q = word_frequency_frequency[q]
                N_r = n_gram_frequency_frequency[r]
                # N_t = word_frequency_frequency[t]

                Z_r = N_r / (0.5 * (t - q))
                # print('%d = %d / (0.5 * (%d - %d))' % (Z_r, N_r, t, q))
                n_gram_frequency_frequency[index] = Z_r
    return n_gram_frequency_frequency
# end compute_n_gram_frequencies (corpus)


# Function used to calculate the top_n unigrams with highest frequency in the corpus.
#
# Parameter: corpus - list of sentences
# Parameter: top_n - the top 'int' number of unigrams to print, including their frequencies.
def find_most_common_unigrams_in_corpus(corpus, top_n):
    # Load corpus into memory
    corpus = parse_corpus(corpus)
    tokenized_corpus = []
    for sentence in corpus:
        tokenized_corpus.extend(sentence.split())

    word_count = {}
    for word in tokenized_corpus:
        if word in word_count:
            word_count[word] = word_count[word] + 1
        else:
            word_count[word] = 1
    sorted_word_count = sorted(word_count.items(), key= lambda kv: (kv[1], kv[0]))
    for item in sorted_word_count[abs(top_n) * -1:]:
        print('%s|%d' % (item[0], item[1]))
# end find_most_common_unigrams_in_corpus(corpus, top_n)


# Function used to calculate the top_n bigrams with highest frequency in the corpus.
#
# Parameter: corpus - list of sentences
# Parameter: top_n - the top 'int' number of bigrams to print, including their frequencies.
def find_most_common_bigrams_in_corpus(corpus, top_n):
    # Load corpus into memory
    corpus = parse_corpus(corpus)
    phrase = ' '.join(corpus)
    bigram = create_n_gram(phrase=phrase, n=2)
    word_count = {}
    for words in bigram:
        key = ' '.join(words)
        if key in word_count:
            word_count[key] = word_count[key] + 1
        else:
            word_count[key] = 1

    sorted_word_count = sorted(word_count.items(), key= lambda kv: (kv[1], kv[0]))

    for item in sorted_word_count[abs(top_n) * -1:]:
        print('%s|%d' % (item[0], item[1]))
# end find_most_common_bigrams_in_corpus(corpus, top_n)


# Function used to compute the probability of a given phrase against a corpus as unigrams
#
# Parameter: corpus - The name of the file containing the text to be used.
# Parameter: phrase - The sentence or group of words to compute the probability of occurring given the corpus
# Returns: The probability of the phrase occurring
def compute_unigram_probability(corpus, phrase, la_placian_smoothing=False):
    global n_gram_frequency, n_gram_frequency_frequency, corpus_length

    unigram = create_n_gram(phrase=phrase, n=1)

    # Load corpus into memory
    corpus = parse_corpus(corpus)
    compute_n_gram_frequencies(corpus)

    lm = 1.0
    for gram in unigram:
        word = ''.join(gram)
        # probability = 0
        occurrences = n_gram_frequency[word]

        if la_placian_smoothing:
            occurrences = occurrences + 1
            probability = occurrences / corpus_length

        else:
            # Calculate the probability of the word occurring given the number of words in the corpus
            probability = occurrences / corpus_length

        # Compute the product of the probability of each word in the unigram
        lm = lm * probability
        # print('P(%s) = %1.20f' % (current_phrase, probability))
    # print("P(%s) = %1.50f" % (phrase, lm))
    return lm
# end compute_unigram_probability(corpus, phrase)


# Function used to process bigrams and compute the good-turing smoothed probability
#
# Parameter: bigrams - list of bigrams to be computed with
# Returns: good-turing probability of bigram list appearing in provided corpus.
#
def compute_good_turing(bigrams):
    global n_gram_frequency, n_gram_frequency_frequency, corpus_length
    lm = 1.0
    for bigram in bigrams:
        bigram_text = ' '.join(bigram)
        matches = n_gram_frequency[bigram_text]
        N = corpus_length

        # Unseen bigrams
        if matches == 0:
            # The probability of a new word being found
            N_1 = n_gram_frequency_frequency[1]
            P_gt = N_1 / N
            lm = lm * P_gt

        # Seen bigrams
        else:
            c = matches
            N_c_plus_1 = n_gram_frequency_frequency[c + 1]
            N_c = n_gram_frequency_frequency[c]

            c_star = (c + 1) * (N_c_plus_1 / N_c)
            P_star_gt = c_star / N
            lm = lm * P_star_gt
    return lm
# end compute_good_turing(bigrams)


# Function used to compute the probability of a given phrase against a corpus as bigrams
#
# Parameter: corpus - The name of the file containing the text to be used.
# Parameter: phrase - The sentence or group of words to compute the probability of occurring given the corpus
# Returns: The probability of the phrase occurring
def compute_bigram_probability(corpus_name, phrase, la_placian_smoothing=False, good_turing_smoothing=False):
    global n_gram_frequency, n_gram_frequency_frequency, corpus_length
    bigrams = create_n_gram(phrase=phrase, n=2)

    # Load corpus into memory
    corpus = parse_corpus(corpus_name)
    compute_n_gram_frequencies(corpus)

    if good_turing_smoothing:
        return compute_good_turing(bigrams)

    lm = 1.0
    index = 0
    for bigram in bigrams:
        index = index + 1

        bigram_text = ' '.join(bigram)
        matches = n_gram_frequency[bigram_text]

        # Find all occurrences of word 0, with or without word 1
        occurrences = 0
        # if we are looking for occurrences of start or end, that equates to the number of sentences.
        if bigram[0] == '<s>':
            occurrences = len(corpus)
        else:
            occurrences = n_gram_frequency[bigram[0]]

        # This may be an unknown word and we end up dividing by zero, so we use the unknown word token
        # of which there is one.
        if occurrences == 0:
            occurrences = 1

        if la_placian_smoothing:
            matches = matches + 1
            occurrences = occurrences + corpus_length
            probability = matches / occurrences

        else:
            # Calculate the probability of two words occurring given the number of times
            # w1 occurs and the number of times w2 follows w1
            # P_mle(w_i|w_i-1)) = c(w_i-1,w_i)/c(w_i-1)
            probability = matches / occurrences

        # Compute the product of the probability of each set of words in the bigram
        lm = lm * probability
    return lm
# end compute_bigram_probability(corpus, phrase)


#  Function used as main entry point into the application
#
if __name__ == '__main__':
    corpus_libraries = ['Pride and Prejudice by Jane Austen.txt',
                        'Frankenstein; Or, The Modern Prometheus by Mary Wollstonecraft Shelley.txt']

    print('---------------------------------------------------------------------')
    print('---------------------------------------------------------------------')
    corpus = corpus_libraries[0]
    phrase = 'i love to walk with my brother and sister'

    print("Using Corpus: %s " % corpus)

    print('Unigrams')
    lm = compute_unigram_probability(corpus, phrase)
    print("unsmoothed - P(%s) = %1.50f" % (create_n_gram(phrase=phrase, n=1), lm))
    lm = compute_unigram_probability(corpus, phrase, la_placian_smoothing=True)
    print("la_placian_smoothing - P(%s) = %1.50f" % (create_n_gram(phrase=phrase, n=1), lm))

    print('Bigrams')
    lm = compute_bigram_probability(corpus, phrase)
    print("unsmoothed - P(%s) = %1.50f" % (create_n_gram(phrase=phrase, n=2), lm))
    lm = compute_bigram_probability(corpus, phrase, la_placian_smoothing=True)
    print("la_placian_smoothing - P(%s) = %1.50f" % (create_n_gram(phrase=phrase, n=2), lm))
    lm = compute_bigram_probability(corpus, phrase, good_turing_smoothing=True)
    print("good_turing_smoothing - P(%s) = %1.50f" % (create_n_gram(phrase=phrase, n=2), lm))
    print('---------------------------------------------------------------------')

    corpus = corpus_libraries[1]
    phrase = 'i love to walk with my brother and sister'
    print("Using Corpus: %s " % corpus)

    print('Unigrams')
    lm = compute_unigram_probability(corpus, phrase)
    print("unsmoothed - P(%s) = %1.50f" % (create_n_gram(phrase=phrase, n=1), lm))
    lm = compute_unigram_probability(corpus, phrase, la_placian_smoothing=True)
    print("la_placian_smoothing - P(%s) = %1.50f" % (create_n_gram(phrase=phrase, n=1), lm))

    print('Bigrams')
    lm = compute_bigram_probability(corpus, phrase)
    print("unsmoothed - P(%s) = %1.50f" % (create_n_gram(phrase=phrase, n=2), lm))
    lm = compute_bigram_probability(corpus, phrase, la_placian_smoothing=True)
    print("la_placian_smoothing - P(%s) = %1.50f" % (create_n_gram(phrase=phrase, n=2), lm))
    lm = compute_bigram_probability(corpus, phrase, good_turing_smoothing=True)
    print("good_turing_smoothing - P(%s) = %1.50f" % (create_n_gram(phrase=phrase, n=2), lm))
    print('---------------------------------------------------------------------')
