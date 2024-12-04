from AcStorage.AcFileStorageBaseClass import AcFileStorageBaseClass
from active_collab_api.AcProjectNote import AcProjectNote
from active_collab_api import AC_CLASS_PROJECT_NOTE, AC_ERROR_WRONG_CLASS


class AcFileStorageProjectNote(AcFileStorageBaseClass):
    def __init__(self, root_path: str, account_id: int):
        super().__init__(root_path, account_id)
        self.filename_prefix = "project-note"
        self.dir_name = "project-notes"

    def setup(self):
        pass

    def save(self, project_note: AcProjectNote) -> str:
        assert project_note.class_ == AC_CLASS_PROJECT_NOTE, AC_ERROR_WRONG_CLASS
        return super().save_with_id(project_note, project_note.id)
