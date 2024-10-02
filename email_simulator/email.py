### --- OOP Email Simulator --- ###

import numpy as np

# --- Classes --- #
class Email:
    '''A class to represent an email.'''
    has_been_read = False

    def __init__(self, email_address, subject_line, email_content):
        '''
        Initialise a new Email instance.

        Parameters:
        email_address: The email address.
        subject_line: The subject line of the email.
        email_content: The content body of the email.
        '''
        self.email_address = email_address
        self.subject_line = subject_line
        self.email_content = email_content

    def mark_as_read(self):
        '''Mark the email as read.'''
        self.has_been_read = True


# --- Functions --- #
def populate_inbox():
    '''Add 3 sample emails to the inbox list.'''
    email_0 = Email("newemailaccount@gmail.com", "Welcome to the Email Simulator!", "This is the first email you will receive in your inbox from the email simulator.")
    inbox.append(email_0)
    email_1 = Email("hootsbahfadd@gmail.com", "Email Simulator Validation", "This email is to confirm that the email simulator has launched properly. There will be one more email to follow.")
    inbox.append(email_1)
    email_2 = Email("awarmwelcomeindeed@gmail.com", "Email Simulator successfully launched!", "This email confirms that the email simulator has been validated via the previous email. Enjoy the system!")
    inbox.append(email_2)

def list_emails():
    '''Print an indexed list of all subject lines from emails in the inbox.'''
    subject_list = [email.subject_line for email in inbox]
    for index, subject in enumerate(subject_list):
        # 'index+1' is so the email indexes will start at 1 and not 0, for 
        # easier readability
        print(f"{index+1} - {subject}")

def read_email(index):
    '''
    Print the email address, subject line and content of a selected email,
    then mark it as read.

    Parameters:
    index: The index of the email in the inbox.
    * 'index-1' to account for 'index+1' in 'list_emails()'.
    '''
    print(f"\n> Email: {inbox[index-1].email_address}\n> Subject: {inbox[index-1].subject_line}\n> {inbox[index-1].email_content}\n> Email end.")
    inbox[index-1].mark_as_read()

# --- Lists --- #
inbox = []

# --- Program Start --- #
populate_inbox()

menu = True

while menu:
    # Allow user to select an option
    user_choice = int(input('''\nWould you like to:
    
    1. Read an email
    2. View unread emails
    3. Quit application

    Enter selection: '''))

    if user_choice == 1:
        # Initiate loop to allow user to select an email from the inbox,
        # and to validate input
        while True:
            print("\nInbox:")
            list_emails()
            print("Type 'back' to return to previous menu.")
            email_selection = input("\nPlease enter the number that corresponds to the email you would like to open: ")
            if email_selection.lower() == 'back':
                break
            try:
                if int(email_selection) >= len(inbox):
                    print("\nInvalid input. Please enter a valid number from the list.")
                else:
                    print("")
                    read_email(int(email_selection))
            except ValueError:
                print("\nInvalid input. Please enter an integer or type 'back'.")
    elif user_choice == 2:
        # Display emails marked as unread/read
        print("")
        for email in inbox:
            if email.has_been_read == True:
                print(f"Email from {email.email_address} marked as READ.")
            else:
                print(f"{email.email_address} - {email.subject_line}")

    elif user_choice == 3:
        # Quit the application
        print("\nApplication has ended.\n")
        menu = False
    else:
        print("\nOops - incorrect input.")
