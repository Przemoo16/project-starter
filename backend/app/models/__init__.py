# Import the models, so that they can be registered in SQLModel.metadata
from .reset_password import ResetPasswordToken, ResetPasswordTokenID
from .user import User, UserSetPassword

# TODO: Workaround for circular imports describe here:
# https://github.com/tiangolo/sqlmodel/issues/121
User.update_forward_refs(ResetPasswordToken=ResetPasswordToken)
UserSetPassword.update_forward_refs(ResetPasswordTokenID=ResetPasswordTokenID)
