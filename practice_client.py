from datetime import datetime
import time
import pyCSM.authorization.auth as auth
import pyCSM.services.session_service.session_service as session_service
import pyCSM.services.session_service.schedule_service as schedule_service
import pyCSM.services.session_service.copyset_service as copyset_service
import pyCSM.clients.session_client as session_client
import pyCSM.services.hardware_service.hardware_service as hardware_service

# s tcpinfo - command on vicom to display address

print("--------------------------------")
print("Step 0: Create session client")
print("--------------------------------")
sessClient = session_client.sessionClient("localhost", "9559", "csmadmin", "csmpword")


print("--------------------------------")
print("Step 1: Create session")
print("--------------------------------")
result=sessClient.create_session("mysession","Migration","session for testing")
print(result.json())

print("--------------------------------")
print("Step 2: Add copysets to session")
print("--------------------------------")
result=sessClient.add_copysets("mysession",[['DS8000:2107.LBL41:VOL:3202','DS8000:2107.LBT61:VOL:3102']],roleorder=None)
print(result.json())

print("--------------------------------")
print("Step 3: Print out session options")
print("--------------------------------")
result=sessClient.get_session_options("mysession")
print(result.json())

print("--------------------------------")
print("Step 4: Issue available commands")
print("--------------------------------")
result=sessClient.get_available_commands("mysession")
print(result.json())

print("--------------------------------")
print("Step 5: Issue Terminate command")
print("--------------------------------")
result=sessClient.run_session_command("mysession",'Terminate')
print(result.json())

print("--------------------------------")
print("Step 5: Issue start GC command")
print("--------------------------------")
result=sessClient.run_session_command("mysession",'StartGC H1->H2')
print(result.json())

print("--------------------------------")
print("Step 6: Issue SYNC and SWAP command")
print("--------------------------------")
result=sessClient.run_session_command("mysession",'Sync And Swap')
print(result.json())

print("---------------------------------------")
print("Waiting for Sync and Swap to complete")
print("---------------------------------------")
for _timeout in range(300, 0, -5):
    result = sessClient.get_session_info("mysession")
    data = result.json()
    print("HyperSwap Status: "+data['hyperswapstatus'])
    print("Session Status: "+data['status'])
    print("Production Host: "+data['productionhost'])
    print("---")
    # Wait until the status transitions to normal and the active host becomes H2
    if ((data['status'] == "Normal") and (data['productionhost'] == "H2")):
        break
    time.sleep(5)


print("--------------------------------")
print("Step 7: Unfence and Clip Command")
print("--------------------------------")
result=sessClient.run_session_command("mysession",'Unfence and Clip')
print(result.json())

time.sleep(5)

print("--------------------------------")
print("Step 8: Undo Clip Command")
print("--------------------------------")
result=sessClient.run_session_command("mysession",'Undo Clip')
print(result.json())

print("-----------------------------------------")
print("Issue available commands PHASE 2")
print("------------------------------------------")
result=sessClient.get_available_commands("mysession")
print(result.json())


print("--------------------------------")
print("Step 9: Get Session info")
print("--------------------------------")
result=sessClient.get_session_info("mysession")
print(result.json())

