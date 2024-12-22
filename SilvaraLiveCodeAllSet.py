

import tradehull
import time
from datetime import datetime
import json
import os
import streamlit as st
import time
import smtplib
import time
from email.mime.text import MIMEText

Completed_Order_id = 0
# Sender email and password
sender_email = "Silvarabot@gmail.com"  # Your sender Gmail address
password = "eyjy janj cbyf lxju"  # Your Gmail password or app password (if 2FA is enabled)
global PLaced_Market_Order
PLaced_Market_Order = False
# Email details
subject = "Test Alert"
body = "This is a test email alert."
recipient_email = "anshjain454@gmail.com"  # Recipient's email address
def send_gmail_alert(subject, body, sender_email, recipient_email, password):
    # Create the email message
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = recipient_email

    try:
        # Connect to the Gmail SMTP server and send the email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
            smtp_server.login(sender_email, password)  # Login with your email and password
            smtp_server.sendmail(sender_email, recipient_email, msg.as_string())  # Send the email
        print("Message sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

UpdatedLastPrice = False
OneOrderIsPlaced = False
# Watchlist instrument token
WATCHLIST = [{"token": "111451399", "name": "SILVERMIC25FEBFUT"}]
 
# Order Status and Price Books
order_status_book = []
Market_order_status_book = []
# Initialize arrays to store names
completed_orders = []
price_order_book = []
Market_order_status_bookss = []
Modification = 0
last_standing_price = 87500
# Constants
NUM_BUY_SELL_ORDERS = 4
GAP = 500  # Price gap for placing orders
CHECK_INTERVAL = 1  # Interval in seconds to check for Tickprice updates
buy_names = []
sell_names = []
we_have_current_order = False
order_status_book =[]

# Function to load order status book from a JSON file
def load_order_status_book():
    order_status_book = []  # Ensure we modify the global variable
    if os.path.exists("order_status_book.json"):  # Check if the file exists
        with open("order_status_book.json", "r") as file:
            order_status_book = json.load(file)  # Load data into the array
    return order_status_book  # Return the array containing the order status book

order_status_booksss = load_order_status_book()
print(order_status_booksss)


# Function to save order status book to a JSON file
def save_order_status_book():
    with open("order_status_book.json", "w") as file:
        print(order_status_book)
        json.dump(order_status_book, file, indent=4)
        return (order_status_book)
    # Function to load order status book from a JSON file



def load_Market_order_status_book():
    Market_order_status_book = []  # Ensure we modify the global variable
    if os.path.exists("Market_order_status_book.json"):  # Check if the file exists
        with open("Market_order_status_book.json", "r") as file:
            Market_order_status_book = json.load(file)  # Load data into the array
    return Market_order_status_book  # Return the array containing the order status book

Market_order_status_booksss = load_Market_order_status_book()
print(Market_order_status_booksss)



# Function to save order status book to a JSON file
def save_Market_order_status_book():
    with open("Market_order_status_book.json", "w") as file:
        print(Market_order_status_book)
        json.dump(Market_order_status_book, file, indent=4)
        return (Market_order_status_book)
        
# API credentials
api_key = "hwkgtf4rx19g6pjk"
api_secret = "86bj6pzsnettaosm6tus0do0pokbjx5c" # Correctly import datetime class

try:
    TH = tradehull.Tradehull(api_key, api_secret, "yes")
    kite = TH.kite

    if kite:
        print("Login Successful!")
    else:
        print("Login Failed. Exiting...")
        exit()
except Exception as e:
    print(f"API Initialization Error: {e}")
    exit()

# Function to fetch the latest price
def fetch_Tickprice(symbol):
    try:
        quote = kite.quote([symbol])
        instrument_data = quote.get(symbol, {})
        tick_price = instrument_data.get("last_price", "N/A")
        if tick_price == "N/A":
            print(f"Could not fetch tick price for {symbol}.")
            return None
        return tick_price
    except Exception as e:
        print(f"Error fetching Tickprice for {symbol}: {e}")
        return None

# Global list to store all order IDs
orders_ids = []

def check_8_order_id_():
    """
    Checks if there are exactly 8 order IDs in the orders_ids list.
    :return: "Yes" if there are exactly 8 order IDs, otherwise "No".
    """
    if len(order_status_book) == 8:
        return "Yes"
    else:
        return "No"

# Function to place a buy AMO order
def place_buy_amo_order(price, quantity=1):
    try:
        # Attempt to place the AMO buy order
        order_id = kite.place_order(
            variety=kite.VARIETY_AMO,  # Set the variety to AMO
            exchange=kite.EXCHANGE_MCX,
            tradingsymbol="SILVERMIC25FEBFUT",
            transaction_type=kite.TRANSACTION_TYPE_BUY,
            quantity=quantity,
            price=price,
            order_type=kite.ORDER_TYPE_LIMIT,
            product=kite.PRODUCT_MIS,
        )
        print(f"AMO Buy Order Placed: ID {order_id}, Price {price}")
        
        # Append the order details to the tracking lists
        orders_ids.append(order_id)
        order_status_book.append({"type": "BUY", "price": price, "status": "OPEN", "order_id": order_id})
        print(order_status_book)
        
    except Exception as e:
        print("Primary attempt to place order failed. Retrying...")
        try:
            # Retry placing the order in case of failure
            order_id = kite.place_order(
                variety=kite.VARIETY_AMO,  # Set the variety to AMO
                exchange=kite.EXCHANGE_MCX,
                tradingsymbol="SILVERMIC25FEBFUT",
                transaction_type=kite.TRANSACTION_TYPE_BUY,
                quantity=quantity,
                price=price,
                order_type=kite.ORDER_TYPE_LIMIT,
                product=kite.PRODUCT_MIS,
            )
            print(f"AMO Buy Order Placed on Retry: ID {order_id}, Price {price}")
            
            # Append the order details to the tracking lists
            orders_ids.append(order_id)
            order_status_book.append({"type": "BUY", "price": price, "status": "OPEN", "order_id": order_id})
            print(order_status_book)
            
        except Exception as retry_error:
            
            # Log the failure of the retry attempt
            print(f"Error placing AMO buy order on retry at {price}: {retry_error}")
            (120)
            #Send Gmail Message


# Function to place a sell AMO order
def place_sell_amo_order(price, quantity=1):
    try:
        order_id = kite.place_order(
            variety=kite.VARIETY_AMO,  # Set the variety to AMO
            exchange=kite.EXCHANGE_MCX,
            tradingsymbol="SILVERMIC25FEBFUT",
            transaction_type=kite.TRANSACTION_TYPE_SELL,
            quantity=quantity,
            price=price,
            order_type=kite.ORDER_TYPE_LIMIT,
            product=kite.PRODUCT_MIS,
        )
        print(f"AMO Sell Order Placed: ID {order_id}, Price {price}")
        
        # Append the order to orders_ids list and order_status_book
        orders_ids.append(order_id)
        order_status_book.append({"type": "SELL", "price": price, "status": "OPEN", "order_id": order_id})
        print(order_status_book)
    except Exception as e:
        print(f"Error placing AMO sell order at {price}: {e}")


def check_status(last_standing_price , UpdatedLastPrice , order_status_book):
    print("Checking order statuses...")

    Completed_Order_id = 0
    if not UpdatedLastPrice:
        (3)

        UpdatedLastPrice = False 
    else:
        (3)
        UpdatedLastPrice = True 
    print(order_status_book)
    print(order_status_book)
    # Iterate over each order in order_status_book
    for order in order_status_book:

        
        order_id = order.get("order_id")
        order_type = order.get("type")
        order_status = order.get("status")
        price = order.get("price")
        name = order.get("name")

        print(f"Checking Order ID: {order_id} - Type: {order_type} - Status: {order_status} - Name: {name}")

        # Fetch order history for the current order_id
        try:
            order_history = kite.order_history(order_id)  # Replace 'kite' with your API client
            if order_history:
                # Get the latest status from the order history
                latest_order = order_history[-1]
                latest_status = latest_order.get("status")
                print(f"Latest Status for Order ID {order_id}: {latest_status}")

                # If the latest status is "COMPLETE"
                if latest_status == "CANCELLED":
                    print(f"Order ID {order_id} is completed.")
                    
                    # Update last standing price
                    last_standing_price = price
                    UpdatedLastPrice = True
                    OneOrderIsPlaced = UpdatedLastPrice
                    Completed_Order_id = order_id
                    print(f"Updated Last Standing Price: {last_standing_price}")
                    print(f" The Complted Order id is {Completed_Order_id}")
                    
                    # Process based on 'name'
                    if name in ["B01", "B02", "B03", "B04", "S01", "S02", "S03", "S04"]:
                        print(f"Processing Name: {name} for Order ID {order_id}")
                    

                    if OneOrderIsPlaced :
                        UpdatedLastPrice = True
                    else:
                        UpdatedLastPrice = False
        except Exception as e:
            print(f"Error fetching history for Order ID {order_id}: {e}")
            print("The Updated Variable is Now")
            print(UpdatedLastPrice)
    # Return all completed orders and the last standing price
    (3)
    return completed_orders, last_standing_price , UpdatedLastPrice , Completed_Order_id 



def cancel_all_orders_if_needed(order_status_book, last_standing_price, UpdatedLastPrice , Completed_Order_id):
    print("While Entering the VCariables are")
    print(last_standing_price)
    print(UpdatedLastPrice)
    print(order_status_book)
    print("\n")
    print("\n")
    (3)

    if last_standing_price is not None and UpdatedLastPrice :
        print("Last standing price updated, canceling all orders...")

        # Loop through the order_status_book and cancel orders
        for order in order_status_book :
            

            try:
                order_id = order.get("order_id")
                print(f"Cancelling Order ID: {order_id}")

                # Implement your cancellation logic here (e.g., via API call)
                if order.get("order_id") != Completed_Order_id: 
                    kite.cancel_order(variety="amo", order_id=order_id)
                    print(f"AMO Order with ID {order_id} cancelled.")  # For regular orders
                else:
                    print("Order Id Is completed cant delete")
                    (2)
            except Exception as e:
                print(f"Error canceling Order ID {order_id}: {e}")


        print("All orders have been canceled. Emptying order status book.")
        print(order_status_book)
        
        order_status_book.clear()
        save_order_status_book()
        print(order_status_book)  # Print empty order book for verification
        (10)  # Optional sleep to manage any delays before further actions

    else:
        print("Last standing price not updated or order status book is empty. No orders canceled.")
        
    return last_standing_price, order_status_book 


# Function to generate the order status message and send email
def send_order_book_status(order_status_book, sender_email, recipient_email, password):
    alert_subject = "ALERT: Order Status Book"
    full_message = "Order Status:\n\n"

    # Loop through all orders in the order status book and generate the message
    for order in order_status_book:
        full_message += "-" * 40 + "\n"
        full_message += f"Order Type: {order['type']}\n"
        full_message += f"Price: {order['price']}\n"
        full_message += f"Status: {order['status']}\n"
        full_message += f"Order ID: {order['order_id']}\n"
        full_message += "-" * 40 + "\n"
    
    # Send the email with all orders
    send_gmail_alert(alert_subject, full_message, sender_email, recipient_email, password)
# Function to generate the order status message and send email
def Market_send_order_book_status(Market_order_status_book, sender_email, recipient_email, password):
    alert_subject = "ALERT: Market-Order-Status-Book"
    full_message = "Order Status:\n\n"

    # Loop through all orders in the order status book and generate the message
    for order in Market_order_status_book:
        full_message += "-" * 40 + "\n"
        full_message += f"Order Type: {order['type']}\n"
        full_message += f"Price: {order['price']}\n"
        full_message += f"Status: {order['status']}\n"
        full_message += f"Order ID: {order['order_id']}\n"
        full_message += "-" * 40 + "\n"
    
    # Send the email with all orders
    send_gmail_alert(alert_subject, full_message, sender_email, recipient_email, password)

# Print completed orders summary
if completed_orders:
    print("Completed Orders Summary:")
    for completed_order in completed_orders:
        print(f"Order ID: {completed_order['order_id']} | Type: {completed_order['type']} | Status: {completed_order['status']}")
else:
    print("No orders are complete.")

# Function to initialize 4 buy and 4 sell AMO orders
def initialize_amo_orders(last_standing_price):
    print("Initializing AMO Orders...")
    print("------------------------------------------------------------------------")
    for i in range(NUM_BUY_SELL_ORDERS):
        buy_price = last_standing_price - (GAP * (i + 1))
        sell_price = last_standing_price + (GAP * (i + 1))
        place_buy_amo_order(buy_price)
        place_sell_amo_order(sell_price)
        save_order_status_book()
        print("---------------------------------------------")
        print(order_status_book)
        print("---------------------------------------------")
        
import time
from datetime import datetime
is_order_placed = False
current_time = datetime.now().strftime("%H:%M")




# 9:01 AM logic
def check_9_01_am_logic(last_standing_price , PLaced_Market_Order, Market_order_status_book):
    print("Market_order_status_book")
    print(Market_order_status_book)
    time.sleep(10)
    global is_order_placed
    is_order_placed = False  # Use the global flag
    while not is_order_placed and not PLaced_Market_Order  and not Market_order_status_book:
            current_time = datetime.now().strftime("%H:%M")
            print("9:01 AM Logic Triggered")
            Tickprice = fetch_Tickprice(WATCHLIST[0]["token"])  # Fetch the Last Traded Price (Tickprice)
            if Tickprice:
                if Tickprice > last_standing_price:
                    # SELL logic
                    try:
                        price_difference = Tickprice - last_standing_price
                        quantity = price_difference // 500
                          # Calculate quantity
                        if quantity > 10:
                                (1000)  # Add a delay of 1 second if quantity exceeds 10

                        print(f"Price Difference: {price_difference}")
                        print(f"Calculated Quantity for SELL: {quantity}")
                        print("Market Order: SELL triggered due to positive difference")
                        if quantity == 0:
                            is_order_placed = True
                            print("As Diffrence is not more then 500 we Dont NEED to Place A order")
                            print("Skipping The 9:01 logic As no need")
                        else:
                                    # Place SELL order
                                    # Place the AMO order and track the order history
                                        order_id = kite.place_order(
                                            variety=kite.VARIETY_AMO,  # Set the variety to AMO
                                            exchange=kite.EXCHANGE_MCX,
                                            tradingsymbol="SILVERMIC25FEBFUT",  # Ensure this is the correct symbol
                                            transaction_type=kite.TRANSACTION_TYPE_SELL,
                                            quantity=quantity,
                                            order_type=kite.ORDER_TYPE_MARKET,  # Market order
                                            product=kite.PRODUCT_MIS,  # Product type
                                        )
                                        print(f"AMO Buy Order Placed: ID {order_id}")
                                                                # Assuming you have the `order_id` after placing the order
                                        order_history = kite.order_history(order_id)

                                        # Printing the order history details to find the price
                                        if order_history and not is_order_placed:
                                            order = order_history[0]

                                            print(f"Order ID: {order['order_id']}")
                                            print(f"Price: {order['average_price']}") 
                                            last_standing_price =   order['average_price']
                                            Market_order_status_book.append({"type": "SELL", "price": order['average_price'], "status": "OPEN", "order_id": order['order_id']})
                                            is_order_placed = True
                                            
                                        else:
                                            print("Errorr Found")
                                            (1)
                                        save_Market_order_status_book()                                   
                    except Exception as e:
                                        print(f"Error placing order or tracking: {e}")
                                        
                else:
                    if not is_order_placed:
                        # BUY logic
                        price_difference = last_standing_price - Tickprice  # Difference for BUY order
                        quantity = price_difference // 500
                        if quantity > 10:
                                (1000)  # Add a delay of 1 second if quantity exceeds 10  # Calculate quantity
                        print(f"Price Difference: {price_difference}")
                        print(f"Calculated Quantity for BUY: {quantity}")
                        print("Market Order: BUY triggered due to negative difference")
                        if quantity == 0:
                            is_order_placed = True
                            print("As Diffrence is not more then 500 we Dont NEED to Place A order")
                            print("Skipping The 9:01 logic As no need")
                        else:                        
                            try:
                                # Place a BUY order
                                order = kite.place_order(
                                    tradingsymbol="MCX:SILVER",  # Trading symbol for Silver
                                    exchange="MCX",  # MCX exchange
                                    transaction_type="BUY",  # Buy order
                                    quantity=quantity,  # The quantity calculated earlier
                                    product="MCX",  # Product type for MCX
                                    order_type="MARKET",  # Market order type
                                    variety="regular"  # Regular order variety
                                )
                                
                                # Extract the order ID from the response
                                order_id = order['order_id']
                                print(f"Market Order BUY placed: Order ID {order_id}")
                                
                                # Fetch the order history to get the price
                                order_history = kite.order_history(order_id)
                                
                                # Check if the order history has any entries and print the first one
                                if order_history and not is_order_placed:
                                    order = order_history[0]  # Access the first order
                                    print(f"Order ID: {order['order_id']}")
                                    print(f"Price: {order['average_price']}")
                                    print(f"Price: {order['average_price']}") 
                                    last_standing_price =   order['average_price']
                                    last_standing_price =   order['average_price']
                                    Market_order_status_book.append({"type": "BUY", "price": order['average_price'], "status": "OPEN", "order_id": order['order_id']})
                                    
                                    is_order_placed = True
                                    
                                else:
                                    print("Errorr Found")
                                    (1)
                            # Extract the order ID from the response
                                save_Market_order_status_book()
                            except Exception as e:
                                print(f"An error occurred: {e}")

            return last_standing_price , is_order_placed ,Market_order_status_book








def time_check():
    # Get the current time
    current_time = datetime.now().strftime("%H:%M:%S")

    # Define market open and close times
    market_open_time = "09:00:00"
    market_close_time = "23:30:00"

    # Check market status based on current time
    if current_time < market_open_time:
        market_status = "early"
    elif market_open_time <= current_time < market_close_time:
        market_status = "open"
    else:
        market_status = "closed"

    # Handle market status logic
    if market_status == "early":
        print("Market is early, waiting for the market to open...")
        (60)  # Re-check every minute
        return market_status

    elif market_status == "closed":
        print("Market is closed, sending message and ending.")
        print("Market is closed. All done.")
        print("All done, ending process.")
        return market_status  # Optionally return to stop further checks

    elif market_status == "open":
        print("Market is open, performing actions...")
        print("Market is open. Proceeding with trading actions.")
        Market_Active = True
        # You can add trading logic or other actions here
        return market_status





# Function to monitor and update orders
# Function to monitor and update orders
def monitor_trading():
    global Market_order_status_book
    global UpdatedLastPrice
    global PLaced_Market_Order
    PLaced_Market_Order = False
    UpdatedLastPrice = False
    last_standing_price = 87500
    initialized = False
    global Prevouis_last_standing_price
    Prevouis_last_standing_price = 0
    completed_orders = completed_orders if 'completed_orders' in locals() else []
    order_status_book = order_status_book if 'order_status_book' in locals() else []

    st.write("🔍 **Order Status Book:**", order_status_booksss)
    if order_status_booksss:
        we_have_current_order = True
    else:
        we_have_current_order = False

    # -------------------------------------------------Login Message ------------------------------------------------------------#
    alert_subject = "ALERT: Login Successful"
    alert_message = f"✅ **The user has successfully logged in at {time.strftime('%Y-%m-%d %H:%M:%S')}**"
    recipient_email = "anshjain454@gmail.com"  # Replace with the recipient's email address

    send_gmail_alert(alert_subject, alert_message, sender_email, recipient_email, password)
    order_status_book = order_status_booksss

    while kite:
        try:
            # ------------------------- 9:01 Logic -----------------------------------------------#
            Prevouis_last_standing_price = last_standing_price
            st.write("📚 **Order Status Book:**", order_status_book)
            st.write("-------------------------------------------------------------------")
            st.write("📊 **Market Order Book:**")
            st.write(Market_order_status_book)
            st.write("-------------------------------------------------------------------")

            Market_order_status_book = load_Market_order_status_book()
            save_Market_order_status_book()
            st.write("📦 **Updated Market Order Book:**", Market_order_status_book)

            if not PLaced_Market_Order and not Market_order_status_book:
                last_standing_price, PLaced_Market_Order, Market_order_status_book = check_9_01_am_logic(
                    last_standing_price, PLaced_Market_Order, Market_order_status_book
                )
                load_Market_order_status_book()
                save_Market_order_status_book()
                Market_order_status_book = Market_order_status_bookss
            else:
                st.write("⏳ **Market order already placed at 9:01 AM.**")

            if PLaced_Market_Order:
                st.write("✅ **Order placed successfully at 9:01 AM!**")

            if last_standing_price == 0:
                last_standing_price = 87500

            # ------------------------------ Check Updated OR not -------------------------------------------------------#
            if OneOrderIsPlaced:
                UpdatedLastPrice = True
            else:
                UpdatedLastPrice = False

            # --------------------------------- Email for ORDER BOOK BEFORE ANY ORDER TODAY ------------------------------#
            recipient_email = "anshjain454@gmail.com"  # Replace with the recipient's email address
            Market_send_order_book_status(Market_order_status_book, sender_email, recipient_email, password)

            # ---------------------------- CHECK PAST ORDERS -----------------------------------------------------------------------#
            st.write("📃 **Checking the Current Placed Orders:**")
            if order_status_book:
                we_have_current_order = True
                st.write("📦 **Previous Orders Restored:**", order_status_book)
            else:
                st.write("❌ **No Previous Order found.**")

            # ---------------------------------- Tick Price --------------------------------------#
            symbol = WATCHLIST[0]["token"]
            Tickprice = fetch_Tickprice(symbol)
            st.write("📈 **Last Standing Price:**", last_standing_price)
            st.write("🔄 **Updated Last Price:**", UpdatedLastPrice)

            if Tickprice:
                st.write("📊 **Tick Price:**", Tickprice)

            if check_8_order_id_() == "Yes":
                initialized = True
                st.write("✅ **There are exactly 8 order IDs.**")
            else:
                st.write("❌ **The number of order IDs is not 8.**")
                st.write("🔄 **Initialized:**", initialized)
                st.write("🔍 **We have current order:**", we_have_current_order)

                # Step 1: Place initial orders
                if not initialized and not we_have_current_order:
                    initialize_amo_orders(last_standing_price)
                    initialized = True
                    order_status_book = save_order_status_book()
                    recipient_email = "anshjain454@gmail.com"
                    send_order_book_status(order_status_book, sender_email, recipient_email, password)

            # ------------------------------------------------------------------------------------------#
            completed_orders, last_standing_price, UpdatedLastPrice, Completed_Order_id = check_status(
                last_standing_price, UpdatedLastPrice, order_status_book
            )
            recipient_email = "anshjain454@gmail.com"
            send_order_book_status(order_status_book, sender_email, recipient_email, password)

            # ------------------------------- Cancelling if Needed --------------------------------#
            cancel_all_orders_if_needed(order_status_book, last_standing_price, UpdatedLastPrice, Completed_Order_id)
            send_order_book_status(order_status_book, sender_email, recipient_email, password)

            # ------------------------------- Initializing order if needed ----------------------------#
            if UpdatedLastPrice:
                initialize_amo_orders(last_standing_price)
                initialized = True
                order_status_book = save_order_status_book()
                st.write("📋 **Order Status Book Updated:**", order_status_book)

            st.write("📈 **The updated last standing price is:**", last_standing_price)
            time.sleep(CHECK_INTERVAL)
        except KeyboardInterrupt:
            st.write("🚪 **Exiting Monitoring Loop...**")
            break
        except Exception as e:
            st.write("⚠️ **Error in monitoring loop:**", e)
            time.sleep(CHECK_INTERVAL)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------



# Main Execution
if __name__ == "__main__":
    try:
        st.title("Trading Bot")
        if st.button("▶️ Start Monitoring"):
            st.write("🚀 **Starting Trading Bot...**")
            monitor_trading()
        if st.button("⏹️ Stop Monitoring"):
            st.write("🛑 **Stopping Trading Bot...**")
    except Exception as e:
        st.write("⚠️ **Error in Main Execution:**", e)
