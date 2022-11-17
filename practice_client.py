from datetime import datetime
import pyCSM.authorization.auth as auth
import pyCSM.services.session_service.session_service as session_service
import pyCSM.services.session_service.schedule_service as schedule_service
import pyCSM.services.session_service.copyset_service as copyset_service
import pyCSM.clients.session_client as session_client
import time
import os
import pytest
import requests
from zart import harness

#in this file, functions will be made to then be called by the test_var1 file (imported)
#
def create_csm_session():
# s tcpinfo - command on vicom to display address
    print("--------------------------------")
    print(" Create session client")
    print("--------------------------------")
    sess_client = session_client.sessionClient("localhost", "9559", "csmadmin", "csmpword")

    print("--------------------------------")
    print(" Create session")
    print("--------------------------------")
    # Create a session

    #convert following variable to inpurt parameter

    in_session_name = "mysession"
    session_type = "Migration"
    in_session_description = "session for testing"
    result = sess_client.create_session (in_session_name,session_type,in_session_description)
    data= result.json()
    #if output says session already exists, delete it and then create it
    if  (data['msg'] == "I"):
        raise Exception("Sorry there was a session creation error, please try again.")
    #continue with the rest of the script
    else:
        print(data)
        print("You may proceed forward.")

create_csm_session()
