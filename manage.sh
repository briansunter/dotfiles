#!/usr/bin/env bash

symlinks=(
  emacs
  vim
  git
  zsh
)

setup_home() {
  echo "Setting up home"
  /usr/local/bin/stow ${symlinks[@]}
}

setup_macos() {
  echo "Setting up macos"
  ./macos/bootstrap.sh
}

install_brew() {
  if ! [ -x "$(command -v brew)" ]; then
    echo "Installing Homebrew"
    /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
  fi
}

bootstrap() {
  pushd ~/.dotfiles
  install_brew
  brew bundle
  setup_home
  setup_macos
  popd
}

if declare -f "$1" > /dev/null
then
  "$@"
else
  echo "'$1' is not a known function name" >&2
  exit 1
fi
