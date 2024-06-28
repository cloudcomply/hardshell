import grp
import pwd
from dataclasses import dataclass

from src.hardshell.checks.base import BaseCheck


@dataclass
class AccountsCheck(BaseCheck):
    def check_groups(self, groups):
        self.set_result_and_log_status(log_message="checking groups", log_only=True)
        dupe_gids = 0
        dupe_names = 0
        group_names = set()
        group_gids = set()
        for group in groups:
            self.set_result_and_log_status(
                log_message=f"checking group {group['name']}", log_only=True
            )
            if group["name"] in group_names:
                self.set_result_and_log_status(
                    log_message=f"duplicate group name found: {group['name']}",
                    log_only=True,
                )
                dupe_names += 1
            if group["gid"] in group_gids:
                self.set_result_and_log_status(
                    log_message=f"duplicate GID found: {group['gid']}", log_only=True
                )
                dupe_gids += 1
            group_names.add(group["name"])
            group_gids.add(group["gid"])
        return dupe_gids, dupe_names

    def check_groups_exist(self, groups, users):
        self.set_result_and_log_status(
            log_message="checking all groups exist", log_only=True
        )
        group_names = {group["name"] for group in groups}
        group_exists = 0
        for user in users:
            self.set_result_and_log_status(
                log_message=f"checking user {user['name']}", log_only=True
            )
            if user["name"] not in group_names:
                self.set_result_and_log_status(
                    log_message=f"User {user['name']} does not have a corresponding group",
                    log_only=True,
                )
                groups.append({"name": user["name"], "gid": user["gid"], "members": []})
                group_exists += 1
        return group_exists

    def check_users(self, users):
        self.set_result_and_log_status(log_message="checking users", log_only=True)
        dupe_names = 0
        dupe_uids = 0
        shadowed_password = 0
        user_names = set()
        user_uids = set()
        for user in users:
            if user["name"] in user_names:
                self.set_result_and_log_status(
                    log_message=f"duplicate user name found: {user['name']}",
                    log_only=True,
                )
                dupe_names += 1
            if user["uid"] in user_uids:
                self.set_result_and_log_status(
                    log_message=f"duplicate UID found: {user['uid']}", log_only=True
                )
                dupe_uids += 1
            if user["passwd"] != "x":
                self.set_result_and_log_status(
                    log_message=f"user not using shadowed password: {user['name']}",
                    log_only=True,
                )
                shadowed_password += 1
            user_names.add(user["name"])
            user_uids.add(user["uid"])
        return dupe_names, dupe_uids, shadowed_password

    def check_root(self, users):
        self.set_result_and_log_status(log_message="checking root", log_only=True)
        root_gid = [user for user in users if user["name"] == "root"]
        root_gid_status = True if root_gid[0]["gid"] == 0 else False
        root_uids = [user for user in users if user["uid"] == 0]
        if len(root_uids) != 1:
            self.set_result_and_log_status(
                log_message="error: there should be exactly one root user with uid 0",
                log_only=True,
            )
        return root_gid_status, root_uids

    def get_groups(self):
        all_groups = grp.getgrall()
        groups = []
        for group in all_groups:
            groups.append(
                {
                    "name": group.gr_name,
                    "gid": group.gr_gid,
                    "members": group.gr_mem,
                }
            )
        return groups

    def get_users(self):
        all_users = pwd.getpwall()
        users = []
        for user in all_users:
            users.append(
                {
                    "name": user.pw_name,
                    "uid": user.pw_uid,
                    "gid": user.pw_gid,
                    "dir": user.pw_dir,
                    "gecos": user.pw_gecos,
                    "passwd": user.pw_passwd,
                    "shell": user.pw_shell,
                }
            )
        return users

    def run_check(self, current_os, global_config):
        self.set_result_and_log_status(
            log_message=f"checking local groups and users", log_only=True
        )

        # get groups and users
        groups = self.get_groups()
        users = self.get_users()

        # check users and groups
        dupe_gids, dupe_names = self.check_groups(groups)
        dupe_names, dupe_uids, shadowed_password = self.check_users(users)

        # check all groups exist
        group_exists = self.check_groups_exist(groups, users)

        # check root user
        root_gid_status, root_uids = self.check_root(users)

        # Set Results and Log Status
        # Duplicate Groups
        self.set_result_and_log_status(
            check_id=self.check_id,
            check_message="duplicate groups",
            check_name=self.check_name,
            check_result="pass" if dupe_gids < 1 and dupe_names < 1 else "fail",
            check_type=self.check_type,
            log_message="",  # TODO
        )

        # Duplicate Users
        self.set_result_and_log_status(
            check_id=self.check_id,
            check_message="duplicate users",
            check_name=self.check_name,
            check_result="pass" if dupe_names < 1 and dupe_uids < 1 else "fail",
            check_type=self.check_type,
            log_message="",  # TODO
        )

        # Shadowed Passwords
        self.set_result_and_log_status(
            check_id=self.check_id,
            check_message="shadowed passwords",
            check_name=self.check_name,
            check_result="pass" if shadowed_password < 1 else "fail",
            check_type=self.check_type,
            log_message="",  # TODO
        )

        # Group Exists
        self.set_result_and_log_status(
            check_id=self.check_id,
            check_message="all groups exist",
            check_name=self.check_name,
            check_result="pass" if group_exists < 1 else "fail",
            check_type=self.check_type,
            log_message="",  # TODO
        )

        # Root User
        self.set_result_and_log_status(
            check_id=self.check_id,
            check_name=self.check_name,
            check_result="pass" if root_gid_status else "fail",
            check_message="root user gid 0",
            check_type=self.check_type,
            log_message="",  # TODO
        )
        self.set_result_and_log_status(
            check_id=self.check_id,
            check_message="root user uid 0",
            check_name=self.check_name,
            check_result="pass" if len(root_uids) == 1 else "fail",
            check_type=self.check_type,
            log_message="",  # TODO
        )
