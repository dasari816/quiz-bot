
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
    '''def get_next_question(session):
    '''
    Fetches and returns the next quiz question from the PYTHON_QUESTION_LIST.
    '''
    # Initialize if session doesn't have current_question_id
    if "current_question_id" not in session:
        session["current_question_id"] = 0
    else:
        session["current_question_id"] += 1

    # Check if all questions are completed
    if session["current_question_id"] >= len(PYTHON_QUESTION_LIST):
        return {"status": "completed", "message": "Quiz completed. Thank you for participating!"}

    # Fetch the next question
    question_data = PYTHON_QUESTION_LIST[session["current_question_id"]]
    return {
        "status": "success",
        "question_id": session["current_question_id"],
        "question": question_data.get("question"),
        "options": question_data.get("options

    return True, ""


def get_next_question(current_question_id):
    '''
    Fetches the next question from the PYTHON_QUESTION_LIST based on the current_question_id.
    '''
   def get_next_question(session):
    '''
    Fetches and returns the next quiz question from the PYTHON_QUESTION_LIST.
    '''
    # Initialize if session doesn't have current_question_id
    if "current_question_id" not in session:
        session["current_question_id"] = 0
    else:
        session["current_question_id"] += 1

    # Check if all questions are completed
    if session["current_question_id"] >= len(PYTHON_QUESTION_LIST):
        return {"status": "completed", "message": "Quiz completed. Thank you for participating!"}

    # Fetch the next question
    question_data = PYTHON_QUESTION_LIST[session["current_question_id"]]
    return {
        "status": "success",
        "question_id": session["current_question_id"],
        "question": question_data.get("question"),
        "options": question_data.get("options", []),  # Assuming multiple-choice questions may have options
    }
                                  
    return "dummy question", -1


def generate_final_response(session):
    '''
    Creates a final result message including a score based on the answers
    by the user for questions in the PYTHON_QUESTION_LIST.
    '''
    def generate_final_response(session):
    '''
    Calculates the final score and provides a summary of the quiz results.
    '''
    # Ensure necessary data exists
    if "user_answers" not in session or "current_question_id" not in session:
        return {"status": "error", "message": "No quiz data found. Please start the quiz."}

    # Calculate the score
    correct_count = 0
    for i, question in enumerate(PYTHON_QUESTION_LIST):
        user_answer = session["user_answers"].get(i)
        if user_answer is not None and user_answer == question.get("correct_answer"):
            correct_count += 1

    total_questions = len(PYTHON_QUESTION_LIST)
    score_percentage = (correct_count / total_questions) * 100

    # Provide feedback based on score
    if score_percentage == 100:
        feedback = "Excellent! You got all answers correct!"
    elif score_percentage >= 75:
        feedback = "Great job! You have a strong understanding of the material."
    elif score_percentage >= 50:
        feedback = "Good effort! A little more practice will help."
    else:
        feedback = "Keep practicing, and you'll get better!"

    # Final result response
    return {
        "status": "completed",
        "score": correct_count,
        "total_questions": total_questions,
        "percentage": round(score_percentage, 2),
        "feedback": feedback
    }

    return "dummy result"
