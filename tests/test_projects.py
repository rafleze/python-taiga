from taiga.requestmaker import RequestMaker, RequestMakerException
from taiga.models.base import InstanceResource, ListResource
from taiga.models import User, Point, UserStoryStatus, Severity, Project, Projects
from taiga import TaigaAPI
import taiga.exceptions
import json
import requests
import unittest
from mock import patch
from .tools import create_mock_json
from .tools import MockResponse

class TestProjects(unittest.TestCase):

    @patch('taiga.requestmaker.RequestMaker.get')
    def test_single_project_parsing(self, mock_requestmaker_get):
        mock_requestmaker_get.return_value = MockResponse(200,
            create_mock_json('tests/resources/project_details_success.json'))
        api = TaigaAPI(token='f4k3')
        project = api.projects.get(1)
        self.assertEqual(project.description, 'test 1 on real taiga')
        self.assertEqual(len(project.users), 1)
        self.assertTrue(isinstance(project.points[0], Point))
        self.assertTrue(isinstance(project.us_statuses[0], UserStoryStatus))
        self.assertTrue(isinstance(project.severities[0], Severity))

    @patch('taiga.requestmaker.RequestMaker.get')
    def test_list_projects_parsing(self, mock_requestmaker_get):
        mock_requestmaker_get.return_value = MockResponse(200,
            create_mock_json('tests/resources/projects_list_success.json'))
        api = TaigaAPI(token='f4k3')
        projects = api.projects.list()
        self.assertEqual(projects[0].description, 'test 1 on real taiga')
        self.assertEqual(len(projects), 1)
        self.assertEqual(len(projects[0].users), 1)
        self.assertTrue(isinstance(projects[0].users[0], User))

    @patch('taiga.requestmaker.RequestMaker.post')
    def test_star(self, mock_requestmaker_post):
        rm = RequestMaker('/api/v1', 'fakehost', 'faketoken')
        project = Project(rm, id=1)
        self.assertEqual(project.star().id, 1)
        mock_requestmaker_post.assert_called_with(
            '/{endpoint}/{id}/star',
            endpoint='projects', id=1
        )

    @patch('taiga.requestmaker.RequestMaker.post')
    def test_unstar(self, mock_requestmaker_post):
        rm = RequestMaker('/api/v1', 'fakehost', 'faketoken')
        project = Project(rm, id=1)
        self.assertEqual(project.unstar().id, 1)
        mock_requestmaker_post.assert_called_with(
            '/{endpoint}/{id}/unstar',
            endpoint='projects', id=1
        )

    @patch('taiga.models.base.ListResource._new_resource')
    def test_create_project(self, mock_new_resource):
        rm = RequestMaker('/api/v1', 'fakehost', 'faketoken')
        mock_new_resource.return_value = Project(rm)
        sv = Projects(rm).create('PR 1', 'PR desc 1')
        mock_new_resource.assert_called_with(
            payload={'name': 'PR 1', 'description': 'PR desc 1'}
        )

    @patch('taiga.models.Priorities.create')
    def test_add_priority(self, mock_new_priority):
        rm = RequestMaker('/api/v1', 'fakehost', 'faketoken')
        project = Project(rm, id=1)
        project.add_priority('Priority 1')
        mock_new_priority.assert_called_with(1, 'Priority 1')

    @patch('taiga.models.Priorities.list')
    def test_list_priorities(self, mock_list_priorities):
        rm = RequestMaker('/api/v1', 'fakehost', 'faketoken')
        project = Project(rm, id=1)
        project.list_priorities()
        mock_list_priorities.assert_called_with(project=1)

    @patch('taiga.models.Severities.create')
    def test_add_severity(self, mock_new_severity):
        rm = RequestMaker('/api/v1', 'fakehost', 'faketoken')
        project = Project(rm, id=1)
        project.add_severity('Severity 1')
        mock_new_severity.assert_called_with(1, 'Severity 1')

    @patch('taiga.models.Severities.list')
    def test_list_severities(self, mock_list_severities):
        rm = RequestMaker('/api/v1', 'fakehost', 'faketoken')
        project = Project(rm, id=1)
        project.list_severities()
        mock_list_severities.assert_called_with(project=1)

    @patch('taiga.models.models.IssueTypes.create')
    def test_add_issue_type(self, mock_new_issue_type):
        rm = RequestMaker('/api/v1', 'fakehost', 'faketoken')
        project = Project(rm, id=1)
        project.add_issue_type('Severity 1')
        mock_new_issue_type.assert_called_with(1, 'Severity 1')

    @patch('taiga.models.models.IssueTypes.list')
    def test_list_issue_types(self, mock_list_issue_types):
        rm = RequestMaker('/api/v1', 'fakehost', 'faketoken')
        project = Project(rm, id=1)
        project.list_issue_types()
        mock_list_issue_types.assert_called_with(project=1)

    @patch('taiga.models.UserStoryStatuses.create')
    def test_add_us_status(self, mock_new_us_status):
        rm = RequestMaker('/api/v1', 'fakehost', 'faketoken')
        project = Project(rm, id=1)
        project.add_user_story_status('US status 1')
        mock_new_us_status.assert_called_with(1, 'US status 1')

    @patch('taiga.models.UserStoryStatuses.list')
    def test_list_us_statuses(self, mock_list_us_statuses):
        rm = RequestMaker('/api/v1', 'fakehost', 'faketoken')
        project = Project(rm, id=1)
        project.list_user_story_statuses()
        mock_list_us_statuses.assert_called_with(project=1)

    @patch('taiga.models.TaskStatuses.create')
    def test_add_task_status(self, mock_new_task_status):
        rm = RequestMaker('/api/v1', 'fakehost', 'faketoken')
        project = Project(rm, id=1)
        project.add_task_status('Task status 1')
        mock_new_task_status.assert_called_with(1, 'Task status 1')

    @patch('taiga.models.TaskStatuses.list')
    def test_list_task_statuses(self, mock_list_task_statuses):
        rm = RequestMaker('/api/v1', 'fakehost', 'faketoken')
        project = Project(rm, id=1)
        project.list_task_statuses()
        mock_list_task_statuses.assert_called_with(project=1)

    @patch('taiga.models.Points.create')
    def test_add_point(self, mock_new_point):
        rm = RequestMaker('/api/v1', 'fakehost', 'faketoken')
        project = Project(rm, id=1)
        project.add_point('Point 1', 1.5)
        mock_new_point.assert_called_with(1, 'Point 1', 1.5)

    @patch('taiga.models.Points.list')
    def test_list_points(self, mock_list_points):
        rm = RequestMaker('/api/v1', 'fakehost', 'faketoken')
        project = Project(rm, id=1)
        project.list_points()
        mock_list_points.assert_called_with(project=1)
