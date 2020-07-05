from extract_otp.from_notification import *

args_obj = parse_arguments()
driver = setup()
clear_previous_notifications(driver)
otp = fetch_otp(driver, args_obj.pattern, args_obj.length)
print_otp(otp)
