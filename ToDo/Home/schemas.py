from typing import Optional, Required

from pydantic import BaseModel

class UserSignUpDataSchema(BaseModel):

    signupname : str
    signupemail : str
    signupnumber : Optional[str] = ''
    signuppassword : str
    confirmpassword : str

    class ConfigDict:
        from_attributes = True

class UserLoginDataSchema(BaseModel):

    loginemail : str
    loginpassword : str

    class ConfigDict:
        from_attributes = True

class TaskDataSchema(BaseModel):

    TaskName : str
    TaskDeadline : str

    class ConfigDict:
        from_attributes = True