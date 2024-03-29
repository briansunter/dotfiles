# settings
export FUNCNEST=2000

export PATH="/opt/homebrew/bin:$PATH"
export PATH="/usr/local/bin:/usr/local/sbin:~/bin:$PATH"
export PATH="$HOME/.dotfiles/node/node_modules/.bin:$PATH"
## Terminal Vim Mode
bindkey -v
export KEYTIMEOUT=1

# aliases
export EDITOR='nvim'
alias vim='nvim'
alias ec='emacsclient -c'
alias simple-serve='python -m http.server 8000'
alias dot="$HOME/.dotfiles/manage.sh bootstrap"
alias getip="ipconfig getifaddr en1 || ipconfig getifaddr en0"
alias mergemd="find . -name '*.md' ! -name 'out.md' -exec cat {} + > out.md"
export PATH="$HOME/.dotfiles/scripts/scripts:$PATH"
# gpg
export GPG_TTY=$(tty)
gpgconf --launch gpg-agent

# history
HISTFILE="$HOME/.zsh_history"
HISTSIZE=10000000
SAVEHIST=10000000
setopt BANG_HIST                 # Treat the '!' character specially during expansion.
setopt EXTENDED_HISTORY          # Write the history file in the ":start:elapsed;command" format.
setopt INC_APPEND_HISTORY        # Write to the history file immediately, not when the shell exits.
setopt SHARE_HISTORY             # Share history between all sessions.
setopt HIST_EXPIRE_DUPS_FIRST    # Expire duplicate entries first when trimming history.
setopt HIST_IGNORE_DUPS          # Don't record an entry that was just recorded again.
setopt HIST_IGNORE_ALL_DUPS      # Delete old recorded entry if new entry is a duplicate.
setopt HIST_FIND_NO_DUPS         # Do not display a line previously found.
setopt HIST_IGNORE_SPACE         # Don't record an entry starting with a space.
setopt HIST_SAVE_NO_DUPS         # Don't write duplicate entries in the history file.
setopt HIST_REDUCE_BLANKS        # Remove superfluous blanks before recording entry.
setopt HIST_VERIFY               # Don't execute immediately upon history expansion.
setopt HIST_BEEP   

# antibody
source <(antibody init)
antibody bundle < ~/.dotfiles/zsh/lib/zsh_plugins.txt

# completions
autoload -U compinit && compinit

# NVM
export NVM_DIR=~/.nvm
source "$(brew --prefix nvm)/nvm.sh"

# FZF
if test -d /usr/local/opt/fzf/shell; then
  . /usr/local/opt/fzf/shell/key-bindings.zsh
  . /usr/local/opt/fzf/shell/completion.zsh
else
  bindkey '^R' history-incremental-search-backward
fi

# fasd init
fasd_cache="$HOME/.fasd-init-bash"
if [ "$(command -v fasd)" -nt "$fasd_cache" -o ! -s "$fasd_cache" ]; then
  fasd --init posix-alias zsh-hook zsh-ccomp zsh-ccomp-install >| "$fasd_cache"
fi
source "$fasd_cache"
unset fasd_cache

# functions
. ~/.dotfiles/zsh/lib/functions.sh

test -f ~/.dotfiles/zsh/.localrc && source ~/.dotfiles/zsh/.localrc

export GOPATH=$HOME/go
export GOBIN=$GOPATH/bin
export PATH=$PATH:$GOBIN
export PATH=$PATH:$GOROOT/bin
eval "$(github-copilot-cli alias -- "$0")"

export PYENV_ROOT="$HOME/.pyenv"
command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"

# pnpm
export PNPM_HOME="/Users/bsunter/Library/pnpm"
export PATH="$PNPM_HOME:$PATH"
# pnpm end
# >>> conda initialize >>>
# !! Contents within this block are managed by 'conda init' !!
__conda_setup="$('/Users/bsunter/miniforge3/bin/conda' 'shell.zsh' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    if [ -f "/Users/bsunter/miniforge3/etc/profile.d/conda.sh" ]; then
        . "/Users/bsunter/miniforge3/etc/profile.d/conda.sh"
    else
        export PATH="/Users/bsunter/miniforge3/bin:$PATH"
    fi
fi
unset __conda_setup

if [ -f "/Users/bsunter/miniforge3/etc/profile.d/mamba.sh" ]; then
    . "/Users/bsunter/miniforge3/etc/profile.d/mamba.sh"
fi
# <<< conda initialize <<<

