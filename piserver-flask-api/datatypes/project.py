
class Project():
    def __init__(self, project_data: dict) -> None:
        '''
        Parse an instance of user json for data 

        Expected input example:
        {
            project_id:   INTEGER NOT NULL,
            project_name: TEXT NOT NULL,
            project_desc: TEXT NOT NULL,
            created_on:   TEXT NOT NULL,
            github_link:  TEXT
        } 
        '''
        self.project_id = project_data["project_data"]
        self.project_name = project_data["project_name"]
        self.project_desc = project_data["project_desc"]
        self.created_on = project_data["created_on"]
        self.github_link = project_data["github_link"] if "github_link" in project_data else ""

