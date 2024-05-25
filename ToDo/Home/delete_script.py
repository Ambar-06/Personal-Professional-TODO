from .models import TasksModel

def run_delete_script():
    tasks = TasksModel.objects.filter(is_deleted=None)
    for task in tasks:
        task.is_deleted = True
        task.save()
    return True