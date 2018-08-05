import os
import sys
import vim
import json
import operator
from cycle_files.cyclable_list import CyclableList



def eval2py(vim_expression):
    """ Converts the results of a vim expression to a python object and returns it. """
    return json.loads(vim.eval('json_encode({})'.format(vim_expression)))

class LocationCycler(object):
    def cycle_locations(self, forward=True):
        """ Cycles the current buffer between path lists defined in `g:cycle_files_location_maps`. """

        cycle_location_maps = self._get_cycle_location_maps()

        def normalize_path(p):
            result = os.path.realpath(p)
            if sys.platform == "win32":
                # on windows casing doesn't matter
                result = result.lower()
            return result

        def get_location_pattern_match_strengths(cur_path):
            cur_path = normalize_path(cur_path)
            result = []
            for location_pattern_list in cycle_location_maps:
                location_pattern_list = map(normalize_path, location_pattern_list)
                location_pattern_match_strength = 0
                for location_pattern in location_pattern_list:
                    if not cur_path.startswith(location_pattern):
                        continue
                    location_pattern_match_strength = max(location_pattern_match_strength, len(location_pattern))

                result.append(location_pattern_match_strength)

            return result

        def get_highest_match(location_pattern_match_strengths):
            index, value = max(enumerate(location_pattern_match_strengths), key=operator.itemgetter(1))
            return index, value

        def get_filepath_suffix(cur_path, location_pattern_list):
            cur_path = normalize_path(cur_path)
            location_pattern_list = map(normalize_path, location_pattern_list)

            for location_pattern in location_pattern_list:
                if not cur_path.startswith(location_pattern):
                    continue
                return cur_path[len(location_pattern):]
            return None

        cur_path = eval2py(r"expand('%: p')")
        location_pattern_match_strengths = get_location_pattern_match_strengths(cur_path)
        if not location_pattern_match_strengths:
            print(r"No parallel files found.")
            return

        index, value = get_highest_match(location_pattern_match_strengths)
        if value == 0:
            print(r"Can't cycle locations for current file.")
        fp_suffix = get_filepath_suffix(cur_path, cycle_location_maps[index])
        location_filepaths = [lp + fp_suffix for lp in cycle_location_maps[index]]

        self.cycle_paths(location_filepaths, forward=forward)

    def cycle_paths(self, paths, forward=True):
        if not paths:
            return
        curp = eval2py("expand('%:p')")
        if curp is None:
            curp = paths[-1]
        nextp = self._cycle_path(curp, paths, forward=forward)
        vim.command(r"edit {0}".format(nextp.rstrip()))

        # _close_buf previous file if it is part of the path list
        if self._curbuf_is_saved(curp):
            self._close_buf(curp)

    def _cycle_path(self, curpath, paths, forward=True):
        """ Cycles through `paths` returning the next one in the list of `paths`. """
        curpath = os.path.realpath(os.path.expandvars(curpath))
        paths = map(os.path.expandvars, paths)
        paths = map(os.path.realpath, paths)
        res = _cycle_list(paths, curpath, forward=forward, ignore_missing=True)
        return res

    def _curbuf_is_saved(self, p):
        result = p != ""
        return result

    def _close_buf(self, fp):
        if eval2py(r"bufexists('{0}')".format(fp)):
            vim.command("call lib#buffer#check_not_open_and_unsaved('{0}')".format(fp))

            # Query the buffer number first so 'bwipeout' works more reliably
            # than having paths with possibly special characters.
            bufnr = eval2py(r"bufnr('{0}')".format(fp))

            try:
                vim.command(r"bwipeout {0}".format(bufnr))
            except:
                vim.command(r"bdelete {0}".format(bufnr))
                print("warning: unable to wipe out buffer -> {0}".format(fp))

    def _get_cycle_location_maps(self):
        """ Translate the VIM variable `g:cycle_files_location_maps` to python. """

        try:
            res = eval2py('g:cycle_files_location_maps')
        except vim.error:
            # `g:cycle_files_location_maps` wasn't defined by the user.
            res = []
        return res


def _cycle_list(l, item, forward=True, ignore_missing=False):
    l_unique = []
    # Ensure the list of paths is unique.
    for p in l:
        if p in l_unique:
            continue
        l_unique.append(p)

    cl = CyclableList(l_unique)
    if forward:
        return cl.item_after(item, ignore_missing=ignore_missing)
    else:
        return cl.item_before(item, ignore_missing=ignore_missing)



