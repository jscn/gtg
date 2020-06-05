# -----------------------------------------------------------------------------
# Getting Things GNOME! - a personal organizer for the GNOME desktop
# Copyright (c) 2008-2013 - Lionel Dricot & Bertrand Rousseau
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.
# -----------------------------------------------------------------------------

import os
import uuid

from GTG.backends.backend_signals import BackendSignals
from GTG.backends.generic_backend import GenericBackend
from GTG.backends.periodic_import_backend import PeriodicImportBackend
from GTG.backends.sync_engine import SyncEngine, SyncMeme
from GTG.core.task import Task
from GTG.core.translations import _
from GTG.core.logger import log

from caldav import DAVClient

"""
Backend for syncing with a CalDAV server.
"""


class Backend(PeriodicImportBackend):
    _general_description = {
        GenericBackend.BACKEND_NAME: "backend_caldav",
        GenericBackend.BACKEND_HUMAN_NAME: _("CalDAV"),
        GenericBackend.BACKEND_AUTHORS: ["Josh Crompton"],
        GenericBackend.BACKEND_TYPE: GenericBackend.TYPE_READWRITE,
        GenericBackend.BACKEND_DESCRIPTION:
        _("This backend syncs your GTG tasks with a CalDAV server."),
    }

    _static_parameters = {
        "period": {
            GenericBackend.PARAM_TYPE: GenericBackend.TYPE_INT,
            GenericBackend.PARAM_DEFAULT_VALUE: 5, },
        "username": {
            GenericBackend.PARAM_TYPE: GenericBackend.TYPE_STRING,
            GenericBackend.PARAM_DEFAULT_VALUE: 'Username', },
        "password": {
            GenericBackend.PARAM_TYPE: GenericBackend.TYPE_PASSWORD,
            GenericBackend.PARAM_DEFAULT_VALUE: '', },
        "calendar_name": {
            GenericBackend.PARAM_TYPE: GenericBackend.TYPE_STRING,
            GenericBackend.PARAM_DEFAULT_VALUE: '', },
        "service_url": {
            GenericBackend.PARAM_TYPE: GenericBackend.TYPE_STRING,
            GenericBackend.PARAM_DEFAULT_VALUE: 'http://example.com/username/UUID',
        },
    }

    def __init__(self, *args, **kwargs):
        """
        See GenericBackend for an explanation of this function.
        Re-loads the saved state of the synchronization
        """
        super().__init__(*args, **kwargs)
        # loading the saved state of the synchronization, if any
        self.data_path = os.path.join('caldav', 'sync_engine-' + self.get_id())
        self.sync_engine = self._load_pickled_file(self.data_path, SyncEngine())

    def save_state(self):
        """Save the state of the synchronization."""
        self._store_pickled_file(self.data_path, self.sync_engine)

    def do_periodic_import(self):
        # do the thing
        self.cancellation_point()
        client = DAVClient(
            url=self._parameters['service_url'],
            username=self._parameters['username'],
            password=self._parameter['password'],
        )
        # need the calendar name to get the right one.
        principal = client.principal()
        calendars = [calendar for calendar in principal.calendars() if calendar.name == self._parameters["calendar_name"]]
        if not any(calendars):
            # create one, i guess?
            pass
        calendar = calendars[0]
        
            
        
        # need some way to serialise the internal todo format to VTODO, and parse it back again.

        # # Establishing connection
        # try:
        #     self.cancellation_point()
        #     client = Client('%s/api/soap/mantisconnect.php?wsdl' %
        #                     self._parameters['service-url'])
        # except KeyError:
        #     self.quit(disable=True)
        #     BackendSignals().backend_failed(self.get_id(),
        #                                     BackendSignals.ERRNO_AUTHENTICATION
        #                                     )
        #     return

        # projects = client.service.mc_projects_get_user_accessible(
        #     self._parameters['username'],
        #     self._parameters['password'])
        # filters = client.service.mc_filter_get(self._parameters['username'],
        #                                        self._parameters['password'], 0)

        # # Fetching the issues
        # self.cancellation_point()
        # my_issues = []
        # for filt in filters:
        #     if filt['name'] == 'gtg':
        #         for project in projects:
        #             my_issues = client.service.mc_filter_get_issues(
        #                 self._parameters['username'],
        #                 self._parameters['password'],
        #                 project['id'],
        #                 filt['id'], 0, 100)
        #             for issue in my_issues:
        #                 self.cancellation_point()
        #                 self._process_mantis_issue(issue)
        # last_issue_list = self.sync_engine.get_all_remote()
        # new_issue_list = [str(issue['id']) for issue in my_issues]
        # for issue_link in set(last_issue_list).difference(set(new_issue_list)):
        #     self.cancellation_point()
        #     # we make sure that the other backends are not modifying the task
        #     # set
        #     with self.datastore.get_backend_mutex():
        #         tid = self.sync_engine.get_local_id(issue_link)
        #         self.datastore.request_task_deletion(tid)
        #         try:
        #             self.sync_engine.break_relationship(remote_id=issue_link)
        #         except KeyError:
        #             pass
        # return
