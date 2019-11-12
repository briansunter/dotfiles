#!/usr/bin/env bash

# map caps to esc
hidutil property --set '{"UserKeyMapping":[{"HIDKeyboardModifierMappingSrc":0x700000039,"HIDKeyboardModifierMappingDst":0x700000029}]}'

# show hidden files
defaults write com.apple.finder AppleShowAllFiles YES; killall Finder /System/Library/CoreServices/Finder.app

# normal scroll direction
defaults write -g com.apple.swipescrolldirection -bool FALSE
