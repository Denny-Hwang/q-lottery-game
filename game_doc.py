import streamlit as st

def lotto_doc():
    st.image("https://www.dhlottery.co.kr/images/company/img_bi_intro_logo1.png", width=300)
    st.title("Korean lottery - *Lotto 6/45*")
    st.write(
        """
        In the **Lotto 6/45**, you can choose six numbers in the range 45
        """)

def powerball_doc():
    st.image(
        "https://s3.amazonaws.com/cdn.powerball.com/drupal/files/2020-02/Powerball%20%2B%20PP%20Horizontal-Flat-Color.jpg",
        width=300)
    st.title("USA lottery - *Power ball*")

    st.write(
        """       
        In the **Power ball**, you can choose five *White ball* in the range 69 and select one *Power ball* in the range 26
        """)

def lotto_India_doc():
    st.image(
        "https://www.lotto.in/images/lottery-logos/lotto-india-logo.png",
        width=300)
    st.title("India lottery - *Lotto India*")

    st.write(
        """       
        In the **Lotto India**, you can choose six numbers in the range 50 and select one *Joker Ball* in the range 5
        """)

def lotto7_doc():
    st.image(
        "https://cdn.lottolyzer.com/images/lotto7mediumlogo.gif",
        width=300)
    st.title("Japen lottery - *Lotto7*")

    st.write(
        """       
        In the **Lotto7**, you can choose seven numbers in the range 37
        """)

def french_lottery_doc():
    st.image(
        "https://upload.wikimedia.org/wikipedia/commons/thumb/d/df/Logo_FDJ.svg/1024px-Logo_FDJ.svg.png",
        width=400)
    st.title("France lottery - *French Lottery*")

    st.write(
        """       
        In the **French_lottery**, you can choose five numbers in the range 49 and select one *Lucky number* in the range 10
        """)

#######################################################################################################
""" <RESISTRATION FORM>

def (GAME_NAME)_doc():
    st.title("GAME_NAME Q-Lottery Game")

    st.write(
        ""       
        WRITE DOWN HERE ABOUT GAME RULE SHORTLY

        "")
        
"""
#######################################################################################################

def custom_doc():
    st.title("Custom Q-Lottery Game")

    st.write(
        """       
        Customize your Q-Lottery Game

        """)
