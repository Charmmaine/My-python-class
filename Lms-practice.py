num=[1,2,3,4,5]
num[1] = 0
print(num)

#reassigning in dictionaries
eng2fr= {"one":"un", "two":"deux", "three":"trois"}
eng2fr["two"] = "mbili"
print(eng2fr)

# F-string
name = "Charmaine"
age = 20
print(f"This is {name}, she is from Albania, she is {age} years old.")
#an f string evaluates what is in the curly braces and injects it int the string

# try/except
age= int(input("How old are you? "))
print(f"You are {age} years old")
# if the user inputs a string instead of an integer, the program will crash. We can use try/except to handle this error

try:
    age =int(input("How old are you"))
    print(f"You are {age} years old")
except:
    print("ERROR: Please enter a valid number") 

print("The program is still running")      
# For loops
Friends = ["Charmaine", "Martha", "Miriam", "Moses"]
for friend in friends:
    print(f"Happy birthday {friend}")