import pytest
from todoist_api_python.oop_models.oop_models import Project, Section, Task, Comment, Label, TodoistEnv
from todoist_api_python.api import TodoistAPI

@pytest.fixture(scope="module")
def api():
    with open("/home/thomas6785/todoist_api_token.txt", "r", encoding="utf8") as f:
        API_TOKEN = f.read().strip()
    return TodoistAPI(API_TOKEN)

@pytest.fixture(scope="module")
def env(api):
    return TodoistEnv(api)

@pytest.fixture(scope="module")
def project(env):
    proj = env.create_project("Test Project")
    yield proj
    proj.delete_project()

@pytest.fixture(scope="module")
def alternate_project(env):
    proj = env.create_project("Alternate Test Project")
    yield proj
    proj.delete_project()

@pytest.fixture(scope="module")
def section(project):
    return project.add_section("Test Section")

@pytest.fixture(scope="module")
def alternate_section(project):
    return project.add_section("Alternate Section")

@pytest.fixture(scope="module")
def task(section):
    ret = section.add_task("Test Task", description="This is a test task", labels=["testlabel"], priority=1)
    yield ret
    try:
        ret.delete_task()
    except:
        pass

@pytest.fixture(scope="function")
def fresh_task(section):
    ret = section.add_task("Fresh Task")
    yield ret
    try:
        ret.delete_task()
    except:
        pass

@pytest.fixture(scope="module")
def label(env):
    label = env.get_label_by_name("testlabel")
    yield label
    label.delete_label()

@pytest.fixture(scope="module")
def comment(fresh_task):
    return task.add_comment("This is a test comment")

def test_task_add_comment(task):
    comment = task.add_comment("Comment")
    assert isinstance(comment, Comment)
    assert comment.content == "Comment"

def test_task_labels(fresh_task):
    assert len(fresh_task.labels) == 0

    fresh_task.add_label("testlabel")
    assert "testlabel" in fresh_task.labels
    assert fresh_task.has_label("testlabel")
    assert not fresh_task.has_label("nonexistentlabel")

    fresh_task.remove_label("testlabel")
    assert "testlabel" not in fresh_task.labels
    assert not fresh_task.has_label("testlabel")
    assert not fresh_task.has_label("nonexistentlabel")

def test_task_labels_obj(fresh_task, label):
    assert len(fresh_task.labels) == 0

    fresh_task.add_label(label)
    assert label.name in fresh_task.labels
    assert fresh_task.has_label(label)
    assert fresh_task.has_label(label.name)
    assert not fresh_task.has_label("nonexistentlabel")

    fresh_task.remove_label(label)
    assert label.name not in fresh_task.labels
    assert not fresh_task.has_label(label)
    assert not fresh_task.has_label(label.name)
    assert not fresh_task.has_label("nonexistentlabel")

def test_task_add_subtask(task):
    subtask = task.add_subtask("Subtask")
    assert subtask.content == "Subtask"
    assert subtask.is_subtask
    assert subtask.get_parent_task() is task
    assert subtask._data.project_id == task._data.project_id

def test_task_mark_complete_incomplete(task):
    task.mark_complete()
    assert task.is_completed
    task.mark_incomplete()
    assert not task.is_completed

def test_task_get_comments(task):
    new_comment = task.add_comment("test comment abc123")
    comments = task.get_comments()
    assert new_comment in comments

def test_task_get_subtasks(task):
    new_subtask = task.add_subtask("Subtask 124")
    assert new_subtask.get_parent() is task
    subtasks = task.get_subtasks()
    assert new_subtask in subtasks

def test_task_move_task_project(task,alternate_project):
    assert task.get_project() is not alternate_project
    task.move_task(alternate_project)
    assert task.get_project() is alternate_project
    assert task.get_parent() is alternate_project

def test_task_move_task_section(task,alternate_section):
    assert task.get_section() is not alternate_section
    task.move_task(alternate_section)
    assert task.get_section() is alternate_section
    assert task.get_parent() is alternate_section

def test_task_move_task_parent(task):
    new_parent = task.add_subtask("New Parent Task")
    subtask = task.add_subtask("Child Task")
    assert subtask.get_parent() is task
    subtask.move_task(new_parent)
    assert subtask.get_parent() is new_parent

def test_task_set_content(task):
    task.set_content("New Content")
    assert task.content == "New Content"

def test_task_set_description(task):
    task.set_description("New Desc")
    assert task.description == "New Desc"

def test_task_set_priority(task):
    task.set_priority(3)
    assert task.priority == 3

def test_task_delete_task(fresh_task):
    proj = fresh_task.get_project()
    fresh_task.delete_task()
    assert fresh_task not in proj.get_tasks()

def test_task_get_parent_task(task):
    new_subtask = task.add_subtask("Subtask ABC 123")
    assert new_subtask.get_parent_task() is task

def test_task_get_section(fresh_task,section):
    assert fresh_task.get_section() is section

def test_task_get_project(fresh_task, project):
    assert fresh_task.get_project() is project
    assert fresh_task.get_project() is fresh_task.get_section().get_project()

def test_proj_color(project):
    assert project.color is not None
    project.set_color("blue")
    assert project.color == "blue"

def test_proj_set_name(project):
    project.set_name("New Project Name")
    assert project.name == "New Project Name"

def test_proj_archive_unarchive(project):
    assert not project.is_archived
    project.archive()
    assert project.is_archived
    project.unarchive()
    assert not project.is_archived

def test_proj_description(project):
    project.set_description("Project Description")
    assert project.description == "Project Description"
