import os
import shutil


class ColabUtils:
    """
    Colab Utils is a utility class that helps you to save the files in your project's session storage to you Google Drive account.
    If you have any modules and/or data files in you working directory and don't want to lose them when your runtime resets,
    you can save the files to your Google Drive account and fetch them back when you restart your runtime to the current session storage.
    """

    __default_files = [
        "sample_data",
        ".config",
        ".ipynb_checkpoints",
        "__pycache__",
    ]

    def __init__(
        self, project_name: str, drive_root: str, project_drive_root: str
    ):
        """
        Initializes the ColabUtils class.

        Parameters:
            project_name: The name of the project. This name will be used to name the project directory
            drive_root: The root directory of your Google Drive account.
            project_drive_root: The parent directory of your project in google drive. The project will be saved in the following path: drive_root/project_drive_root/project_name
        """
        self.project_name = project_name
        self.project_drive_root = project_drive_root
        self.drive_root = self.__load_drive_root_path(drive_root)
        self.__project_path = os.path.join(
            self.drive_root, project_drive_root, project_name
        )

        print(
            f"Initialized project {self.project_name} using the following path: {self.__project_path}"
        )

        self.fetch_project()

    def __load_drive_root_path(self, drive_root: str):
        """
        Loads the drive root path.

        Parameters:
            drive_root: The drive root path.
        """
        if not os.path.exists(drive_root) or not os.path.isdir(drive_root):
            raise FileNotFoundError(
                "The drive root path does not exist. Please check the path and try again."
            )

        if "MyDrive" not in drive_root:
            drive_root = os.path.join(drive_root, "MyDrive")

        return drive_root

    def __is_drive_root(self, file: str):
        """
        Checks if the file path is the drive root directory. Prevents recursive copying of files.

        Parameters:
            file: The file path to check.
        """
        if file == self.drive_root or os.path.abspath(file) == os.path.abspath(
            self.drive_root
        ):
            return True

    def __copy_files(self, files: list, dest: str, override: bool = False):
        """
        Copies the files to the destination.
        """
        for f in files:
            filename = os.path.basename(f)
            # check if the file exists
            if os.path.exists(os.path.join(dest, filename)):
                if override:
                    os.remove(os.path.join(dest, filename))
                else:
                    continue
            if os.path.isdir(f):
                shutil.copytree(f, os.path.join(dest, filename))
            else:
                shutil.copy(f, os.path.join(dest, filename))

    def save_project(self, ignore_files: list = None):
        """
        Saves the project to your Google Drive account.

        Parameters:
            ignore_files: A list of files to ignore when saving the project.
            The following list is excluded by default: ['sample_data', '.config', '.ipynb_checkpoints', "__pycache__"]
        """
        if not os.path.exists(self.__project_path):
            os.makedirs(self.__project_path)

        if ignore_files is None:
            ignore_files = []

        ignore_file_list = self.__default_files + ignore_files
        files = os.listdir(".")
        files = [
            f
            for f in files
            if f not in ignore_file_list and not self.__is_drive_root(f)
        ]

        if len(files):
            self.__copy_files(files, self.__project_path, override=True)

        print(f"Saved project {self.project_name} at {self.__project_path}")

    def fetch_project(self):
        """
        Fetches the project from your Google Drive account.
        """

        if os.path.exists(self.__project_path):
            print(f"Project already exists, fetching files")

            files = os.listdir(self.__project_path)
            files = [os.path.join(self.__project_path, f) for f in files]

            if len(files):
                self.__copy_files(files, ".")

            print(f"Fetched project {self.project_name}")
        else:
            print(f"Project does not exist, creating new project")

            os.makedirs(self.__project_path)

            print(
                f"Created project {self.project_name} at {self.__project_path}"
            )
