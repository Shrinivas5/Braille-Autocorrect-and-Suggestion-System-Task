 Braille Autocorrect and Suggestion System 
Overview:
This project addresses the challenge of autocorrecting and suggesting words for visually 
impaired users typing Braille using a QWERTY keyboard. Since Braille input can be error-prone 
due to mispressed, missing, or extra keys, an efficient and accurate autocorrect system is 
essential for a smooth user experience.
Approach:
1. Braille Mapping & Input Handling:
 - The system maps QWERTY keys (D, W, Q, K, O, P) to Braille dots (1–6), following the 
standard six-key Braille entry method.
 - Each Braille character is entered as a combination of these keys, and the script converts 
these combinations into English letters using a Braille-to-letter mapping based on the 2x3 Braille 
grid.
2. Word Construction:
 - Words are represented as lists of QWERTY Braille key combinations (e.g., ['DK', 'D', 'K'] for 
"cat").
 - The script translates the sequence into a string using the Braille mapping, reconstructing the 
intended word.
3. Autocorrect & Suggestion:
 - To handle typos, missing, or extra keys, the system uses the Levenshtein distance algorithm 
to measure similarity between the input and dictionary words.
 - For optimal performance with large dictionaries, a BK-tree (Burkhard-Keller tree) is used. 
This data structure allows efficient fuzzy search, quickly finding the closest word(s) in the 
dictionary without comparing every word individually.
 - The system suggests the closest matching word(s) based on the minimum edit distance, 
ensuring both speed and accuracy.
4. Efficiency:
 - The BK-tree ensures that even with large dictionaries (tens or hundreds of thousands of 
words), the system remains fast and suitable for real-time use.
 - The approach is scalable and can be adapted for use in embedded devices or web 
applications.
5. Extensibility & Real-World Applications:
 - The system can be extended to support multiple languages, Braille contractions, or even a 
learning mechanism that adapts to user-specific typing patterns over time.
 - This solution can be integrated into assistive devices, educational tools, or mobile 
applications to enhance accessibility for visually impaired users.

Conclusion:
This solution provides an accurate, efficient, and extensible Braille autocorrect and suggestion 
system. By leveraging the BK-tree for fast fuzzy search, it is suitable for real-time use and can 
be scaled to large dictionaries. The approach is robust to common Braille input errors and can 
be further enhanced for broader accessibility needs.
