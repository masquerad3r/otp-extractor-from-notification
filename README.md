# otp-extractor-from-notification

## Overview
This simple working example demonstrates how one can achieve the automatic 2FA code, aka OTP, extraction for automated application testing. The functionalities can be further tweaked according to individual requirements. 

**Example Test Case**: Automated Web application testing, whose login is protected with 2FA and the OTP code is sent through SMS. Since, different factors are being checked here, 

1. **Password**: Something a user knows
2. **OTP code on mobile**: Something a user has

It becomes somewhat tedious to automate such a workflow. Hence, this code aims to make automated testing of such use cases a bit easier.

## Methodology Used
The code follows the below mentioned methodology:

1. Take **OTP Length** and **OTP message pattern to match** as arguments from user.
2. Clear any previously loaded notifications, if any.
3. Wait for a small duration and look for any message that matches the user supplied pattern.
4. Extract the OTP numerical code of specified length from the message.
5. Print the extracted OTP code.

## Running the tool
**NOTE**: Main package is 'extract_otp'. The 'test_case.py' file simply shows the way one can interact with the package.

### Setting up the environment
For those who just need a quick list to go to, do the following:
1. Appium Desktop Application [download](https://github.com/appium/appium-desktop/releases).
2. Android Studio [download](https://developer.android.com/studio).
3. Add the Java and Android SDK installation directories to system path.

For visual type people, see this youtube [video](https://www.youtube.com/watch?v=FlKJuQihRiw&list=PLWIBmxdTr81dDEZRiNxoy55dIDWtMyOoc).

### Required Modules
Required modules are included in the requirements.txt file. Simply, run the following command to install all the dependencies.
```
pip install -r requirements.txt
```

### Usage
The tool has 2 optional parameters which the user can specify.

1. **OTP Length**: Expected length of the OTP code. (Default: 6)
2. **OTP Pattern**: Expected pattern of OTP message. (Default: "Your OTP is")

```
usage: test_case.py [-h] [-l] [-p]

Automated OTP fetching from notifications

optional arguments:
  -h, --help       show this help message and exit
  -l , --length    Length of the OTP (Default Value: 6)
  -p , --pattern   Pattern to look for in OTP messages. If the message comes
                   in the form of 'Your OTP is: 123456', then pattern will be
                   -> 'Your OTP is'. This is also the default value.
```
