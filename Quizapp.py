import json
import streamlit as st
from streamlit_lottie import st_lottie


#This to load the welcome animation, What happens here is simple, take file from path and load as json
with open("Welcome plants.json", "r") as welcomeanimation:
    jsonanimation = json.load(welcomeanimation)

#Due to streamlits VERY bad way of running this is to ensure that everytime it reruns these key things are still there
if "score" not in st.session_state:
    st.session_state.score = 0

if "qnum" not in st.session_state:
    st.session_state.qnum = -1

if "finished" not in st.session_state:
    st.session_state.finished = False

if "done" not in st.session_state:
    st.session_state.done = False

#this is where we use a sort of list/dict to add questions this is crcuial as this is the base of the quiz every key here matters
questions = [
    {
        "Q": "Who is the richest man on planet earth",
        "O": ["Elon musk", "Bill gates", "Mark zuckerburg" ],
        "A": "Elon musk",
        "M": "https://i.imgur.com/iYpqKHR_d.webp?maxwidth=1520&fidelity=grand"
    },

    {
        "Q": "Who is the founder of the United States?",
        "O": ["George Washington", "Bill gates", "Donald Trump" ],
        "A": "George Washington",
        "M": "https://images.unsplash.com/photo-1447727214830-cbcbf097b52c?q=80&w=1296&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
    },

    {
        "Q": "Who is the current president of the united states?",
        "O": ["George Washington", "Bill gates", "Donald Trump" ],
        "A": "Donald Trump",
        "M": "https://images.unsplash.com/photo-1541876788-2221e585da7f?q=80&w=700&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
    },
]

# this is for the qnum state so it counts all the questions so they can be displayed
TOTAL = len(questions)

# this is the starting screen this is what Clients see and these are all server sided 
# to put it in plain words: if the program starts show the animation, and show text and then show a button to begin the quiz,
# if user presses "Lets start" then begin the quiz from question Number 0 rerun the script now so it updates everything and stop it if something wrong happens
if st.session_state.qnum == -1:
    st_lottie(jsonanimation, height=300)
    st.title("👋🏼 Hello! Welcome to the quiz")
    st.title("General knowlege quiz!")

    if st.button("Lets start!"):
        st.session_state.qnum = 0
        st.rerun()

    st.stop()

# this is the main quiz handler this is where the magic happens
# in simple words the way this part works is that if the quiz is not finished it will show the image of the question and all its content and the options
# the reason why if not is being used is simple: streamlit reruns everytime so the most important parts aka the states must always be there
if not st.session_state.finished:

    current = questions[st.session_state.qnum]
    st.image(current["M"], use_column_width=True)
    st.title(f"Question {st.session_state.qnum + 1}")
    st.write(current["Q"])

    userchoice = st.radio(
        "",
        current["O"],
        key=f"q{st.session_state.qnum}"
    )

    # this is where we check the user submission 
    # this part of script in simple words is checking if the user submits and what happens and if the option choosed by the user is correct
    # if the option is correct the user gets a score if it is not then the user does not 
    if not st.session_state.done:
        if st.button("Submit"):
            st.session_state.done = True
            
            if userchoice == current["A"]:
                st.session_state.score += 1
                st.success("Correct!")
                st.balloons()
            else:
                st.error("Wrong")
                st.write("The correct answer is", current["A"])
            
            st.rerun()
    else:
        # Show the result after submission
        if userchoice == current["A"]:
            st.success("Correct!")
        else:
            st.error("Wrong")
            st.write("The correct answer is", current["A"])

# this is where if the user did submit their answser 
if st.session_state.finished:
    st.title("🎉 Quiz Completed!")
    st.balloons()
    st.subheader(f"Your Final Score: {st.session_state.score} / {TOTAL}")

elif st.session_state.done:
    if st.button("Next"):
        st.session_state.qnum += 1
        st.session_state.done = False
        if st.session_state.qnum >= TOTAL:
            st.session_state.finished = True
        st.rerun()
