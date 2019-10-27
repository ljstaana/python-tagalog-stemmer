import sqlite3
conn = sqlite3.connect('tagalog.db')

words = []
i = 0
for row in conn.execute("SELECT * FROM Dictionary"): 
    wordst = row[2].split(" ")
    for word in wordst: 
        words.append(word)
    i += 1

words = list(set(words))

file = open("wordlist", "w")
for word in words: 
    file.write(word + "\n")