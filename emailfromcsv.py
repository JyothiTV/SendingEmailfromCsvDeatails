import csv
from email.header import Header
from email.mime.text import MIMEText
import smtplib
import socket


email_subject_template = '''{subject} .'''
email_content_template = '''Hi {firstname} {lastname} 
                            {emailbody}   
                            Thanks, Rob Willison  .'''


def send_email_to_multiple_contact_in_csv_file_with_personalized_content(smtp_server_domain1, smtp_server_port1, from_address1, csv_file_path1):

    # get all rows in the csv file and return a list.
    csv_row_list = read_multiple_contacts_from_csv_file(csv_file_path1)

    # loop in the csv rows list and send emai
    for row_dict in csv_row_list:

        # parse out required column values from the dictionary object
        to_firstname = ''
        to_lastname = ''
        to_addr = ''
        to_subject = ''
        to_emailbody = ''


        # loop in row keys(csv column names).
        for csv_column_name in row_dict.keys():
            # csv column value.
            column_value = row_dict[csv_column_name]

            # assign column value to related variable.
            if csv_column_name.lower() == 'first_name':
                to_firstname = column_value
            if csv_column_name.lower() == 'last_name':
                    to_lastname = column_value
            if csv_column_name.lower() == 'email':
                to_address = column_value
            elif csv_column_name.lower() == 'subject':
                to_subject = column_value
            elif csv_column_name.lower() == 'Email Body':
                to_emailbody = column_value

        # create personalized email content with the parsed out personal data.

        email_subject = email_subject_template.format(subject=to_subject)
        email_data = email_content_template.format(firstname=to_firstname, lastname=to_lastname, emailbody=to_emailbody)
        send_email(smtp_server_domain1, smtp_server_port1, from_address1, to_address, email_subject, email_data)


# this method mainly focus on send the email.
def send_email(smtp_server_domain1, smtp_server_port1, from_address1, to_address, email_subject, email_data):
    # create MIMEText object and specify the email content as plain text format.
    msg = MIMEText(email_data, 'plain', 'utf-8')
    # set email from, to attribute value to display them in the email client tool( thunderbird, outlook etc. ).
    msg['From'] = from_address1
    msg['To'] = to_address
    msg['Subject'] = Header(email_subject, 'utf-8').encode()
    # create SMTP server object which will be used to send email.

    print(smtp_server_domain1)
    print(smtp_server_port1)

    username = input('Enter your  username \n')
    password = input('Enter the password \n')

    smtp_server = smtplib.SMTP_SSL(smtp_server_domain1, smtp_server_port1)
    smtp_server.helo()
    smtp_server.starttls()
    smtp_server.login(username,password)
    # send the email to specified SMTP server.
    smtp_server.sendmail(from_address1, to_address, msg)
    smtp_server.close()
    print('Email sent sucessfully')


def read_multiple_contacts_from_csv_file(csv_file_path1):
    csv_rows_list = []

    try:
        # open the csv file.
        file_object = open(csv_file_path1, 'r')

        # create a csv.DictReader object with above file object.
        csv_file_dict_reader = csv.DictReader(file_object)
        # get column names list in the csv file.
        column_names = csv_file_dict_reader.fieldnames
        # loop in csv rows.
        for row in csv_file_dict_reader:
            # create a dictionary object to store the row column name value pair.
            tmp_row_dict = {}
            # loop in the row column names list.
            for column_name in column_names:
                # get column value in this row. Convert to string to avoid type convert error.
                column_value = str(row[column_name])
                tmp_row_dict[column_name] = column_value

            csv_rows_list.append(tmp_row_dict)

    except FileNotFoundError:
        print(csv_file_path1 + " not found.")
    finally:
        print("csv_rows_list = " + csv_rows_list.__repr__())
        return csv_rows_list


if __name__ == '__main__' :

    smtp_server_domain = 'smtp.gmail.com'
    smtp_server_port = 465
    from_address = 'jyothitv24@gmail.com'
    csv_file_path = 'C:/Users/Jaya/Downloads/sample_email - Copy.csv'
    send_email_to_multiple_contact_in_csv_file_with_personalized_content(smtp_server_domain, smtp_server_port, from_address, csv_file_path)
