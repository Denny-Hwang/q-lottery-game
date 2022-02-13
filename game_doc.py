import streamlit as st

def lotto_doc():
    st.image("https://www.dhlottery.co.kr/images/company/img_bi_intro_logo1.png", width=300)
    st.title("Korean lottery - *Lotto 6/45*")
    st.write(
        """
        In the **Lotto 6/45**, you can choose six numbers in the 1~45 range
        """)

def powerball_doc():
    st.image(
        "https://s3.amazonaws.com/cdn.powerball.com/drupal/files/2020-02/Powerball%20%2B%20PP%20Horizontal-Flat-Color.jpg",
        width=400)
    st.title("USA lottery - *Power ball*")

    st.write(
        """       
        In the **Power ball**, you can choose five *white ball* in the 1~69 range and select one *power ball* in the 1~26 range
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
