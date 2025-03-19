
from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST


def generate_bot_responses(message, session):
    bot_responses = []

    current_question_id = session.get("current_question_id")
    if not current_question_id:
        bot_responses.append(BOT_WELCOME_MESSAGE)

    success, error = record_current_answer(message, current_question_id, session)

    if not success:
        return [error]

    next_question, next_question_id = get_next_question(current_question_id)

    if next_question:
        bot_responses.append(next_question)
    else:
        final_response = generate_final_response(session)
        bot_responses.append(final_response)

    session["current_question_id"] = next_question_id
    session.save()

    return bot_responses


def record_current_answer(answer, current_question_id, session):
    '''
    Validates and stores the answer for the current question to django session.
    '''
     # Check if current_question_id is valid
    if current_question_id is None or current_question_id < 0 or current_question_id >= len(PYTHON_QUESTION_LIST):
        return False, "Invalid question ID."

    # Check for empty or invalid answers
    if not answer or not isinstance(answer, str):
        return False, "Invalid answer. Please provide a valid response."

    # Retrieve the correct answer
    question_data = PYTHON_QUESTION_LIST[current_question_id]
    correct_answer = question_data.get("answer")

    # Initialize session storage if not present
    if "user_answers" not in session:
        session["user_answers"] = []

    # Store the user's answer and correctness
    session["user_answers"].append({
        "question_id": current_question_id,
        "user_answer": answer.strip().lower(),
        "is_correct": answer.strip().lower() == correct_answer.strip().lower()
    })

    return True, ""


def get_next_question(current_question_id):
    '''
    Fetches the next question from the PYTHON_QUESTION_LIST based on the current_question_id.
    '''

    return "dummy question", -1


def generate_final_response(session):
    '''
    Creates a final result message including a score based on the answers
    by the user for questions in the PYTHON_QUESTION_LIST.
    '''

    return "dummy result"
