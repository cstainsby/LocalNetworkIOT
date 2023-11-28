
class Project():
    def __init__(self) -> None:
        '''
        Parse an instance of user json for data 

        Expected input example:
        {
            project_name: TEXT PRIMARY KEY,
            project_desc: TEXT NOT NULL,
            created_on:   TEXT NOT NULL,
            github_link:  TEXT
        } 
        '''
        self.title = ""
        self.desc = ""
        self.created_on = ""
        self.github_link = None
    
    def inflate_from_sqlLite_row(self, data: list):
        self.title = data[0]
        self.desc = data[1]
        self.created_on = data[2]
        self.github_link = data[3]
    
    def to_template_data_format(self) -> dict:
        template_data = {
            "title": self.title,
            "desc": self.desc,
            "created_on": self.created_on,
        }
        if self.github_link:
            template_data["github_link"] = self.github_link

        return template_data

