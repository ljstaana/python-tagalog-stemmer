from syllabicator import Syllabicator
import json 
import re

class Stemmer: 
    
    def __init__(self, syllabicator, options, wordlist): 
        self.syllabicator = syllabicator 
        self.options = options 
        
        self.verbose = options["verbose"] 

        # hash dictionary for speed 
        self.words = {} 

        # cache for speed 
        self.cache = {}

        # wordlist 
        for word in wordlist: 
            self.words[word.lower()] = True 

        print(len(self.words))

        self.affixes = []

        # clusters 
        self.clusters = self.treefy([
            "bl", "br", 
            "dr", "dy", 
            "gr", 
            "kr", "ky", 
            "pl", "pr", 
            "sw", 
            "tr", "ts", 
            "sh"
        ]) 

        # tagalog stopwords 
        self.stopwords = ["akin","aking","ako","alin","am","amin","aming","ang","ano","anumang","apat","at","atin","ating","ay","bababa","bago","bakit","bawat","bilang","dahil","dalawa","dapat","din","dito","doon","gagawin","gayunman","ginagawa","ginawa","ginawang","gumawa","gusto","habang","hanggang","hindi","huwag","iba","ibaba","ibabaw","ibig","ikaw","ilagay","ilalim","ilan","inyong","isa","isang","itaas","ito","iyo","iyon","iyong","ka","kahit","kailangan","kailanman","kami","kanila","kanilang","kanino","kanya","kanyang","kapag","kapwa","karamihan","katiyakan","katulad","kaya","kaysa","ko","kong","kulang","kumuha","kung","laban","lahat","lamang","likod","lima","maaari", "man", "maaaring","maging","mahusay","makita","marami","marapat","masyado","may","mayroon", "nasa", "mga","minsan","mismo","mula","muli","na","nabanggit","naging","nagkaroon","nais","nakita","namin","napaka","narito","nasaan","ng","ngayon","ni","nila","nilang","nito","niya","niyang","noon","o","pa","paano","pababa","paggawa","pagitan","pagkakaroon","pagkatapos","palabas","pamamagitan","panahon","pangalawa","paraan","pareho","pataas","pero","pumunta","pumupunta","sa","sabihin","sarili","sila","sino","siya","tatlo","tayo","tulad","tungkol","una","walang"]

        # prefixes 
        self.prefixes = [
            "nakikipag", "pakikipag", "pinakama", 
            "pagpapa", "pakiki", "magpa", 
            "napaka", "pinaka", "panganga", 
            "nakapag", "tagapag", "pinag", 
            "pagka", "ipinag", "mapag", 
            "mapa", "taga", "ipag", "makipag", 
            "nakipag", "tiga", "pala", "pina", 
            "pang", "ipa", "nang", "naka", 
            "pam", "pan", "pag", "mag", "nam", 
            "nag", "man", "may", "ma", "na", "ni", 
            "pa", "in", "ka", "um", "ibi", 
            "jo", "a", "e", "i", "o", "u"
        ]

        # suffixes
        self.suffixes = [
            "uhan", "han", "hin", "ing", 
            "ng", "an", "in", "n",
        ] 

        # infixes 
        self.infixes = [
            "in", "um"
        ]

        # vowels 
        self.vowels = \
            self.treefy([
                "a", "e", "i", "o", "u"
            ])

        # checks if a word is already seen 
        self.seen = {} 

        # applies circumfixation on prefixes 
        self.apply_circumfixation  



    # hashmaps a consonant cluster for optimization (makes searching
    # for a cluster a log(1) operation) 
    def treefy(self, array): 
        hash = {} 
        for val in array: 
            # lookup 
            lookup = hash 
            # loop through the end 
            for i in range(len(val)): 
                letter = val[i] 
                if i > len(val) - 1: 
                    break 
                role = {} 
                if i == len(val) - 1: 
                    role = True 
                if letter not in lookup: 
                    lookup[letter] = role 
                lookup = lookup[letter] 
            lookup = hash 
        return hash

    # returns the first consonant cluster that is matched by the word
    # with priority on longer clusters
    def tree_match(self, cluster, index, word): 
        result = "" 
        lookup = cluster 
        # get the piece of the word from index to the last letter 
        string = self.word[index:] 
        for i in range(len(string)): 
            letter = string[i] 
            # look for the current letter in the clusters 
            if letter in lookup:
                lookup_t = lookup[letter] 
            else: 
                return False
            if type(lookup_t) == type({}): 
                # if found, then change lookup and add letter to buffer
                lookup = lookup_t 
                result += letter 
            elif lookup_t == True: 
                # return the result 
                result += letter 
                break 
            else: 
                # if not found, then quit and return not a cluster 
                return False
        return result 
    
    # syllabicator getter 
    def syllabicator(self):
        return self.syllabicator 

    # output 
    def out(self, smessage):
        if self.verbose: 
            # print(message)
            pass 
        return None 

    # letter type checker 
    def is_vowel(self, letter): 
        return letter in self.vowels 
    
    def is_consonant(self, letter): 
        return letter not in self.vowels 

    # prefix circumfix 
    # - applies circumfixation on a prefix 
    # - circumfixation is applied after the first consonant 
    def circumfix_prefix(self):
        # add -in- and -um- after the first 
        # consonant of the word 
        letters = prefix.split("")
        buffer = "" 
        if self.is_consonant(leter): 
            circumfixed_prefixes = {} 
            for infix in self.infixes: 
                tail = prefix[index+1:] 
                fix = buffer + infix + tail 
                circumfixed_prefix.append(fix) 
            return circumfixed_prefixes 
        return False 

    # circumfix prefixes / apply circumfixation 
    def apply_circumfixation(self):
        circumfixes = []
        for prefix in self.prefixes: 
            circumfixes += self.circumfix_prefix(prefix) 
        self.prefixes += circumfixes 
    
    # prefix matcher 
    # - gets which prefixes a word matches 
    def prefix_match(self, word): 
        prefix_matches = [] 
        for prefix in self.prefixes: 
            if len(prefix) < len(word): 
                # check if word matches prefix 
                word_part = word[0:len(prefix)] 
                if prefix == word_part: 
                    prefix_matches.append(prefix) 
        return prefix_matches

    # suffix matcher 
    def suffix_match(self, word): 
        suffix_matches = [] 
        for suffix in self.suffixes: 
            if len(suffix) < len(word): 
                # check if word matches suffix 
                word_part = word[-len(suffix):] 
                if suffix == word_part: 
                    suffix_matches.append(suffix)
        return suffix_matches 

    # infix matches 
    # - gets which infixes a word matches 
    def infix_match(self, word): 
        infix_matches = []
        for infix in self.infixes: 
            # check if word has infix after the first consonant 
            word_part = word.find(infix)
            if word_part and word_part != len(word) - len(infix) - 1: 
                infix_matches.append(infix) 
        return infix_matches 

    # removes specific infixes from a word 
    def remove_fixes(self, word, prefix, infix, suffix): 
        word_t = word[0:] 
        if prefix is not None:   
            word_t = word_t[len(prefix):] 
        if suffix is not None:  
            word_t = word_t[0:len(word_t) - len(suffix)]
        if infix is not None: 
            word_t = re.sub(infix, "", word_t) 

        return word_t 
    
    # gets the first consonant in the word (returns index) 
    def first_consonant(self, word): 
        for i in range(len(word)): 
            letter = word[i] 
            if self.is_consonant(letter): 
                return i 
        return None 

    # gets the first vowel in the word (returns index )
    def first_vowel(self, word): 
        for i in range(len(word)):
            letter = word[i] 
            if self.is_vowel(letter): 
                return i 
        return None

    # handles partial reduplication 
    def handle_partial_reduplication(self, root, original): 
        roott = root

        if len(root) > 1: 
            if root[0] == root[1]:
                roott = root[1:]
                
        original_syls = self.syllabicator.syllabicate(original)
        root_syls = self.syllabicator.syllabicate(roott) 
        no_dups = [] 


        if len(root_syls) == 2:
            if root_syls[0] == root_syls[1]: 
                no_dups.append(root[1:-1]) 
    

        if len(root_syls) >= 3: 
            if self.is_consonant(root[0]) and self.is_vowel(root[1]): 
                root_t = root[0:] 
                no_dups.append(root_t[2:]) 
        
        # "if the first syllable of the root has a cluster of 
        #  consonants, two approaches can be used. This is based on the 
        #  speaker's habit" 
        cluster = self.tree_match(self.clusters, 0, root)

        if len(root) > 2: 
            first_cons = self.first_consonant(root) 
            first_vow = self.first_vowel(root) 
            if first_cons and first_vow: 
                if first_vow - first_cons == 1 and self.tree_match(self.clusters, first_cons + 1, root): 
                    root_t = root[0:] 
                    root_t[first_cons:first_vow] = "" 
                    no_dups.append(root_t) 
        else: 
            return [] 

        # approach 2 : reduplicates the cluster of consonants 
        # including the succeeding vowel of the stem 
        if cluster: 
            root_t = root[0:]  
            root_t = root_t[len(cluster):]
            no_dups.append(root_t) 
    
        # in a three syllable root, the first two syllables 
        # are reduplicated and hyphenated from the stem 
        if len(root_syls) == 5: 
            first_two_syls = root_syls[0:1] 
            root_t = root[0:]  
            root_t = root_t[len(first_two_syls) + 1:]
            no_dups.append(root_t)

        return no_dups

    # unassimilates a word by prefix 
    def prefix_unassimilate(self, word, prefix): 
        word_reverts = [] 
       
        word_t = word[0:] 

        # D-R Assimilation
        # dapat - marapat 
        # change in d to r where in between two vowels 
        # VdV - VrV 
        # happens in prefixing 
        # checks if the word starts with `r` 

        if word[0] == 'r' and len(word) > 1: 
            # check if the last letter of the prefix is a vowel 
            vowel_last = self.is_vowel(prefix[-1]) 
            # check if the second letter of the word is a vowel
            vowel_next = self.is_vowel(word_t[1])  
            # if both are vowels then change r back to d 
            if vowel_last and vowel_next: 
                word_reverts.append("d" + word_t[1:]) 
            

        # CUSTOM ASSIMILATION BY PREFIX 
        word_t = word[0:] 
        starts_vowel = self.is_vowel(word_t[0]) 

        # if word starts with m 
        if word[0] == "m": 
            word_reverts.append("b" + word[1:])

        # for prefixes that ends in 'm' 
        if prefix[-1] == "m" and starts_vowel: 
            # b_case 
            word_reverts.append("b" + word) 
            word_reverts.append("p" + word) 

        # for prefixes that ends in 'n' 
        elif prefix[-1] == "n" and starts_vowel: 
            # d case 
            word_reverts.append("d" + word) 
            # l case 
            word_reverts.append("l" + word) 
            # s case 
            word_reverts.append("s" + word) 
            # t case 
            word_reverts.append("t" + word) 

        # for prefixes that ends in `ng` 
        elif prefix[-1] == "ng" and starts_vowel: 
            # get word's tail 
            tail = word_t[1:] 
            # k case 
            word_reverts.append("k" + word) 
            # null case 
            word_reverts.append(tail) 

        return word_reverts 

    # checks if a word has a vowel or not 
    def has_no_vowel(self, word): 
        for i in range(len(word)): 
            letter = word[i] 
            if self.is_vowel(letter): 
                return False 
        return True 
    
    # checks if a word has a consonant or no 
    def has_no_consonant(self, word): 
        for i in range(len(word)): 
            letter = word[i] 
            if self.is_consonant(letter): 
                return False 
        return True 
    
    # unassimilates a word by suffix 
    def suffix_unassimilate(self, word, suffix): 
        word_reverts = [] 
        word_t = word[0:] 
        # print("word: ", word, " | suffix: " , suffix)


        # D-R ASSIMILATION 
        # If suffix is either
        # -in- or -an an and the word ends in r 
        # unassimilate r to d 
        if suffix == "in" or suffix == "ang" or suffix == "an" and word_t[-1] == "r": 
            # print("suffix unassimilate")
            # print("suffix : " + suffix)
            # print("word : " + word)
            word_t = word_t[0:-1] + "d" 
            if word_t not in self.seen: 
                word_reverts.append(word_t) 
            #print("word_t: " + word_t)

        if suffix == "ng" and word_t[-1] == "a": 
            word_t  = word_t[0:-1] + "" 
            if word_t in self.seen: 
                word_reverts.append(word_t)
        
        if suffix == "hin" or suffix == "han": 
            word_reverts.append(word + "i")
        
        # O-U ASSIMILATION 
        # if there is a suffix 
        # change the last u to an o 
        word_t = word[0:] 
        for i in range(len(word_t)): 
            idx = len(word) - 1 
            letter = word_t[idx] 
            if letter == "u": 
                word_t[idx] = "o" 
                if word_t not in seen: 
                    word_reverts.append(word_t) 
                break 
        
        # KAS-KS ASSIMILATIO N
        word_t = word[0:] 
        word_t = word_t[::-1] 
        word_t = re.sub("sk", "sak", word_t) 
        word_reverts.append(word_t[::-1]) 

      
        return word_reverts 

    # acceptability conditions for a candidate/form 
    # as described in the paper 
    def accept_state(self, candidate, original): 
        state = True 
        if self.is_vowel(original[0]): 
            shorter_than_three = len(candidate) < 3 
            if shorter_than_three or self.has_no_vowel(candidate): 
                state = False 
        else: 
            shorter_than_three = len(candidate) < 3 
            if shorter_than_three or self.has_no_consonant(candidate): 
                state = False 
        return state 

    # handle full word reduplication 
    # full word reduplication 
    # sarisari gamugamo 
    # paruparo 
    def handle_full_word_reduplication(self, word, original): 
        no_dups = [] 
        # remove hyphens in the middle 
        word_t = re.sub("-", " ", word) 
        # get the first and right half of the word 
        word_left = word_t[0:int(len(word_t)/2)-1] 
        word_right = word_t[int(len(word_t)/2):] 
        # handle assimilatory case 
        if word_left and word_right: 
            if word_left[-1] == "u" and word_right[-1] == "o": 
                word_left_t = word_left[0:] 
                word_left_t[-1] = "o" 
                word_left = word_left_t 
            # handle non assimilatory case 
            if word_left == word_right: 
                if self.seen(word_left): 
                    no_dups.append(word_left) 
        return no_dups 

    # filters a set of words by the accepted conditions only 
    def accepts_only(self, candidates, original): 
        final = []
        # remove words with beginning consonants (more than 2) that 
        # are not a consonant cluster 
        candidates_new = [] 
        for candidate in candidates: 
            consonant_start = 0 
            for i in range(len(candidate)): 
                letter = candidate[i] 
                if self.is_consonant(letter): 
                    consonant_start +=  1 
                else: 
                    break 
            # check if cluster 
            if consonant_start >= 2: 
                if self.tree_match(self.clusters, 0, candidate): 
                    candidates_new.append(candidate) 
            else: 
                candidates_new.append(candidate) 
        
        candidates = candidates_new 

        # handle partial reduplication
        for candidate in candidates: 
            candidates += self.handle_full_word_reduplication(candidate, original)
            candidates += self.handle_partial_reduplication(candidate, original)

        for candidate in candidates: 
            # handle partial and full reduplication on candidate 
            accept = self.accept_state(candidate, original) 
            if accept: 
                final.append(candidate) 
        
        return final 

    # unfixes a word 
    def do_unfix(self, word, prefixes, infixes, suffixes): 
        # print("Suffix: ", suffixes)

        # affixes 
        prefixes.append(None)
        infixes.append(None)
        suffixes.append(None)

        #print("Prefixes: ", prefixes) 
        #print("Suffixes: ", suffixes)

    
        # Candidates List
        candidates = [] 

        prefix_no = 0 

        # remove all prefix, infix and suffix combinations 
        for prefix in prefixes: 
            for infix in infixes: 
                for suffix in suffixes: 
                    # print("@ prefix: ", prefix, " infix: ", infix, " suffix: ", suffix)
                    
                    # remove current affixes from word 
                    word_t = word[0:] 
                    orig_word = word_t
                    word_t = self.remove_fixes(word_t, prefix, infix, suffix) 
                    if len(word_t) < 3: 
                        continue


                    # print("w: ", word_t, " orig:", orig_word, " suffix: ", suffix)
                
                    # special cases 
                    if prefix != None: 
                        if prefix[-1] == "g" and word_t[0] != "-" and self.is_vowel(word_t[0]): 
                            continue 
                    # unassimilate word by prefix 
                    if prefix: 
                        reverts = self.prefix_unassimilate(word_t, prefix) 
                        # add reverted words to candidates 
                        candidates += reverts 
                    candidates = list(set(candidates)) 

                    # unassimilate a word by suffix 
                    if suffix: 
                        reverts = self.suffix_unassimilate(word_t, suffix)
                        # add reverted words to candidates 
                        candidates += reverts 
                    candidates = list(set(candidates)) 

                    # add word to candidates 
                    candidates.append(word_t) 

                    prefix_no += 1
                    # print("\n")
        candidates = self.accepts_only(candidates, word) 
        candidates.sort(key=len)

        return list(set(candidates)) 
    
    # stems a word 
    def do_stem(self, word, prev_affixes): 

        # if a word has been seen already, don't process it 
        if word in self.seen: 
            return [] 
        else: 
            self.seen[word] = True 
        if word in self.cache: 
            return self.cache[word] 
        
        prefix_matches = self.prefix_match(word) 
        suffix_matches = self.suffix_match(word)
        infix_matches = self.infix_match(word) 
        fix_nos = len(prefix_matches) + len(infix_matches) + len(suffix_matches) 
        
        cur_affixes = [prefix_matches, suffix_matches, infix_matches] 
        
        self.affixes += prefix_matches
        self.affixes += suffix_matches
        self.affixes += infix_matches
        self.affixes = list(set(self.affixes))
        

        if prev_affixes != cur_affixes: 
            candidates = \
                self.do_unfix(word, prefix_matches, infix_matches, suffix_matches) 

            for candidate in candidates:
                candidates += self.do_stem(candidate, cur_affixes )

            candidates = list(set(candidates))
            self.cache[word] = candidates
            return candidates 

        
        return [word]

    # stemmer driver 
    def stem(self, word): 
        self.seen = {} 
        self.word = word 
        if len(word.split("-")) > 1: 
            word = word.split("-")[1] 
        
        results = self.do_stem(word, []) 

        if word[0] == "i":
            results = self.do_stem(word[1:], []) + results 

        if len(results) == 1 and results[0] == word : 
            results = [word] 

        if len(word) <= 3:
            return [word]

        # filter tagalog words only 
        final_results  = []
        aside = [] 
        for result in results: 
            if result in self.words and result not in self.stopwords: 
                final_results.append(result)
            else: 
                aside.append(result)

        final_results.sort(key=len) 
        final_results += aside 
        final_results = self.accepts_only(final_results, word) 

        
        return final_results 

    # validity test - from a tsv file 
    def validity_test(self, test_file, report_file): 
        ifile = open(test_file, "r").read()
        ofile = open(report_file, "w") 

        words = {} 
        for line in ifile.split("\n")[1:]: 
            tokens = line.split(":")
            words[tokens[0].strip()] = tokens[1].strip()

        # Display test words
        i = 0 
        for word in words: 
            print(f"{i + 1} Word: {word} | Expected: {words[word]}\n") 
            i += 1

        # Make tests 
        results = {} 
        score = 0 
        total = len(words) 
        for word in words:
            stems = self.stem(word) 
            print(stems) 
            result = stems[0]
            correct = words[word]
            if result == correct: 
                score += 1 
            results[word] = result 

        # Get results 
        accuracy = score * 1.0 / total 

        # Display results 
        i = 0 
        for word in words: 
            result = results[word] 

            correct = words[word]
          
            in_dict = True
            if correct not in self.words:
                in_dict = False 

            restype = "WRONG"
            if result == correct:
                restype = "CORRECT"

            print(f"#{i + 1} | Word: {word} | Expected: {words[word]} | Expected in Dictionary? {str(in_dict)} | Prediction : {results[word]} | " + restype)

            i += 1
        

options = {
    "verbose" : False
} 

wordlist = open("wordlist", "r").read().split("\n") 
syllabicator = Syllabicator(options) 
stemmer = Stemmer(syllabicator, options, wordlist)

text = "masayang kinuha ang barkada"
words = text.split(" ")
stemmyes = []
for word in words: 
    stems = stemmer.stem(word)
    if stems == []: 
            stems = [word] 
    stemmyes.append(stems[0])
print(stemmyes)

# stemmer.validity_test("test_words.txt", "results.txt")