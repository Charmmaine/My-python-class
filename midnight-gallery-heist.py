import random
 
# ---------------------------------------------------
# THE MIDNIGHT GALLERY HEIST
# A true-crime style investigation quiz.
# You are a detective piecing together clues to solve
# the case. Answer correctly to build your case file!
# ---------------------------------------------------
 
questions = [
    {
        "question": "The gallery's security footage cuts out at 11:47 PM. What is the FIRST thing a detective should check?",
        "choices": ("A. The gift shop receipts", "B. Whether the system was tampered with or simply malfunctioned", "C. The weather report", "D. The janitor's schedule"),
        "answer": "B"
    },
    {
        "question": "A witness says they saw a 'tall figure in a dark coat' near the loading dock. This kind of statement is called:",
        "choices": ("A. Physical evidence", "B. Forensic evidence", "C. Eyewitness testimony", "D. Circumstantial proof"),
        "answer": "C"
    },
    {
        "question": "Investigators find a partial fingerprint on the display case. What should happen to it next?",
        "choices": ("A. Wipe it off to keep the case clean", "B. Photograph it, lift it, and send it for lab comparison", "C. Ignore it since it's only partial", "D. Let the museum staff handle it"),
        "answer": "B"
    },
    {
        "question": "The stolen painting was insured for $2 million just three weeks before the heist. This detail is most useful for establishing:",
        "choices": ("A. The weather that night", "B. A possible motive", "C. The painting's history", "D. The alarm code"),
        "answer": "B"
    },
    {
        "question": "Two suspects give conflicting accounts of where they were that night. This is best described as:",
        "choices": ("A. A confession", "B. An alibi that doesn't hold up", "C. Hard evidence", "D. A confirmed timeline"),
        "answer": "B"
    },
    {
        "question": "Which piece of evidence would a court consider the STRONGEST on its own?",
        "choices": ("A. A rumor from an anonymous tipster", "B. DNA found at the scene matching a suspect", "C. A suspect's nervous behavior in an interview", "D. A vague resemblance in a blurry photo"),
        "answer": "B"
    },
    {
        "question": "The night guard claims she 'never left her post,' but her badge shows she swiped out at 11:50 PM. This is an example of:",
        "choices": ("A. A solid alibi", "B. A contradiction worth investigating further", "C. Proof of innocence", "D. An irrelevant detail"),
        "answer": "B"
    },
    {
        "question": "Detectives find a receipt for a getaway van rented under a fake name. What's the smart next step?",
        "choices": ("A. Assume the case is closed", "B. Trace the payment method and rental location for more leads", "C. Discard it as unrelated", "D. Ask the museum director to pay for it"),
        "answer": "B"
    }
]

# A set of valid answers used to check user input
valid_answers = {"A","B","C","D"}

# Mix up the order of questions
random.shuffle(questions)

#keep track of score
score = 0
total_questions = len(questions)

print("================================")
print("   THE MIDNIGHT GALLERY HEIST")
print("   A True Crime Investigation Game")
print("=================================")
print("A priceless painting vanished from the city gallery last night")
print( "You're the lead detective. Piece together the clues to crack the case")

#Loop through each question one by one
for i in range(total_questions):
    current_question = questions[i]

    print("\nClue", i+1, ":", current_question["question"])
    for choice in current_question["choices"]:
     print(choice)

    # Get user input, handle invalid input with try/except
    try:
        user_answer = input("Your deduction (A/B/C/D): ").strip().upper()
        if user_answer not in valid_answers:
            print("That's not a valid answer.")
        elif user_answer == current_question["answer"]:
            print("Good instinct, detective.")
            score += 1
        else:
            print("That lead goes nowhere. The correct call was", current_question["answer"])
    except Exception as e:
        print("Something went wrong with your input:", e) 

#------------------------------------------------
# Case results and final rank
#------------------------------------------------
print('\n================================')
print("CASE CLOSED")
print("Clues solved:", score, "out of", total_questions)

percentage = (score/total_questions) * 100

if percentage >= 80:
    print("Rank: Master Detective — the case is airtight!")
elif percentage >= 50:
    print("Rank: Solid Investigator — you cracked most of it.")
else:
    print("Rank: Rookie Detective — the case remains unsolved. Try Again.")
 