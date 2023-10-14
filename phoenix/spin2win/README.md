# Phoenix configuration

This is my personal [Phoenix](https://github.com/kasper/phoenix) configuration, written in TypeScript and forked from [mafredri's config](https://github.com/mafredri/phoenix-config/).

## Overview
This config provides per-monitor virtual desktops. I use it with my laptop monitor + an external monitor. It's a reimplementation of my xmonad setup at work.

## Intended Usage
1. Use `modKey + Left/Right` to select a monitor
2. Use `modKey + 1-9`  to select a workspace
3. Use `modKeyShift + 1-9` to move windows between workspaces
4. Extra windows on a workspace are stacked to the side. Press `modKey + r` to cycle through the windows on a workspace.

This setup allows you assign your apps to workspaces, and quickly retrieve them wherever you're looking. And if you have a lot of Chrome windows like I do, you can just cycle through them to find the right one.

## Bindings
* `modKey + 1-9` Select workspace
* `modKeyShift + 1-9` Move focused window to workspace
* `modKey + Left/Right` Select left/right monitor
* `modKeyShift + Left/Right` Move active window to left/right monitor
* `modKey + r` Spin windows on current workspace
* `modKeyShift + r` Spin workspaces across monitors
* `modKey + h/l` Decrease/increase the main area size
* `modKey + up/down/j/k` Focus next/previous window on current workspace
* `modKey + return` Add focused window to current workspace
* `modKeyShift + return` Add all stray windows of focused app to current workspace (good for collecting apps on first run)
* `modKey + backspace` Remove focused window from workspace
* `modKeyShift + c` Close focused window
* `modKeyShift + space` Rerender current layout. Useful if you drag around windows and can't figure out what belongs where. Or if things go haywire.
* `modKey + a` Enable/disable auto-adding windows to current workspace (janky).
* `modKey + m` Enable/disable focus follow mouse (janky).

## Key bindings
The definition of `modKey` and `modKeyShift` can be found in [src/config.ts](src/config.ts). Otherwise modify keys in phoenix.ts.

## Notes
The active monitor is defined by the mouse position.

Focus follows the mouse but can be turned off temporarily by holding `modKey` or permanently in config.ts.

Some apps do random things on focus, like focusing all their windows. This whole thing is a bit janky. You might need custom hacks to get a good experience =( But it mostly works. Rerendering or mashing `modKey + Up/Down` fixes a lot of issues.

Weird interaction with holding down keys to show accented letters. Run `defaults write -g ApplePressAndHoldEnabled -bool false` and reboot to disable.

## Quick install
```
git clone https://github.com/nik3daz/spin2win.git
cd spin2win
ln -s `pwd`/out/phoenix.js ~/.phoenix.js 
```

## Building

```
git clone https://github.com/nik3daz/spin2win.git
cd spin2win
yarn install
yarn run build
```

The TypeScript compiler and Webpack will produce `out/phoenix.js` that can be used as Phoenix configuration. 

For development, `yarn start` will run Webpack in watch-mode. The window manager state is stored across reloads for better continuous development. Comment out the loadState() call if things get borked.

## Debugging

In a terminal, run:

```console
$ log stream --process Phoenix
```

Anything logged via logger (`import log from './logger';`) will show up as human friendly output in the terminal. `Phoenix.log` can also be used, but it only supports strings, much of the heavy lifting is already done by logger to create a similar experience to `console.log` in the browser.

You can also read about [Attaching to Web Inspector for Debugging](https://github.com/kasper/phoenix/wiki/Attaching-to-Web-Inspector-for-Debugging) in the Phoenix wiki. This gives access to true `console.log` and ability to use `debugger` statements in your code.
