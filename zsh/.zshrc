# settings
export PATH="/usr/local/bin:/usr/local/sbin:~/bin:$PATH"
export PATH="$HOME/.dotfiles/node/node_modules/.bin:$PATH"
## Terminal Vim Mode
bindkey -v
export KEYTIMEOUT=1

# aliases
export EDITOR='nvim';
alias ec='emacsclient -c'
alias simple-serve='python -m SimpleHTTPServer 8000'
alias dot="$HOME/.dotfiles/manage.sh bootstrap"

# history
HISTFILE=~/.zsh_history
HISTSIZE=999999999
SAVEHIST=$HISTSIZE

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
