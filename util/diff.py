# Standard Library Imports
from queue import Queue

# Third Party Imports

# Local Application Imports


class Diff:
    def __init__(self, dcmp):

        self.dcmp = dcmp

    def run(self):

        try:
            queue = Queue()
            queue.put(self.dcmp)
            diff_files, left_only, right_only = self._diff_iter(queue)
            if diff_files != None or left_only != None or right_only != None:
                raise DiffException(diff_files, left_only, right_only)
            return False
        except DiffException as e:
            print(
                f"## Diff Report between ##: \n# {self.dcmp.left} #\n# {self.dcmp.right} #"
            )
            print(e.message)
            return True

    @classmethod
    def _diff_iter(
        cls, dcmp_queue, diff_files=list(), left_only=dict(), right_only=dict()
    ):

        if dcmp_queue.empty():
            if not diff_files and not left_only and not right_only:
                return (None, None, None)
            else:
                return (diff_files, left_only, right_only)
        else:
            dcmp = dcmp_queue.get()
            if dcmp.diff_files:
                diff_files.extend(dcmp.diff_files)
            elif dcmp.left_only or dcmp.right_only:
                left_only[dcmp.left] = dcmp.left_only
                right_only[dcmp.right] = dcmp.right_only
            for (
                sub_dir_name,
                sub_dir_dcmp,
            ) in (
                dcmp.subdirs.items()
            ):  # key ==> common_dir string, value ==> dircmp object
                if sub_dir_name == ".git":
                    continue
                dcmp_queue.put(sub_dir_dcmp)
            return cls._diff_iter(dcmp_queue, diff_files, left_only, right_only)


class DiffException(Exception):
    def __init__(self, diff_files, left_only, right_only):
        self.message = f"Shared files differences: {str(diff_files)}\n"
        for (left_dir_name, left_dir_diff), (right_dir_name, right_dir_diff) in zip(
            left_only.items(), right_only.items()
        ):
            self.message += f"{left_dir_name} has exclusively: {str(left_dir_diff)}\n"
            self.message += f"{right_dir_name} has exclusively: {str(right_dir_diff)}\n"
