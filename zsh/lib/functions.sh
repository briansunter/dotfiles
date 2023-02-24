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

unalias z 2> /dev/null
z() {
  [ $# -gt 0 ] && fasd_cd -d "$*" && return
  local dir
  dir="$(fasd -Rdl "$1" | fzf -1 -0 --no-sort +m)" && cd "${dir}" || return 1
}

function cd() {
  if [[ "$#" != 0 ]]; then
    builtin cd "$@";
    return
  fi
  while true; do
    local lsd=$(echo ".." && ls -p | grep '/$' | sed 's;/$;;')
    local dir="$(printf '%s\n' "${lsd[@]}" |
            fzf --reverse --preview '
                __cd_nxt="$(echo {})";
                __cd_path="$(echo $(pwd)/${__cd_nxt} | sed "s;//;/;")";
                echo $__cd_path;
                echo;
                ls -p "${__cd_path}";
        ')"
    [[ ${#dir} != 0 ]] || return 0
    builtin cd "$dir" &> /dev/null
  done
}

# c - browse chrome history
c() {
  local cols sep google_history open
  cols=$(( COLUMNS / 3 ))
  sep='{::}'

  if [ "$(uname)" = "Darwin" ]; then
    google_history="$HOME/Library/Application Support/Google/Chrome/Default/History"
    open=open
  else
    google_history="$HOME/.config/google-chrome/Default/History"
    open=xdg-open
  fi
  cp -f "$google_history" /tmp/h
  sqlite3 -separator $sep /tmp/h \
    "select substr(title, 1, $cols), url
     from urls order by last_visit_time desc" |
  awk -F $sep '{printf "%-'$cols's  \x1b[36m%s\x1b[m\n", $1, $2}' |
  fzf --ansi --multi | sed 's#.*\(https*://\)#\1#' | xargs $open > /dev/null 2> /dev/null
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

function init-git-secrets () {
    git secrets --install
    git secrets --register-aws
}

function setup-git-gpg () {
keybase pgp export | gpg --import
keybase pgp export --secret | gpg --allow-secret-key-import --import
}

function biggest-files (){
    count=20
    while getopts ":n:" opt; do
        case ${opt} in
            n )
                count=$OPTARG
                ;;
            \? )
                echo "Invalid option: $OPTARG" 1>&2
                ;;
            : )
                echo "Invalid option: $OPTARG requires an argument" 1>&2
                ;;
        esac
    done
    shift $((OPTIND -1))

    du -a . | sort -n -r | head -n $count
}

remove-all-files () {
    find . -delete
}

function take-picture (){
ffmpeg -f avfoundation -video_size 1920x1080 -framerate 30 -i "0" -vframes 1 out.jpg
}

function dote () {
  vim $( find  ~/.dotfiles -type f | fzf)
}

gif2mp4() {
  local output_folder=${2:-.}
  local output_file="$output_folder/${1%.*}.mp4"
  ffmpeg -i "$1" -movflags faststart -pix_fmt yuv420p -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" "$output_file"
}
mp42gif() {
  local output_folder=${2:-.}
  local output_file="$output_folder/${1%.*}.gif"
  ffmpeg -i "$1" \
  -vf "fps=10,scale=600:-2:flags=lanczos,split[s0][s1];\
[s0]palettegen=max_colors=128:reserve_transparent=0[p];\
[s1][p]paletteuse" \
-y "$output_file"

}

vidresize() {
  local width=${2:-"720"}
  local out_file="${1%.*}-${width}.${1##*.}"
  local height='trunc(ow/a/2)*2'
  ffmpeg -i "$1" -vf scale="$width:$height" "$out_file"
}

function rm-confirm() {
  # Check if the user has provided any arguments
  if [ $# -eq 0 ]; then
    echo "Usage: rm-confirm <file1> <file2> ..."
    return 1
  fi

  # Print the list of files to be deleted
  echo "The following files will be deleted:"
  for file in "$@"; do
    echo "$file"
  done

  # Ask for confirmation
  echo -n "Are you sure you want to delete these files? (y/n) "
  read answer
  if [ "$answer" != "y" ]; then
    echo "Aborting..."
    return 1
  fi

  # Delete the files
  command rm "$@"
}

