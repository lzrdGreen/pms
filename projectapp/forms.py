from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Project, Task, Tag

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description']
    
class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['project', 'name']

    def __init__(self, *args, **kwargs):
        project = kwargs.pop('project', None)
        super(TagForm, self).__init__(*args, **kwargs)


class TaskForm(forms.ModelForm):
    new_tags = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Add new tags (comma-separated)'}),
        required=False
    )

    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.none(),  # Start with an empty queryset
        widget=forms.CheckboxSelectMultiple,
        required=False
    )


    class Meta:
        model = Task
        fields = ['project', 'title', 'description', 'due_date', 'priority', 'status', 'parent_task', 'tags']

        widgets = {
            'priority': forms.Select(choices=Task.PRIORITY_CHOICES),
        }

    def __init__(self, *args, **kwargs):
        project = kwargs.pop('project', None)  # Extract project passed from view
        super(TaskForm, self).__init__(*args, **kwargs)

        # Only show the tags that are associated with the project
        if project:
            self.fields['tags'].queryset = project.tags.all()

        if project:
            # Filter to only include tasks from the same project and exclude the task being edited
            self.fields['parent_task'].queryset = Task.objects.filter(project=project).exclude(id=self.instance.id)
            self.fields['parent_task'].empty_label = f"Depends on project: {project.title}"           
            
        else:
            # If no project, don't show any tasks in parent_task dropdown
            self.fields['parent_task'].queryset = Task.objects.none()
            self.fields['tag'].widget = forms.Select(choices=[])

    def clean_parent_task(self):
        parent_task = self.cleaned_data.get('parent_task')
        if parent_task and parent_task == self.instance:
            raise forms.ValidationError("A task cannot depend on itself.")
        return parent_task

    def clean_due_date(self):
        due_date = self.cleaned_data.get('due_date')
        if due_date and due_date < timezone.now().date():
            raise ValidationError('Due date cannot be in the past.')
        return due_date
    
    def save(self, commit=True):
        # Save the task without committing any many-to-many relationships yet
        task = super().save(commit=False)  # Get the Task instance but don't save

        # Save the task first to make sure it gets a valid primary key (ID)
        task.save()  # This ensures task has an ID, crucial for many-to-many relationships

        # Now handle the tags (Many-to-Many field)
        tags = self.cleaned_data.get('tags')
        if tags:
            task.tags.set(tags)  # Set the tags (many-to-many) after saving the task
        
        # Handle new tags input
        new_tags = self.cleaned_data.get('new_tags')
        if new_tags:
            new_tags_list = [tag.strip() for tag in new_tags.split(',')]
            for tag_name in new_tags_list:
                tag, created = Tag.objects.get_or_create(name=tag_name, project=task.project)
                task.tags.add(tag)  # Add the new tag to the task's tags

        if commit:
            task.save()  # Commit changes after handling the tags

        return task

    """
    def save(self, commit=True):
        # Save the task without committing the many-to-many relationships yet
        task = super().save(commit=False)

        # Save the task first to ensure it gets a valid primary key (ID)
        task.save()

        # Handle the existing tags
        tags = self.cleaned_data.get('tags')
        if tags:
            task.tags.set(tags)  # Assign the selected tags

        # Handle new tags input
        new_tags = self.cleaned_data.get('new_tags')
        if new_tags:
            new_tags_list = [tag.strip() for tag in new_tags.split(',')]
            for tag_name in new_tags_list:
                # Create new tag for the specific project
                tag, created = Tag.objects.get_or_create(name=tag_name, project=task.project)
                task.tags.add(tag)  # Add the new tag to the task

        if commit:
            task.save()  # Commit the task after handling the tags

        return task
    """
    


