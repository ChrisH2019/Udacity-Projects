# RAINBOW TABLE SOLUTION
rainbow_table = {}
for word in nist_bad:
    hashed_word = hashlib.md5(word.encode()).hexdigest()
    rainbow_table[hashed_word] = word
    
# Use the Rainbow table to determine the plain text password
for user in leaked_users_table.keys():
    try:
        print(user + ":\t" + rainbow_table[leaked_users_table[user]['md5']])
    except KeyError:
        print(user + ":\t" + '******* hash not found in rainbow table')