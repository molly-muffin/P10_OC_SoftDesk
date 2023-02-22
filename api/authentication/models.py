#############
# LIBRARIES #
#############
from django.contrib.auth.models import AbstractUser


#############
# FUNCTIONS #
#############
class User(AbstractUser):
    """
    Parameters for user(s)
    """
    def __str__(self):
        return str(self.username)
