class User():
    def __init__(self, user_json) -> None:
        '''
        Parse an instance of user json for data  
        '''
        self.user_id = user_json["user_id"],
        self.fname = user_json["fname"]
        self.lname = user_json["lname"]
        self.user_desc = user_json["user_desc"] if "user_desc" in user_json else ""
    
    def get_display_name(self) -> str:
        return self.fname + " " + self.lname[0] + "."