from api.ApiConnector import ApiConnector
from otp.otpbase import OTPGlobals

class JWTAccountDB:
    def __init__(self, loginManager):
        self.loginManager = loginManager
        try:
            apiUrl = config.GetString('api-server', None)
            self.authApi = ApiConnector(apiUrl)
        except Exception as e:
            self.authApi = ApiConnector()

    def lookup(self, playToken, callback):
        response = self.authApi.validate_token(playToken)
        if not response.get("success"):
            callback({"success": False, "reason": response.get("reason")})
            return

        username = response.get("data", {}).get("username")
        astronAccountId = response.get("data", {}).get("astronId")

        if not astronAccountId:
            accessLevel = config.GetString("default-access-level", "SYSTEM_ADMIN")
            if accessLevel not in OTPGlobals.AccessLevelName2Int:
                self.loginManager.notify.warning(
                f'Access Level "{accessLevel}" isn\'t defined.  Reverting back to SYSTEM_ADMIN'
                )
            accessLevel = "SYSTEM_ADMIN"
            callback(
                {
                    "success": True,
                    "accountId": 0,
                    "databaseId": username,
                    "accessLevel": accessLevel,
                }
            )
        else:
            def handleAccount(dclass, fields):
                if dclass != self.loginManager.air.dclassesByName["AstronAccountUD"]:
                    result = {
                        "success": False,
                        "reason": "Your account object (%s) was not found in the database!"
                        % dclass,
                    }
                else:
                    result = {
                        "success": True,
                        "accountId": astronAccountId,
                        "databaseId": username,
                        "accessLevel": fields.get("ACCESS_LEVEL", "NO_ACCESS"),
                    }
                callback(result)

            # Query the account from Astron to verify its existance. We need to get
            # the ACCESS_LEVEL field anyways.
            # TODO: Add a timeout timer?
            self.loginManager.air.dbInterface.queryObject(
                self.loginManager.air.dbId,
                astronAccountId,
                handleAccount,
                self.loginManager.air.dclassesByName["AstronAccountUD"],
                ("ACCESS_LEVEL",),
            )
            
    def storeAccountId(self, databaseId, accountId, callback):
        ## This is a stub function. It's not used in the current implementation.
        callback({"success": True})
