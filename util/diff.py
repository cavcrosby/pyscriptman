"""The class module for diff and related classes.

The purpose of this module is to replicate the Unix
program 'diff' found in diffutils. Also look at 'See Also'
in the Diff class.

"""
# Standard Library Imports
from queue import Queue

# Third Party Imports

# Local Application Imports


class Diff:
    """The class Diff.

    Parameters
    ----------
    dcmp : filecmp.dircmp
        A new directory comparsion object.

    See Also
    --------
    https://www.gnu.org/software/diffutils/

    """

    def __init__(self, dcmp):

        self.dcmp = dcmp

    def run(self):
        """Checking for differences between two directories.
        
        Returns
        -------
        bool
            Whether or not any differences exist between
            the two directories.
        
        """
        try:
            queue = Queue()
            queue.put(self.dcmp)
            diff_files, left_only, right_only = self._diff_iter(queue)
            if (
                diff_files is not None
                or left_only is not None
                or right_only is not None
            ):
                raise DiffException(diff_files, left_only, right_only)
            return False
        except DiffException as e:
            print(
                f"## Diff Report between ##: \n# {self.dcmp.left} #\n# {self.dcmp.right} #"
            )
            print(e.message)
            return True

    @classmethod
    def _diff_iter(cls, dcmp_queue, diff_files=None, left_only=None, right_only=None):
        """Iteration over the entire directory tree occurs here.

        Parameters
        ----------
        dcmp_queue : queue.Queue of filecmp.dircmp objects
            This is a collection of comparsion objects to iterate over.
        diff_files : list of str
            Each file that is different is recorded.
        left_only, right_only : dict of str, str
            This is to record what file was different
            and which directory did it belong to.
        
        Returns
        -------
        (diff_files, left_only, right_only)
            Once the recursion is over, the final results
            are stored in to a tuple.
        (None, None, None)
            Incase no differences were found between the
            directories.
        
        """
        if diff_files is None:
            diff_files = list()
        if left_only is None:
            left_only = dict()
        if right_only is None:
            right_only = dict()
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
    """Custom exception that formats the body of the diff message.
    
    Error reporting title is printed out by the
    Diff class.

    """

    def __init__(self, diff_files, left_only, right_only):
        self.message = f"Shared files differences: {str(diff_files)}\n"
        for (left_dir_name, left_dir_diff), (right_dir_name, right_dir_diff) in zip(
            left_only.items(), right_only.items()
        ):
            self.message += f"{left_dir_name} has exclusively: {str(left_dir_diff)}\n"
            self.message += f"{right_dir_name} has exclusively: {str(right_dir_diff)}\n"
        super().__init__(self.message)
