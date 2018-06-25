# Introduction
`cycle-files` uses pre-defined lists of locations to quickly jump between files in VIM.

This is useful if you have several similar file structures (like git clones or forks)
and you need to do comparisons between them.

# Example
Imagine your currently open VIM buffer has the file `/forkA/dir/file.txt` opened.
Your file system structure may look something like this:

* `/forkA/dir/file.txt`
* `/someDir/forkB/dir/file.txt`
* `/anotherDir/forkC/dir/file.txt`

By telling `cycle-files` about the three root locations,

* `/forkA`
* `/someDir/forkB`
* `/anotherDir/forkC`

the system can figure out how to jump from `/forkA/dir/file.txt` to `/someDir/forkB/dir/file.txt`
or from `/someDir/forkB/dir/file.txt` to `/anotherDir/forkC/dir/file.txt` (or in reverse if you like).

# Adding Locations
Set `g:cycle_files_location_maps` to define as many location maps as you like.

Below is a single location map defined matching the example above:
```
let g:cycle_files_location_maps = [['/forkA', '/someDir/forkB', '/anotherDir/forkC']]
```

By adding more sub-lists, you can define as many location maps as you like.

# Requirements
Your instance of VIM needs to be compiled with either `python` and/or `python3`.
Check the output of the `:version` command to see if one is available.

# Installation
## Linux/MacOS
```
git clone https://github.com/hweickert/cycle-files.git ~/.vim/pack/external/opt/cycle-files
```

In your `~/.vimrc` add the following.

```
packadd cycle-files

nmap <a-up>   :call CycleFileLocNext()<cr>
nmap <a-down> :call CycleFileLocPrevious()<cr>
```

## Windows
```
git clone https://github.com/hweickert/cycle-files.git ~/vimfiles/pack/external/opt/cycle-files
```

In your `%USERPROFILE%/_vimrc` add the following

```
packadd cycle-files

nmap <a-up>   :call CycleFileLocNext()<cr>
nmap <a-down> :call CycleFileLocPrevious()<cr>
```

# Usage
By using the mappings from the `Installation` section above, `Alt+Up` and `Alt+Down` will move you forwards / backwards between your defined locations.

