from datetime import datetime
from multiprocessing.connection import answer_challenge
import pyCSM.authorization.auth as auth
import pyCSM.services.session_service.session_service as session_service
import pyCSM.services.session_service.schedule_service as schedule_service
import pyCSM.services.session_service.copyset_service as copyset_service
import pyCSM.clients.session_client as session_client
import pyCSM.services.hardware_service.hardware_service as hardware_service
import time
import os
import array
import sys
import pytest
import requests

from zart import harness
import pytest

# Scope=module, indicates that this fixure runs ONCE for every test defined in this python module
# We want to ipl the system once then run all the tests. There are other scopes that allow you to change
# this behavior - see https://docs.pytest.org/en/stable/fixture.html
# Note that params we are using to indicate the zosplex configuration. You could put in multiple configurations
# which would to indicate to run this test across different systems.
@pytest.fixture(scope="module", params=["zos24.zosplex.json","zos25.zosplex.json","zos31.zosplex.json"])
def ipl_system(request):
    from zart import harness
    with harness.Tester(config_file=request.param, pytest=True) as tst:
        # IPL the system with zosplex
        tst.ipl()
    from pycsmsession import create_csm_session
    with harness.Tester(config_file=request.param, pytest=True) as tst:
        tst.ipl()


        # Yield lets us return back to the test to run, and we expose 'tst' (harness class) to the test so it can use it
        yield tst
