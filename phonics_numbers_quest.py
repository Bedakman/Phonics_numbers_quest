"""
Phonics & Numbers Quest
------------------------
Final Project - Stanford Code in Place

Created by: Amos
Context: Built for use as a teacher-led classroom game at an underserved
primary school in Ghana (Lead For Ghana), where learners face a basic
literacy and numeracy gap. Designed to be run on ONE screen by the
teacher, who reads questions aloud and types in the class's answers,
while the program tracks individual learner scores and a leaderboard.

Concepts used: variables, strings, lists, dictionaries, functions,
loops, and file reading -- all core Code in Place / CS106A techniques.
"""

import random

WORD_BANK_FILE = "word_bank.txt"
NUMBER_BANK_FILE = "number_bank.txt"


def load_questions(filename):
    """
    Reads a question bank file and returns a list of question dictionaries.
    Each line in the file looks like:
        type|prompt|answer|option1|option2
    where type is either "open" or "mc" (multiple choice).
    """
    questions = []
    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if line == "":
                continue
            parts = line.split("|")
            question = {
                "type": parts[0],
                "prompt": parts[1],
                "answer": parts[2],
                "option1": parts[3],
                "option2": parts[4],
            }
            questions.append(question)
    return questions


def ask_question(question):
    """
    Displays a single question to the teacher (who reads it aloud to the
    class) and collects the answer that the teacher types in on the
    class's behalf. Returns True if correct, False if not.
    """
    print()
    print(question["prompt"])

    if question["type"] == "mc":
        # Show the two options in random order so the answer position
        # is not always the same.
        options = [question["option1"], question["option2"]]
        random.shuffle(options)
        print("  A) " + options[0])
        print("  B) " + options[1])
        choice = input("Which did the class choose? (A/B): ").strip().upper()
        if choice == "A":
            chosen_answer = options[0]
        elif choice == "B":
            chosen_answer = options[1]
        else:
            chosen_answer = ""
    else:
        chosen_answer = input("Type the class's answer: ").strip().lower()

    correct_answer = question["answer"].strip().lower()
    is_correct = chosen_answer.strip().lower() == correct_answer

    if is_correct:
        print("Correct! Great job!")
    else:
        print("Not quite. The correct answer was: " + question["answer"])

    return is_correct


def run_round(questions, scores, num_questions):
    """
    Runs one full round of the game: asks num_questions questions,
    one learner at a time, updating the scores dictionary as it goes.
    """
    # Make a shuffled copy so we don't always ask questions in the same
    # order, and so we don't modify the original question bank list.
    shuffled_questions = questions[:]
    random.shuffle(shuffled_questions)

    questions_to_ask = shuffled_questions[:num_questions]

    for question in questions_to_ask:
        learner_name = input("\nWhose turn is it? Type the learner's name: ").strip()
        if learner_name == "":
            learner_name = "Class"

        # Make sure this learner has an entry in the scores dictionary.
        if learner_name not in scores:
            scores[learner_name] = 0

        correct = ask_question(question)
        if correct:
            scores[learner_name] += 1


def show_leaderboard(scores):
    """
    Prints every learner's score, sorted from highest to lowest.
    """
    print("\n----- LEADERBOARD -----")
    if len(scores) == 0:
        print("No scores yet!")
        return

    # Sort learners by score, highest first.
    sorted_learners = sorted(scores.keys(), key=lambda name: scores[name], reverse=True)

    rank = 1
    for name in sorted_learners:
        print(str(rank) + ". " + name + " - " + str(scores[name]) + " point(s)")
        rank += 1
    print("------------------------")


def choose_mode():
    """
    Asks the teacher to pick Word Mode, Number Mode, or both, and returns
    the chosen mode as a string.
    """
    print("\nChoose a mode:")
    print("  1) Word Mode (phonics)")
    print("  2) Number Mode (numeracy)")
    print("  3) Mixed (both word and number questions)")
    choice = input("Enter 1, 2, or 3: ").strip()

    if choice == "1":
        return "word"
    elif choice == "2":
        return "number"
    elif choice == "3":
        return "mixed"
    else:
        print("Didn't recognize that, defaulting to Mixed mode.")
        return "mixed"


def main():
    print("=========================================")
    print("   PHONICS & NUMBERS QUEST")
    print("   A classroom learning game")
    print("=========================================")
    print("Instructions for the teacher:")
    print("- Read each question aloud to the class.")
    print("- Type in the name of the learner whose turn it is.")
    print("- Enter the class's answer (or pick A/B for multiple choice).")
    print("- The game keeps score for every learner you name.")

    word_questions = load_questions(WORD_BANK_FILE)
    number_questions = load_questions(NUMBER_BANK_FILE)

    scores = {}
    keep_playing = True

    while keep_playing:
        mode = choose_mode()

        if mode == "word":
            question_pool = word_questions
        elif mode == "number":
            question_pool = number_questions
        else:
            question_pool = word_questions + number_questions

        num_questions_input = input(
            "How many questions for this round? (default 5): "
        ).strip()
        if num_questions_input.isdigit():
            num_questions = int(num_questions_input)
        else:
            num_questions = 5

        # Don't try to ask for more questions than exist in the bank.
        num_questions = min(num_questions, len(question_pool))

        run_round(question_pool, scores, num_questions)
        show_leaderboard(scores)

        again = input("\nPlay another round? (y/n): ").strip().lower()
        keep_playing = again == "y"

    print("\nThanks for playing Phonics & Numbers Quest! Well done, everyone!")


if __name__ == "__main__":
    main()
