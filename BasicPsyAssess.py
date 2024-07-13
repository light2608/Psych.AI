# Define the PHQ-9 questions and answer options
questions = [
    "1. Little interest or pleasure in doing things?",
    "2. Feeling down, depressed, or hopeless?",
    "3. Trouble falling or staying asleep, or sleeping too much?",
    "4. Feeling tired or having little energy?",
    "5. Poor appetite or overeating?",
    "6. Feeling bad about yourself — or that you are a failure or have let yourself or your family down?",
    "7. Trouble concentrating on things, such as reading the newspaper or watching television?",
    "8. Moving or speaking so slowly that other people could have noticed? Or the opposite — being so fidgety or restless that you have been moving around a lot more than usual?",
    "9. Thoughts that you would be better off dead, or thoughts of hurting yourself in some way?"
]

options = [
    "0: Not at all",
    "1: Several days",
    "2: More than half the days",
    "3: Nearly every day"
]

# Store the responses
responses = []

# Ask each question and collect responses
print("Please answer the following questions based on how you have felt over the past 2 weeks.\n")

for question in questions:
    print(question)
    for option in options:
        print(option)
    while True:
        try:
            response = int(input("Select an option (0-3): "))
            if response in [0, 1, 2, 3]:
                responses.append(response)
                break
            else:
                print("Please select a valid option (0-3).")
        except ValueError:
            print("Please enter a number between 0 and 3.")

# Calculate the total score
total_score = sum(responses)

# Output the total score
print("\nYour total PHQ-9 score is:", total_score)

# Provide some interpretation of the score (optional)
if total_score <= 4:
    interpretation = "Minimal or no depression"
elif 5 <= total_score <= 9:
    interpretation = "Mild depression"
elif 10 <= total_score <= 14:
    interpretation = "Moderate depression"
elif 15 <= total_score <= 19:
    interpretation = "Moderately severe depression"
else:
    interpretation = "Severe depression"

print("Interpretation:", interpretation)
