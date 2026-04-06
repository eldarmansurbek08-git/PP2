# Python has a built-in package called re, which can be used to work with Regular Expressions
import re

# Search the string to see if it starts with "The" and ends with "Spain"
txt = "The rain in Spain"
x = re.search("^The.*Spain$", txt)

# The findall() function returns a list containing all matches
# Return an empty list if no match was found
txt = "The rain in Spain"
x = re.findall("ai", txt)
print(x)

# The search() function searches the string for a match, and returns a Match object if there is a match
# If there is more than one match, only the first occurrence of the match will be returned
# If no matches are found, the value None is returned
txt = "The rain in Spain"
x = re.search("\s", txt)
print("The first white-space character is located in position:", x.start())

# The split() function returns a list where the string has been split at each match
txt = "The rain in Spain"
x = re.split("\s", txt)
print(x) 
# You can control the number of occurrences by specifying the maxsplit parameter
txt = "The rain in Spain"
x = re.split("\s", txt, 1)
print(x)

# The sub() function replaces the matches with the text of your choice
txt = "The rain in Spain"
x = re.sub("\s", "9", txt)
print(x) 
# You can control the number of replacements by specifying the count parameter
txt = "The rain in Spain"
x = re.sub("\s", "9", txt, 2)
print(x)

# A Match Object is an object containing information about the search and the result
txt = "The rain in Spain"
x = re.search("ai", txt)
print(x) #this will print an object 
'''
.span() returns a tuple containing the start-, and end positions of the match.
.string returns the string passed into the function
.group() returns the part of the string where there was a match
'''

txt = "The rain in Spain"
x = re.search(r"\bS\w+", txt)
print(x.span()) 

txt = "The rain in Spain"
x = re.search(r"\bS\w+", txt)
print(x.string) 

txt = "The rain in Spain"
x = re.search(r"\bS\w+", txt)
print(x.group())

# Metacharacters are characters with a special meaning
'''
[] 	A set of characters 	                                                      "[a-m]" 	
\ 	Signals a special sequence (can also be used to escape special characters) 	"\d" 	
. 	Any character (except newline character) 	                                    "he..o" 	
^ 	Starts with 	                                                               "^hello" 	
$ 	Ends with 	                                                                  "planet$" 	
* 	Zero or more occurrences 	                                                   "he.*o" 	
+ 	One or more occurrences 	                                                   "he.+o" 	
? 	Zero or one occurrences 	                                                   "he.?o" 	
{} 	Exactly the specified number of occurrences 	                              "he.{2}o" 	
| 	Either or 	                                                                  "falls|stays" 	
() 	Capture and group
'''

# You can add flags to the pattern when using regular expressions
'''
re.ASCII 	   re.A 	   Returns only ASCII matches 	
re.DEBUG 		         Returns debug information 	
re.DOTALL 	   re.S 	   Makes the . character match all characters (including newline character) 	
re.IGNORECASE 	re.I 	   Case-insensitive matching 	
re.MULTILINE 	re.M 	   Returns only matches at the beginning of each line 	
re.NOFLAG 		         Specifies that no flag is set for this pattern 	
re.UNICODE 	   re.U 	   Returns Unicode matches. This is default from Python 3. For Python 2: use this flag to return only Unicode matches 	
re.VERBOSE 	   re.X 	   Allows whitespaces and comments inside patterns. Makes the pattern more readable 
'''	

# A special sequence is a \ followed by one of the characters in the list below, and has a special meaning
'''
\A 	Returns a match if the specified characters are at the beginning of the string 	                                "\AThe" 	
\b 	Returns a match where the specified characters are at the beginning or at the end of a word                      r"\bain"
      (the "r" in the beginning is making sure that the string is being treated as a "raw string")                     r"ain\b" 	
\B 	Returns a match where the specified characters are present, but NOT at the beginning (or at the end) of a word   r"\Bain"
      (the "r" in the beginning is making sure that the string is being treated as a "raw string") 	                 r"ain\B" 	
\d 	Returns a match where the string contains digits (numbers from 0-9) 	                                            "\d" 	
\D 	Returns a match where the string DOES NOT contain digits 	                                                     "\D" 	
\s 	Returns a match where the string contains a white space character 	                                            "\s" 	
\S 	Returns a match where the string DOES NOT contain a white space character 	                                      "\S" 	
\w 	Returns a match where the string contains any word characters                                                    "\w"
      (characters from a to Z, digits from 0-9, and the underscore _ character) 	
\W 	Returns a match where the string DOES NOT contain any word characters 	                                         "\W" 	
\Z 	Returns a match if the specified characters are at the end of the string  	                                      "Spain\Z" 
'''	

# A set is a set of characters inside a pair of square brackets [] with a special meaning
'''
[arn] 	   Returns a match where one of the specified characters (a, r, or n) is present 	
[a-n] 	   Returns a match for any lower case character, alphabetically between a and n 	
[^arn] 	   Returns a match for any character EXCEPT a, r, and n 	
[0123] 	   Returns a match where any of the specified digits (0, 1, 2, or 3) are present 	
[0-9] 	   Returns a match for any digit between 0 and 9 	
[0-5][0-9] 	Returns a match for any two-digit numbers from 00 and 59 	
[a-zA-Z] 	Returns a match for any character alphabetically between a and z, lower case OR upper case 	
[+] 	      In sets, +, *, ., |, (), $,{} has no special meaning, so [+] means: return a match for any + character in the string
'''