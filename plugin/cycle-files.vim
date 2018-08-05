let s:plugin_python_dir = fnamemodify(resolve(expand('<sfile>:p')), ':h:h') . '/python'

let s:py_mode = 0
if has('python') == 1
    let s:py_mode = 'py '
python<<endpython
import sys, vim; sys.path.insert(0, vim.eval('s:plugin_python_dir')); import cycle_files.location_cycler
endpython
elseif has('python3') == 1
    let s:py_mode = 'py3 '
python3<<endpython
import sys, vim; sys.path.insert(0, vim.eval('s:plugin_python_dir')); import cycle_files.location_cycler
endpython
endif


function! s:validate_python()
    if s:py_mode is 0
        echo "Neither 'python' nor 'python3' are supported by this instance of VIM."
        return 0
    endif
    return 1
endfunction

function! CyclePaths(paths, ...)
    if !s:validate_python()
        return
    endif
    let l:forward = 1
    if len(a:000) > 1
        let l:forward = a:0
    endif
    execute s:py_mode . 'cycle_files.location_cycler.LocationCycler().cycle_paths(cycle_files.location_cycler.eval2py('.string(a:paths).'), '.l:forward.')'
endfunction

function! CycleFileLocNext(...)
    if !s:validate_python()
        return
    endif
    execute s:py_mode . 'cycle_files.location_cycler.LocationCycler().cycle_locations()'
endfunction

function! CycleFileLocPrevious(...)
    if !s:validate_python()
        return
    endif
    execute s:py_mode . 'cycle_files.location_cycler.LocationCycler().cycle_locations(False)'
endfunction




