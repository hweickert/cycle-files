let s:plugin_python_dir = fnamemodify(resolve(expand('<sfile>:p')), ':h:h') . '/python'
pyx import sys, vim; sys.path.insert(0, vim.eval('s:plugin_python_dir')); import cycle_files.location_cycler
pyx import glob

function! CyclePaths(paths, ...)
    let l:forward = 1
    if len(a:000) > 1
        let l:forward = a:0
    endif
    pyx cycle_files.location_cycler.LocationCycler().cycle_paths(cycle_files.location_cycler.eval2py('a:paths'), vim.eval('l:forward'))
endfunction

function! CycleFileLocNext(...)
    pyx cycle_files.location_cycler.LocationCycler().cycle_locations()
endfunction

function! CycleFileLocPrevious(...)
    pyx cycle_files.location_cycler.LocationCycler().cycle_locations(False)'
endfunction

function! CycleFileSiblingNext()
    pyx cycle_files.location_cycler.LocationCycler().cycle_paths(sorted(glob.glob('./*')), True)
endfunction

function! CycleFileSiblingPrevious()
    pyx cycle_files.location_cycler.LocationCycler().cycle_paths(sorted(glob.glob('./*')), False)
endfunction
