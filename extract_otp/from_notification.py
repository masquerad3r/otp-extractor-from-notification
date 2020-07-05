#  Logic for fetching the OTP from notification
#  Device Used: REDMI NOTE 5

from appium import webdriver
from selenium.common import exceptions
import time
import re
import argparse


#  Returns the parsed arguments by the users
def parse_arguments():
    parser = argparse.ArgumentParser(description="Automated OTP fetching from notifications")
    parser.add_argument("-l", "--length", type=int, metavar="", help="Length of the OTP (Default Value: 6)")
    parser.add_argument("-p", "--pattern", metavar="", help="Pattern to look for in OTP messages. If the message comes "
                                                            "in the form of 'Your OTP is: 123456', then pattern will "
                                                            "be -> 'Your OTP is'. This is also the default value.")

    args = parser.parse_args()

    #  Setting the default OTP length
    if not args.length:
        args.length = 6

    #  Setting the default pattern string
    if not args.pattern:
        args.pattern = "Your OTP is"

    else:
        args.pattern = args.pattern.strip()

    return args


#  Returns the driver for running various tasks
def setup():

    print("Setting up the driver...")

    #  Setting the initial fields for opening the messaging app
    desired_cap = {
        "deviceName": "",
        "platformName": "Android",
    }

    return webdriver.Remote("http://localhost:4723/wd/hub", desired_cap)


#  Fetches the OTP from the notifications shade
def fetch_otp(driver, otp_message_pattern, otp_length):
    print("Fetching new OTP value...")

    otp = ""
    otp_message = ""
    message_body_list = []

    #  Checking for OTP value received in notification any arbitrarily small number of times
    #  Took 3 here, for getting the best out of 3 luck :)
    print("Checking for any OTP message matching the provided pattern")

    for i in range(3):
        time.sleep(2)

        #  Get the list of all the messages from the notifications
        message_body_list = fetch_messages_from_notification(driver)

        #  Check whether message_body_list is empty or not
        #  If not empty, then do the following actions
        if message_body_list:
            if len(otp_message) == 0:
                otp_message = extract_otp_message(message_body_list, otp_message_pattern)

            else:
                print("Successfully found OTP string")
                break

    #  If no messages found in notification
    if not message_body_list:
        print("No new notifications fetched, please check back when you receive the OTP message")
        print_exit_error()

    if len(otp_message) < otp_length:
        print("OTP not received. If it's my bad, check whether you provided the correct OTP pattern to match")
        print_exit_error()

    else:
        otp = extract_otp_from_message(otp_message, otp_length)

    if len(otp) == 0:
        print("OTP not received. If it's my bad, check whether you provided the correct OTP length")
        print_exit_error()

    return otp


#  Checks from a list of notification messages and returns the message containing the OTP message body
def extract_otp_message(message_body_list, pattern):
    for message in message_body_list:
        if pattern in message.text:
            return message.text

    return ""


#  Extracts the numerical OTP code of the specified length
def extract_otp_from_message(otp, otp_length):
    extracted_otp = re.findall("\d+", otp)

    for possible_otp in extracted_otp:
        if len(possible_otp) == otp_length:
            return possible_otp

    return ""


#  Clears the previous notifications, if available
#  NOTE: value of close_button_id may change according to the mobile environment
def clear_previous_notifications(driver, close_button_id="com.android.systemui:id/dismiss_view"):
    try:
        print("Clearing any previously loaded notifications")

        driver.open_notifications()

        #  Wait for the DOM elements to be loaded properly
        time.sleep(2)

        #  Clear the notifications
        driver.find_element_by_id(close_button_id).click()

        #  Wait for the action to be completed properly
        time.sleep(1)

        #  Open the notification shade
        driver.open_notifications()

    except exceptions.NoSuchElementException:
        print("No previous notifications found")


#  Returns a list of all the element objects from different notifications available of the TextView class
#  NOTE: Value of class_name may change according to the mobile environment
def fetch_messages_from_notification(driver, class_name="android.widget.TextView"):
    return driver.find_elements_by_class_name(class_name)


#  Display the fetched OTP value
def print_otp(otp):
    print(f"OTP received: {otp}")


def print_exit_error():
    print("Exiting...")
    exit()
