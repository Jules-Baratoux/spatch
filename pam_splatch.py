
import syslog


INFO = """
Welcome to Splatch!\n
Select a server to connect to..\n

\t1)developer (10.0.0.3)
\t2)sales (10.0.0.2)
\t3)admin (10.0.0.1)

"""


def prompt_password(pamh, pwd_prompt="Password:"):
    pass


def prompt_info(pamh, info):
    try:
        message = pamh.Message(pamh.PAM_TEXT_INFO, info)
        resp = pamh.conversation(message)
    except pamh.exception as e:
        return e.pam_result
    return resp


def parse_server_selection(response):
    
    if int(response) > 0 and int(response) < 3:
        return response
    raise Exception("invalid response")


def prompt_message(pamh, prompt, parse_func):
    
    try:
        message = pamh.Message(pamh.PAM_PROMPT_ECHO_ON, prompt)
        resp = pamh.conversation(message)
        return parse_func(resp)
    except pamh.exception as e:
        return e.pam_result

    
def pam_sm_authenticate(pamh, flags, argv):
    try:
        user = pamh.get_user(None)
        # open db to check if user exists
        # if user_exists == false
        prompt_info(pamh, INFO)
        selection = prompt_message(pamh, "Server: ")
        syslog.syslog(str(selection))
        if user == "splatch":
            return pamh.PAM_SUCCESS
    except pamh.exception, e:
        return e.pam_result
    return pamh.PAM_SUCCESS
    

def pam_sm_setcred(pamh, flags, argv):
    return pamh.PAM_SUCCESS


def pam_sm_acct_mgmt(pamh, flags, argv):
    return pamh.PAM_SUCCESS


def pam_sm_open_session(pamh, flags, argv):
    return pamh.PAM_SUCCESS


def pam_sm_close_session(pamh, flags, argv):
    return pamh.PAM_SUCCESS


def pam_sm_chauthtok(pamh, flags, argv):
    return pamh.PAM_SUCCESS
                                
