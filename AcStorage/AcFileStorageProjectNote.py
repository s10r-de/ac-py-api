from AcFileStorageBaseClass import AcFileStorageBaseClass
from AcProjectNote import AcProjectNote
from ActiveCollabAPI import AC_CLASS_PROJECT_NOTE, AC_ERROR_WRONG_CLASS


class AcFileStorageProjectNote(AcFileStorageBaseClass):
    filename_prefix = "project-note"
    dir_name = "project-notes"

    def save(self, project_note: AcProjectNote, generate_id=None) -> str:
        assert project_note.class_ == AC_CLASS_PROJECT_NOTE, AC_ERROR_WRONG_CLASS
        return super().save(project_note)
