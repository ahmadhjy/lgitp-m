import requests
from requests.exceptions import RequestException


def send_sms(user, password, msisdn, sid, msg, fl):
    url = "http://sms.j-telecom.co.uk/vendorsms/pushsms.aspx"
    params = {
        'user': user,
        'password': password,
        'msisdn': msisdn,
        'sid': sid,
        'msg': msg,
        'fl': fl
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
        return response.json()
    except RequestException as e:
        print(f"An error occurred: {e}")
        return None


if __name__ == "__main__":
    # Replace these values with your actual credentials and details
    user = "Ghaith"
    password = "Ghaith!321"
    msisdn = "96179145670"  # Replace with actual mobile number
    sid = "084962"
    msg = "test message from api"  # Your message content
    fl = 0  # Flash message flag, 1 if flash message else 0

    response = send_sms(user, password, msisdn, sid, msg, fl)
    if response:
        print(response)
    else:
        print("Failed to send SMS")
