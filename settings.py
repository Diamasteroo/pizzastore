﻿import os

SECRET_KEY = "secret-here"
SIMPLELOGIN_BLUEPRINT = os.getenv("SIMPLELOGIN_BLUEPRINT")
SIMPLELOGIN_LOGIN_URL = os.getenv("SIMPLELOGIN_LOGIN_URL")
SIMPLELOGIN_LOGOUT_URL = os.getenv("SIMPLELOGIN_LOGOUT_URL")
SIMPLELOGIN_HOME_URL = os.getenv("SIMPLELOGIN_HOME_URL")