[Hello](#hello)
===============

Implement a program that prints out a simple greeting to the user, per the below.

    $ python hello.py
    What is your name?
    David
    hello, David


[Specification](#specification)
-------------------------------

Write, in a file called `hello.py` in `~/pset6/hello`, a program that prompts a user for their name, and then prints `hello, so-and-so`, where `so-and-so` is their provided name, exactly as you did in [Lab 1](../../../labs/1/), except that your program this time should be written in Python.

[Usage](#usage)
---------------

Your program should behave per the example below.

    $ python hello.py
    What is your name?
    Emma
    hello, Emma


[Testing](#testing)
-------------------

While `check50` is available for this problem, you’re encouraged to first test your code on your own for each of the following.

*   Run your program as `python hello.py`, and wait for a prompt for input. Type in `David` and press enter. Your program should output `hello, David`.
*   Run your program as `python hello.py`, and wait for a prompt for input. Type in `Brian` and press enter. Your program should output `hello, Brian`.

Execute the below to evaluate the correctness of your code using `check50`. But be sure to compile and test it yourself as well!

    check50 cs50/problems/2021/x/sentimental/hello


Execute the below to evaluate the style of your code using `style50`.

    style50 hello.py


This problem will be graded only along the axes of correctness and style.

[How to Submit](#how-to-submit)
-------------------------------

Execute the below, logging in with your GitHub username and password when prompted. For security, you’ll see asterisks (`*`) instead of the actual characters in your password.

    submit50 cs50/problems/2021/x/sentimental/hello
