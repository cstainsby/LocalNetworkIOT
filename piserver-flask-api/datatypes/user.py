class User():
    def __init__(self, user_data) -> None:
        '''
        Parse an instance of user json for data 

        Expected input example:
        {
            user_id:   INTEGER NOT NULL,
            fname:     TEXT NOT NULL,
            lname:     TEXT NOT NULL,
            user_desc: TEXT
        } 
        '''
        self.user_id = user_data["user_id"],
        self.fname = user_data["fname"]
        self.lname = user_data["lname"]
        self.user_desc = user_data["user_desc"] if "user_desc" in user_data else ""
    
    def get_display_name(self) -> str:
        return self.fname + " " + self.lname[0] + "."