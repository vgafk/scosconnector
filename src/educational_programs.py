class EducationalProgram:
    external_id: str
    title: str
    direction: str
    code_direction: str
    start_year: str
    end_year: str

    def __init__(self, external_id: str, title: str, direction: str, code_direction: str, start_year: str,
                 end_year: str):
        self.external_id = external_id
        self.title = title
        self.direction = direction
        self.code_direction = code_direction
        self.start_year = start_year
        self.end_year = end_year

    @classmethod
    def from_list(cls, values):
        return cls(*values)

    # @classmethod
    # def load_from_file(cls, file_name: str):

