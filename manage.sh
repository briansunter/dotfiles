#!/usr/bin/env bash
set -euxo pipefail 

symlinks=(
  emacs
  vim
  git
  zsh
  skhd
  node
)

install_brew() {
export PATH="/usr/local/bin:/usr/local/sbin:~/bin:$PATH"
  if ! [ -x "$(command -v brew)" ]; then
    echo "Installing Homebrew"
    /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
  fi
}

bootstrap() {
  pushd ${DOTFILES_HOME:-~/.dotfiles}
  install_brew
  brew update
  brew bundle

  echo "Setting up home"
  stow ${symlinks[@]}

  echo "Setting up macos"
  ./macos/bootstrap.sh

  echo "Installing node tools"
  pushd node
  npm install
  popd
  popd
}

if declare -f "$1" > /dev/null
then
  "$@"
else
  echo "'$1' is not a known function name" >&2
  exit 1
fi
