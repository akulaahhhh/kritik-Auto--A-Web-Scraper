# Kritik Long, Didn't Read (KLDR)

***Developed by [@aidilrx04](https://github.com/aidilrx04) maintained by [@akulaahhhh](https://github.com/akulaahhhh)***

A simple program to semi-automate article post insertion from other news source such as NST TheStar and MalayMail.

## Features

Automatically create:
- Post Title
- Post Content
- Post Excerpt
- Post Featured Image
- Post Tags

## Constraints/Limits

This program contains a few limits:

- Cannot automatically select post category
- Cannot automatically set schedule/time for post
- cannot automatically schedule/post the article

## Requirements

- Python 3.x
- PyCharm Community

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/aidilzohl/kritik-auto.git
    cd kritik-auto
    ```

3. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. **Set up environment variables**: Open `.env` file in the root directory and change `KRITIK_USER` and `KRITIK_PASS` to your kritik admin username and password respectively.
    ```text
    KRITIK_USER='INSERT_YOUR_KRITIK_USERNAME_HERE'
    KRITIK_PASS='INSERT_YOUR_KRITIK_PASSWORD_HERE'
    ```

2. **Run the application**:  
Rune the `main.py` file using PyCharm
    ```bash
    python main.py
    ```

3. **Insert Post URL**:  
Copy and paste the post URL you want to automate to the prompt.  
For example, https://nst.com.my/....
  
4. **Post submission**:  
Select post category and schedule time and click post/schedule to upload the post
  
5. **Multiple post**:  
Unfortunately this program cannot handle multiple post at a time.  
Restart this program to start another article post.


## Project Structure

```plaintext
kritik-auto/
├── chromedriver-win64  
│   └── chromedriver.exe   # Chrome driver
│
├── helpers  
│   ├── driver.py          # Construct chrome driver
│   ├── image.py           # Save and manipulate image
│   └── url.py             # Manipulate URL
│
├── images                 # store all article images
│
├── providers
│   ├── provider.py        # Abstract news provider
│   ├── nst.py             # NST Provider
│   └── thestar.py         # TheStar Provider
├── .env                   # Project environment
├── requirements.txt       # Dependency requirements
├── main.py                # Main file entrance
```
