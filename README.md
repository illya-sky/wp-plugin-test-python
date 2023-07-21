# MPMU plugin test
The Automation test is written on Python using Pytest framework.

The test consist of 3 sets of variables.
- 1st set - is supposed to be a Positive test. I pull correct data using Faker lib and some custom variables
- 2nd and 3rd are Negative tests with invalid data. 

There are two options of the test to finish:
- if the test is successful you get a message in the console that it is PASSED
- if it is failed, you get a screenshot of the Error messages from the page and have those screenshots saved to Failed tests folder. Each screenshot named after the test name.

## To RUN the test:
1. Set up the project to use the latest version of Python
2. In the Forms folder create login.py file with wpadmin credentials consists of two variables
- WP_USERNAME = "YOUR_LOGIN"
- WP_PASSWORD = "YOUR_PASSWORD"