#!/usr/bin/env bash
set -euxo pipefail 

symlinks=(
  emacs
  vim
  git
  zsh
  skhd
  node
  gpg
  phoenix
)

install_brew() {
export PATH="/usr/local/bin:/usr/local/sbin:~/bin:$PATH"
export PATH="/opt/homebrew/bin:$PATH"
  if ! [ -x "$(command -v brew)" ]; then
    echo "Installing Homebrew"
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

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
  export NVM_DIR=~/.nvm
  source "$(brew --prefix nvm)/nvm.sh"
  nvm install
  npm install
  popd

  echo "Set up Git Secrets $(pwd)"
  git secrets --register-aws --global
  git secrets --add-provider -- cat git/git-secrets-patterns.txt
  git secrets --install -f ~/.git-templates/git-secrets
  git config --global init.templateDir ~/.git-templates/git-secrets


  echo "scripts"
  pushd scripts
  echo "installing"
  poetry install
  echo "Installed"
  popd
}

if declare -f "$1" > /dev/null
then
  "$@"
else
  echo "'$1' is not a known function name" >&2
  exit 1
fi
