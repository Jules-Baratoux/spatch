
def prompt_password(pamh, pwd_prompt="Password:"):
    pass


def prompt_info(pamh, info):
    message = pamh.Message(pamh.PAM_TEXT_INFO,
                           "Welcome to Splatch!\n Please select a server:\n")
    try:
        resp = pamh.conversation(message)
    except pamh.exception as e:
        return e.pam_result
    return resp


def prompt_message(pamh, info):
    pass


def pam_sm_authenticate(pamh, flags, argv):
    try:
        user = pamh.get_user(None)
        # open db to check if user exists
        # if user_exists == false
        prompt_info(pamh, "")
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
                                
