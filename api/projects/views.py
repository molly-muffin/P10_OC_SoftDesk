#############
# LIBRARIES #
#############
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from django.conf import settings
from .serializers import ProjectSerializer, ContributorSerializer, IssueSerializer, CommentSerializer
from permissions import IsProjectOwner, ContributorPermission, IsContributorOrAuthor
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Project, Contributor, Issue, Comment
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import ValidationError
from django.http import Http404


#############
# VARIABLES #
#############
User = settings.AUTH_USER_MODEL


#############
# FUNCTIONS #
#############
class ProjectViewSet(ModelViewSet):
    """
    Create, retrieve, update and delete project(s).
    """
    queryset = Project.objects.all()
    permission_classes = [IsAuthenticated, IsProjectOwner]
    serializer_class = ProjectSerializer
    authentication_classes = [JWTAuthentication]

    def create(self, request, *args, **kwargs):
        """
        Create new project
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        project = serializer.save(author_user_id=self.request.user)
        Contributor.objects.create(user=request.user,
                                   project_id=project,
                                   role="Author",
                                   permission="All")
        return Response({'Project :': ProjectSerializer(project, context=self.get_serializer_context()).data,
                         'Message :': "Project successfully created !"},
                        status=status.HTTP_201_CREATED)

    def get_project(self):
        """
        Retrieve a project
        """
        current_project = self.kwargs["pk"]
        return get_object_or_404(Project, id=current_project)

    def update(self, request, *args, **kwargs):
        """
        Update a project
        """
        instance = self.get_object()
        if instance:
            serializer = self.get_serializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            project = serializer.save(author_user_id=self.request.user)
            return Response({'Project :': ProjectSerializer(project, context=self.get_serializer_context()).data,
                             'Message :': "Project successfully updated !"},
                            status=status.HTTP_202_ACCEPTED)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, *args, **kwargs):
        """
        Delete a project
        """
        instance = self.get_object()
        if instance:
            self.perform_destroy(instance)
            return Response({'Message :': "Project successfully deleted !"},
                            status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)


class ContributorViewSet(ModelViewSet):
    """
    Add, retrieve, update and delete contributor(s) in a project.
    """
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer
    permission_classes = [IsAuthenticated, ContributorPermission]
    authentication_classes = [JWTAuthentication]


    def create(self, request, *args, **kwargs):
        """
        Add a contributor in a project
        """
        serializer = self.get_serializer(data=request.data)
        current_project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        current_user = request.data['user']
        current_user_exist = Contributor.objects.filter(user=current_user, project_id=current_project)
        if current_user_exist:
            return Response({'Message :': "This contributor already exists !"},
                            status=status.HTTP_403_FORBIDDEN)
        else:
            serializer.is_valid(raise_exception=True)
            contribution = serializer.save(project_id=current_project)
            return Response({'Details :': ContributorSerializer(contribution,
                            context=self.get_serializer_context()).data,
                            'Message :': f"The new contributor is successfully added to the project : {current_project} !"},
                            status=status.HTTP_201_CREATED)

    def get_queryset(self):
        """
        Retrieve contributor(s) in a project
        """
        current_project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        return Contributor.objects.filter(project_id=current_project)

    def destroy(self, request, *args, **kwargs):
        """
        Delete a contributor in a project
        """
        try:
            get_object_or_404(Project, pk=self.kwargs['project_id'])
            contributor_to_delete = Contributor.objects.get(project_id=self.kwargs['project_id'],
                                                            user=self.kwargs['pk'])
            if contributor_to_delete.role == "Author":
                return Response({'Message :': "The author can't be deleted !"},
                                status=status.HTTP_403_FORBIDDEN)
            else:
                self.perform_destroy(contributor_to_delete)
                return Response({'Message :': "This contributor is successfully deleted !"},
                                status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist:
            raise ValidationError("This contributor doesn't exist !")


class IssueViewSet(ModelViewSet):
    """
    Create, retrieve, update and delete issue(s) of a project.
    """
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated, IsContributorOrAuthor]
    authentication_classes = [JWTAuthentication]


    def get_project(self):
        lookup_field = self.kwargs['project_id']
        return get_object_or_404(Project, id=lookup_field)

    def create(self, request, *args, **kwargs):
        """
        Add an issue for a project
        """
        serializer = self.get_serializer(data=request.data)
        try:
            current_project = get_object_or_404(Project, pk=self.kwargs['project_id'])
            serializer.is_valid(raise_exception=True)
            new_issue = serializer.save(author_user_id=self.request.user, project_id=current_project)
            return Response({'New issue': IssueSerializer(new_issue, context=self.get_serializer_context()).data,
                            'Message :': f"this issue is successfully added to the project : {current_project}"},
                            status=status.HTTP_201_CREATED)
        except ObjectDoesNotExist:
            raise Http404

    def get_queryset(self):
        """
        Retrieve issue(s) for a project
        """
        current_project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        return Issue.objects.filter(project_id=current_project).order_by('-last_updated')

    def destroy(self, request, *args, **kwargs):
        """
        Delete an issue for a project
        """
        instance = self.get_object()
        if instance:
            self.perform_destroy(instance)
            return Response(
                {'Message :': "this issue is successfully deleted"},
                status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)


class CommentViewSet(ModelViewSet):
    """
    Create, retrieve, update and delete a comment of an issue.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsContributorOrAuthor]
    authentication_classes = [JWTAuthentication]


    def get_project(self):
        lookup_field = self.kwargs['project_id']
        return get_object_or_404(Project, id=lookup_field)

    def create(self, request, *args, **kwargs):
        """
        Add a comment in an issue for a project
        """
        serializer = self.get_serializer(data=request.data)
        try:
            current_project = get_object_or_404(Project, pk=self.kwargs['project_id'])
            current_issue = get_object_or_404(Issue, pk=self.kwargs['issue_id'], project_id=current_project)
            if current_issue:
                serializer.is_valid(raise_exception=True)
                new_comment = serializer.save(author_user_id=self.request.user, issue_id=current_issue)
                return Response({'New comment': CommentSerializer(new_comment, context=self.get_serializer_context()).data,
                                'Message :': f"this comment is successfully added to the issue : {current_issue}"},
                                status=status.HTTP_201_CREATED)
        except ObjectDoesNotExist:
            raise Http404

    def get_queryset(self):
        """
        Retrieve comment(s) in an issue for a project
        """
        return Comment.objects.filter(issue_id=self.kwargs['issue_id']).order_by('-last_updated')

    def destroy(self, request, *args, **kwargs):
        """
        Delete a comment in an issue for a project
        """
        instance = self.get_object()
        if instance:
            self.perform_destroy(instance)
            return Response({'Message :': "this comment is successfully deleted"},
                            status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)
