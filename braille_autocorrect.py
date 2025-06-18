"""
Braille Autocorrect and Suggestion System
-----------------------------------------
This script implements an autocorrect and suggestion system for Braille input using QWERTY Braille typing.

Features:
- Maps QWERTY Braille key combinations to Braille dot patterns and English letters.
- Converts a sequence of QWERTY Braille inputs into a word.
- Suggests the closest word from a dictionary using a BK-tree for efficient fuzzy search (Levenshtein distance).
- Optimized for large dictionaries and real-time use.

Sample Test Cases are provided at the end of the script.
"""
# Braille Autocorrect and Suggestion System
# Author: Thinkerbell Labs Task Solution
#
# QWERTY Braille Mapping:
# D = dot 1, W = dot 2, Q = dot 3, K = dot 4, O = dot 5, P = dot 6
# Example: 'DK' = dots 1+4 = 'c'

from typing import List, Dict, Tuple, Optional, Any

# Mapping from Braille dot pattern (as a tuple of 6 bools) to letter
BRAILLE_TO_LETTER = {
    (1,0,0,0,0,0): 'a',
    (1,1,0,0,0,0): 'b',
    (1,0,0,1,0,0): 'c',
    (1,0,0,1,1,0): 'd',
    (1,0,0,0,1,0): 'e',
    (1,1,0,1,0,0): 'f',
    (1,1,0,1,1,0): 'g',
    (1,1,0,0,1,0): 'h',
    (0,1,0,1,0,0): 'i',
    (0,1,0,1,1,0): 'j',
    (1,0,1,0,0,0): 'k',
    (1,1,1,0,0,0): 'l',
    (1,0,1,1,0,0): 'm',
    (1,0,1,1,1,0): 'n',
    (1,0,1,0,1,0): 'o',
    (1,1,1,1,0,0): 'p',
    (1,1,1,1,1,0): 'q',
    (1,1,1,0,1,0): 'r',
    (0,1,1,1,0,0): 's',
    (0,1,1,1,1,0): 't',
    (1,0,1,0,0,1): 'u',
    (1,1,1,0,0,1): 'v',
    (0,1,0,1,1,1): 'w',
    (1,0,1,1,0,1): 'x',
    (1,0,1,1,1,1): 'y',
    (1,0,1,0,1,1): 'z',
}

# QWERTY key to Braille dot index
KEY_TO_DOT = {'D':0, 'W':1, 'Q':2, 'K':3, 'O':4, 'P':5}

def qwerty_to_braille_pattern(keys: str) -> tuple:
    """Convert QWERTY keys (e.g., 'DK') to a 6-tuple representing Braille dots."""
    pattern = [0]*6
    for k in keys.upper():
        if k in KEY_TO_DOT:
            pattern[KEY_TO_DOT[k]] = 1
    return tuple(pattern)

def braille_pattern_to_letter(pattern: tuple) -> str:
    """Convert a Braille dot pattern to a letter, or '?' if not found."""
    return BRAILLE_TO_LETTER.get(pattern, '?')

def qwerty_braille_word_to_text(qb_word: List[str]) -> str:
    """Convert a list of QWERTY Braille key combos to a word."""
    return ''.join(braille_pattern_to_letter(qwerty_to_braille_pattern(keys)) for keys in qb_word)

# Sample dictionary (can be replaced with a larger one)
DICTIONARY = ['cat', 'dog', 'bat', 'rat', 'mat', 'hat', 'can', 'man', 'fan', 'pan']

def levenshtein_distance(s1: str, s2: str) -> int:
    """Compute the Levenshtein distance between two strings."""
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    if len(s2) == 0:
        return len(s1)
    previous_row = list(range(len(s2) + 1))
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1]

# --- BK-tree implementation for fast fuzzy search ---
class BKTreeNode:
    def __init__(self, word: str):
        self.word = word
        self.children = {}  # distance -> BKTreeNode

    def insert(self, other_word: str, distance_fn):
        dist = distance_fn(self.word, other_word)
        if dist in self.children:
            self.children[dist].insert(other_word, distance_fn)
        else:
            self.children[dist] = BKTreeNode(other_word)

    def search(self, target: str, max_dist: int, distance_fn, results: list):
        dist = distance_fn(self.word, target)
        if dist <= max_dist:
            results.append((self.word, dist))
        for d in range(dist - max_dist, dist + max_dist + 1):
            child = self.children.get(d)
            if child:
                child.search(target, max_dist, distance_fn, results)

class BKTree:
    def __init__(self, words: list, distance_fn):
        self.root: Optional[BKTreeNode] = None
        self.distance_fn = distance_fn
        for word in words:
            self.insert(word)

    def insert(self, word: str):
        if self.root is None:
            self.root = BKTreeNode(word)
        else:
            self.root.insert(word, self.distance_fn)

    def query(self, word: str, max_dist: int = 2) -> list:
        results = []
        if self.root:
            self.root.search(word, max_dist, self.distance_fn, results)
        return sorted(results, key=lambda x: x[1])

# --- End BK-tree implementation ---

def suggest_word_bktree(braille_input: List[str], bktree: BKTree) -> Tuple[str, int]:
    """Suggest the closest word from the BK-tree for the given Braille input."""
    input_word = qwerty_braille_word_to_text(braille_input)
    results = bktree.query(input_word, max_dist=2)
    if results:
        return results[0]  # (word, distance)
    return ("", -1)

def run_tests_bktree(bktree: BKTree):
    print("Sample Test Cases (BK-tree):")
    tests = [
        (['DK', 'D', 'K'], 'cat'),  # correct input
        (['DK', 'D', 'DK'], 'cat'), # typo (last letter should be 'K')
        (['DK', 'D'], 'cat'),       # missing last letter
        (['DK', 'D', 'K', 'D'], 'cat'), # extra letter
        (['DK', 'D', 'O'], 'can'), # 'O' is close to 'K' in Braille
    ]
    for qb_input, expected in tests:
        suggestion, dist = suggest_word_bktree(qb_input, bktree)
        print(f"Input: {qb_input} -> Suggested: {suggestion} (Distance: {dist}), Expected: {expected}")

if __name__ == "__main__":
    # Build BK-tree from dictionary
    bktree = BKTree(DICTIONARY, levenshtein_distance)
    
    # User input mode
    print("Enter a Braille word as a space-separated sequence of QWERTY Braille key combinations (e.g., 'DK D K' for 'cat'):")
    user_input = input().strip()
    qb_input = user_input.split()
    word = qwerty_braille_word_to_text(qb_input)
    print(f"Braille input: {qb_input} -> {word}")
    suggestion, dist = suggest_word_bktree(qb_input, bktree)
    print(f"Suggested word (BK-tree): {suggestion} (Distance: {dist})")
    
    # Optionally, run sample test cases
    # run_tests_bktree(bktree) 