import pickle as pkl

def load_wordlist(file_path) -> list:
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]
    
def add_word_to_trie(trie, word) -> None:
    node = trie
    for char in word:
        if char not in node:
            node[char] = {}
        node = node[char]
    node['#'] = '#'

def create_trie(list) -> dict:
    trie = {}
    for word in list:
        add_word_to_trie(trie, word)
    return trie

def generate_substrings(trie:dict, size:int) -> list:
    substrings = []
    stack = [(trie, "")]
    
    while stack:
        node, substring = stack.pop()
        
        if len(substring) == size:
            substrings.append(substring)
        
        for char in node:
            if char != '#':
                stack.append((node[char], substring + char))
    
    return substrings

def generate_list_from_substrings(trie:dict, substrings:list) -> list:
    w_list = []
    stack = [(trie, "")]
    
    while stack:
        node, substring = stack.pop()
        
        if '#' in node:
            w_list.append(substring)
        
        for char in node:
            if char != '#':
                stack.append((node[char], substring + char))
                
    return [word for word in w_list if word.startswith(tuple(substrings))]


    
def wagner_fischer(s1, s2) -> int:
    len_s1, len_s2 = len(s1), len(s2)
    if len_s1 > len_s2:
        s1, s2 = s2, s1
        len_s1, len_s2 = len_s2, len_s1

    current_row = range(len_s1 + 1)
    for i in range(1, len_s2 + 1):
        previous_row, current_row = current_row, [i] + [0] * len_s1
        for j in range(1, len_s1 + 1):
            add, delete, change = previous_row[j] + 1, current_row[j-1] + 1, previous_row[j-1]
            if s1[j-1] != s2[i-1]:
                change += 1
            current_row[j] = min(add, delete, change)

    return current_row[len_s1]

def spell_check(word, dictionary, return_size: int|None = None) -> list:
    suggestions:list = []

    for correct_word in dictionary:
        distance:int = wagner_fischer(word, correct_word)
        suggestions.append((correct_word, distance))

    suggestions.sort(key=lambda x: x[1])
    if return_size:
        return suggestions[:return_size]
    else:
        return [suggestion for suggestion in suggestions if suggestion[1] < 3]

misspelled_word:str = "wrlod"


try :
    with open("trie.pkl", "rb") as file:
        trie:dict = pkl.load(file)
except FileNotFoundError:
    dictionary:list= load_wordlist("words.txt")
    trie:dict = create_trie(dictionary)
    pkl.dump(trie, open("trie.pkl", "wb"))
substrings:list = generate_substrings(trie, 3)
ms_substr:str = misspelled_word[:3]
candidate_substr:list = [prefix for prefix, _ in spell_check(ms_substr, substrings)]
reduced_list:list = generate_list_from_substrings(trie, candidate_substr)
suggestions = spell_check(misspelled_word, reduced_list, 10)
print(f"Top 10 suggestions for '{misspelled_word}':")
for word, distance in suggestions:
    print(f"{word} (Distance: {distance})")