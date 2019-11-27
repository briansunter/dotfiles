#fd - cd to selected directory
fd() {
  local dir
  dir=$(find ${1:-.} -path '*/\.*' -prune \
             -o -type d -print 2> /dev/null | fzf +m) &&
    cd "$dir"
}
fe() {
  local files
  IFS=$'\n' files=($(fzf-tmux --query="$1" --multi --select-1 --exit-0))
  [[ -n "$files" ]] && ${EDITOR:-vim} "${files[@]}"
}
vf() {
  local files
  IFS=$'\n' files=($(fzf-tmux --query="$1" --multi --select-1 --exit-0))
  [[ -n "$files" ]] && nvim "${files[@]}"
}

# ls extensions
export CLICOLOR=1
ls_ext() {
  if [ $# -eq 0 ]; then # if ls is called without any arguments
    # make ls print full info, with color
    ls -laF
  else
    ls $@ # otherwise call as intended
  fi
}

alias ls="ls_ext"

function killport() {
  lsof -i TCP:$1 | grep LISTEN | awk '{print $2}' | xargs kill -9
}
