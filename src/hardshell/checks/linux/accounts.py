import grp
import pwd
from dataclasses import dataclass

from src.hardshell.checks.base import BaseCheck
from src.hardshell.common.common import log_and_print


@dataclass
class AccountsCheck(BaseCheck):
    def check_groups(self, groups):
        log_and_print("checking groups", log_only=True)
        dupe_gids = 0
        dupe_names = 0
        group_names = set()
        group_gids = set()
        for group in groups:
            log_and_print(
                f"checking group {group['name']}",
                log_only=True,
            )
            if group["name"] in group_names:
                log_and_print(
                    f"duplicate group name found: {group['name']}", log_only=True
                )
                dupe_names += 1
            if group["gid"] in group_gids:
                log_and_print(f"duplicate GID found: {group['gid']}", log_only=True)
                dupe_gids += 1
            group_names.add(group["name"])
            group_gids.add(group["gid"])
        return dupe_gids, dupe_names

    def check_groups_exist(self, groups, users):
        log_and_print("checking all groups exist", log_only=True)
        group_names = {group["name"] for group in groups}
        group_exists = 0
        for user in users:
            log_and_print(
                f"checking user {user['name']}",
                log_only=True,
            )
            if user["name"] not in group_names:
                log_and_print(
                    f"User {user['name']} does not have a corresponding group",
                    log_only=True,
                )
                groups.append({"name": user["name"], "gid": user["gid"], "members": []})
                group_exists += 1
        return group_exists

    def check_users(self, users):
        log_and_print("checking users", log_only=True)
        dupe_names = 0
        dupe_uids = 0
        shadowed_password = 0
        user_names = set()
        user_uids = set()
        for user in users:
            if user["name"] in user_names:
                log_and_print(
                    f"duplicate user name found: {user['name']}", log_only=True
                )
                dupe_names += 1
            if user["uid"] in user_uids:
                log_and_print(f"duplicate UID found: {user['uid']}", log_only=True)
                dupe_uids += 1
            if user["passwd"] != "x":
                log_and_print(
                    f"user not using shadowed password: {user['name']}", log_only=True
                )
                shadowed_password += 1
            user_names.add(user["name"])
            user_uids.add(user["uid"])
        return dupe_names, dupe_uids, shadowed_password

    def check_root(self, users):
        log_and_print("checking root", log_only=True)
        root_gid = [user for user in users if user["name"] == "root"]
        root_gid_status = True if root_gid[0]["gid"] == 0 else False
        root_uids = [user for user in users if user["uid"] == 0]
        if len(root_uids) != 1:
            log_and_print(
                "error: there should be exactly one root user with uid 0", log_only=True
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
        log_and_print(f"checking local groups and users", log_only=True)

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

        # Set Results
        # Duplicate Groups
        self.set_result(
            self.check_id,
            self.check_name,
            "pass" if dupe_gids < 1 and dupe_names < 1 else "fail",
            "duplicate groups",
            self.check_type,
        )

        # Duplicate Users
        self.set_result(
            self.check_id,
            self.check_name,
            "pass" if dupe_names < 1 and dupe_uids < 1 else "fail",
            "duplicate users",
            self.check_type,
        )

        # Shadowed Passwords
        self.set_result(
            self.check_id,
            self.check_name,
            "pass" if shadowed_password < 1 else "fail",
            "shadowed passwords",
            self.check_type,
        )

        # Group Exists
        self.set_result(
            self.check_id,
            self.check_name,
            "pass" if group_exists < 1 else "fail",
            "all groups exist",
            self.check_type,
        )

        # Root User
        self.set_result(
            self.check_id,
            self.check_name,
            "pass" if root_gid_status else "fail",
            "root user gid 0",
            self.check_type,
        )
        self.set_result(
            self.check_id,
            self.check_name,
            "pass" if len(root_uids) == 1 else "fail",
            "root user uid 0",
            self.check_type,
        )
