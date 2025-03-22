from api.ApiConnector import ApiConnector
from otp.otpbase import OTPGlobals

class JWTAccountDB:
    def __init__(self, loginManager):
        self.loginManager = loginManager
        apiUrl = config.GetString('api-server', '')
        self.authApi = ApiConnector(apiUrl)

    def lookup(self, playToken, callback):
        response = self.authApi.validate_token(playToken)
        if not response.get("success"):
            callback({"success": False, "reason": response.get("reason")})
            return

        username = response.get("data", {}).get("username")
        astronAccountId = response.get("data", {}).get("astronId")

        if not astronAccountId:
            self.handle_missing_astron_account(username, callback)
        else:
            self.query_astron_account(astronAccountId, username, callback)

    def handle_missing_astron_account(self, username, callback):
        accessLevel = config.GetString("default-access-level", "NO_ACCESS")
        if accessLevel not in OTPGlobals.AccessLevelName2Int:
            self.loginManager.notify.warning(
                f'Access Level "{accessLevel}" isn\'t defined. Reverting back to NO_ACCESS'
            )
            accessLevel = "NO_ACCESS"
        
        callback({
            "success": True,
            "accountId": 0,
            "databaseId": username,
            "accessLevel": accessLevel,
        })

    def query_astron_account(self, astronAccountId, username, callback):
        def handle_account(dclass, fields):
            if dclass != self.loginManager.air.dclassesByName["AstronAccountUD"]:
                result = {
                    "success": False,
                    "reason": f"Your account object ({dclass}) was not found in the database!",
                }
            else:
                result = {
                    "success": True,
                    "accountId": astronAccountId,
                    "databaseId": username,
                    "accessLevel": fields.get("ACCESS_LEVEL", "NO_ACCESS"),
                }
            callback(result)

        # Query the account from Astron to verify its existence. We need to get
        # the ACCESS_LEVEL field anyways.
        # TODO: Add a timeout timer?
        self.loginManager.air.dbInterface.queryObject(
            self.loginManager.air.dbId,
            astronAccountId,
            handle_account,
            self.loginManager.air.dclassesByName["AstronAccountUD"],
            ("ACCESS_LEVEL",),
        )

    def storeAccountId(self, databaseId, accountId, callback):
        # This is a stub function. It's not used in the current implementation.
        callback({"success": True})
