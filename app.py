from pytezos import pytezos
import streamlit as st
from streamlit.elements.alert import AlertMixin




def welcome():
    return "Welcome All"


def buyTicket():
    
    st.write("Enter the details to buy a lottery ticket.")
    
    qty = st.number_input("Enter the number of lottery tickets to buy.", step=1,min_value=1)
    email = st.text_input("Enter your Email Address")
    name = st.text_input("Enter your Name")
    number = st.text_input("Enter your Mobile Number")
    number = int(number)
    keyin = st.text_input("Enter your wallet key")
    
    amt = qty * 1000000

    if st.button("Buy"):
        pytezos = pytezos.using(shell = 'https://florence-tezos.giganode.io', key=keyin)
        contract = pytezos.contract('KT1T5GMtK6HUxHu7UDpttoxWqEg6YVpCCmZU')
        contract.buyTicket(qty = qty, email=email, name=name, number = number).with_amount(amt).as_transaction().fill().sign().inject()

def main():
    st.set_page_config(page_title="LotteryTezos")


    st.title("@LotteryTezos")
    st.markdown(
        """<div style="background-color:#e1f0fa;padding:10px">
                    <h1 style='text-align: center; color: #304189;font-family:Helvetica'><strong>
                    Lottery System on Tezos</strong></h1></div><br>""",
        unsafe_allow_html=True,
    )

   

    st.sidebar.title("Entrypoints")
    st.sidebar.markdown("Select the entrypoints accordingly:")
    algo = st.sidebar.selectbox(
        "Select the Opetion", options=["BuyTicket"]
    )

    if algo == "BuyTicket":
        buyTicket()
    


if __name__ == "__main__":
    main()
