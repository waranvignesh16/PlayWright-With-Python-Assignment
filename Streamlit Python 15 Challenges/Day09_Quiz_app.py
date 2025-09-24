import streamlit as st

st.title("📝 Quiz Game App")

# -----------------------
# Questions & Answers
# -----------------------
questions = [
    {
        "question": "What is the capital of France?",
        "options": ["Paris", "London", "Berlin", "Rome"],
        "answer": "Paris"
    },
    {
        "question": "Which language is used for data analysis?",
        "options": ["Python", "HTML", "CSS", "JavaScript"],
        "answer": "Python"
    },
    {
        "question": "Who developed the theory of relativity?",
        "options": ["Isaac Newton", "Albert Einstein", "Galileo Galilei", "Nikola Tesla"],
        "answer": "Albert Einstein"
    },
    {
        "question": "What is the largest planet in our solar system?",
        "options": ["Earth", "Mars", "Jupiter", "Venus"],
        "answer": "Jupiter"
    },
]

# -----------------------
# Initialize session state
# -----------------------
if "current_question" not in st.session_state:
    st.session_state.current_question = 0
    st.session_state.score = 0
    st.session_state.answers = []

# -----------------------
# Check if quiz is completed
# -----------------------
if st.session_state.current_question >= len(questions):
    st.subheader("🎉 Quiz Completed!")
    st.write(f"Your Score: **{st.session_state.score} / {len(questions)}**")

    st.write("✅ Summary of your answers:")
    for i, q in enumerate(questions):
        st.write(f"**Q{i+1}: {q['question']}**")
        st.write(f"Your Answer: {st.session_state.answers[i]}")
        st.write(f"Correct Answer: {q['answer']}")
        st.write("---")

    if st.button("Restart Quiz"):
        st.session_state.current_question = 0
        st.session_state.score = 0
        st.session_state.answers = []
        st.rerun()
else:
    # -----------------------
    # Show current question
    # -----------------------
    q_index = st.session_state.current_question
    q_data = questions[q_index]

    st.subheader(f"Question {q_index + 1} of {len(questions)}")
    st.write(q_data["question"])

    # User selects answer
    user_answer = st.radio("Select your answer:", q_data["options"])

    # Submit Button
    if st.button("Submit"):
        st.session_state.answers.append(user_answer)

        if user_answer == q_data["answer"]:
            st.session_state.score += 1

        st.session_state.current_question += 1
        st.rerun()
