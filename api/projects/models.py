#############
# LIBRARIES #
#############
from django.conf import settings
from django.db import models

#############
# VARIABLES #
#############
User = settings.AUTH_USER_MODEL

# TYPES, ROLES AND PERMISSIONS FOR PROJECTS #
TYPE = (("Back-end", "Back-End"),
        ("Front-end", "Front-End"),
        ("Android", "Android"),
        ("IOS", "IOS"))
ROLE = (("Author", "Author"),
        ("Manager", "Manager"),
        ("Contributor", "Contributor"))
PERMISSION = (("All", "All"),
              ("Restricted", "Restricted"))

# PRIORITIES AND STATUS FOR ISSUES #
PRIORITY = (("Hight", "Hight"),
            ("Medium", "Medium"),
            ("Low", "Low"))
STATUS = (("To do", "To do"),
          ("In progess", "In progess"),
          ("Completed", "Completed"))

#############
# FUNCTIONS #
#############


class Project(models.Model):
    """
    Parameters for project(s)
    """
    title = models.CharField(max_length=50, blank=False, unique=True)
    description = models.CharField(max_length=500)
    type = models.CharField(max_length=9, choices=TYPE)
    author_user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    constraints = [models.UniqueConstraint(fields=['author_user_id', 'title'], name="unique_contributor")]

    class Meta:
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'

    def __str__(self):
        return self.title


class Contributor(models.Model):
    """
    Parameters for contributor(s)
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    permission = models.CharField(max_length=15, choices=PERMISSION, default="Restricted", editable=False)
    role = models.CharField(max_length=15, choices=ROLE, default="Contributor", editable=False)

    class Meta:
        verbose_name = 'Contributor'
        verbose_name_plural = 'Contributors'

    def __str__(self) -> str:
        return f"{self.user} - {self.role} - {self.project_id}"


class Issue(models.Model):
    """
    Parameters for issue(s)
    """
    priority = models.CharField(max_length=15, choices=PRIORITY)
    status = models.CharField(max_length=15, choices=STATUS)
    description = models.CharField(max_length=5000)
    title = models.CharField(max_length=50, unique=True)
    assignee_user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="assignee")
    author_user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author")
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Issue'
        verbose_name_plural = 'Issues'

    def __str__(self):
        return self.title


class Comment(models.Model):
    """
    Parameters for comment(s)
    """
    description = models.CharField(max_length=500, blank=False, unique=True)
    created_time = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    author_user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    issue_id = models.ForeignKey(Issue, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.description)
