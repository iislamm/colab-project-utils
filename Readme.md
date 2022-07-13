# Colab Project Utils

Utility package to help you save your colab project files in your Google Drive account and fetch them back when you continue working on you project.

The goal of this project is to save you time while working on complex projects using Colab.

## Getting Started

#### 1. Mount Google Drive

```python
DRIVE_PATH = '/gdrive'
```

```python
from google.colab import drive
drive.mount(DRIVE_PATH)
```

    Drive already mounted at /gdrive; to attempt to forcibly remount, call drive.mount("/gdrive", force_remount=True).

#### 2. Download and import ColabUtils

```python
!wget https://raw.githubusercontent.com/islammohamedd1/colab-project-utils/main/colab_utils.py
```

```python
from colab_utils import ColabUtils
```

#### 3. Initialize ColabUtils

When you initialize ColabUtils, it will look if the project already exists in your Google Drive using the following path
`{drive_root}/{project_root}/{project_name}`
If the project exists, it will copy all the files to the current session storage.

```python
PROJECT_NAME = "Test Project"
PROJECT_ROOT = 'colab_projects'

cu = ColabUtils(PROJECT_NAME, DRIVE_PATH, PROJECT_ROOT)
```

    Initialized project Test Project using the following path: /gdrive/MyDrive/colab_projects/Test Project
    Project does not exist, creating new project
    Created project Test Project at /gdrive/MyDrive/colab_projects/Test Project

#### 4. Write a test file

```python
%%writefile test.py
print('hello world')
```

    Writing test.py

#### 5. Save the project

```python
cu.save_project()
```

    Saved project Test Project

Voila! Your project is now saved to your Google Drive account. When you start working on you project again, the files will be fetched automatically when you initialize the ColabUtils object as described in step 3
