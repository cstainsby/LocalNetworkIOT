
class Project():
    def __init__(self, data: dict = None) -> None:
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

        if data is not None:
            self.title = data["title"] 
            self.desc = data["desc"] 
            self.created_on = data["created_on"] 
            self.github_link = data["github_link"] if "github_link" in data else None
    
    def to_template_data_format(self) -> dict:
        template_data = {
            "title": self.title,
            "desc": self.desc,
            "created_on": self.created_on,
        }
        if self.github_link:
            template_data["github_link"] = self.github_link

        return template_data

