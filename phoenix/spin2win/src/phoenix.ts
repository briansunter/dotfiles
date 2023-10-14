import { pointInsideFrame } from './calc';
import { onKey } from './key';
import log from './logger';
import { Workspace } from './workspace';
import {
  getActiveScreen,
  workspaces,
  screens,
  windowMap,
  focusWindow,
  autoAddWindows,
  moveFocusedWindowToWorkspace,
  getActiveWorkspace,
  center,
  initScreens,
  mouseMoveFocus,
  setMouseMoveFocus,
  setAutoAddWindows,
} from './globals';
import { modKey, modKeyShift } from './config';


Phoenix.set({
  daemon: false,
  openAtLogin: true,
});

function getNextScreen(dir = 1) {
  let idx = screens.findIndex(s => s === getActiveScreen());
  return screens[Math.max(0, Math.min(screens.length - 1, idx + dir))];
}

function focusNextScreen(dir = 1) {
  let screen = getNextScreen(dir)
  if (screen.workspace?.windows.length) {
    focusWindow(screen.workspace.windows[0]);
  } else {
    Mouse.move(center(screen.screen.flippedFrame()));
  }
}

onKey('right', modKey, () => {
  focusNextScreen(1);
});
onKey('right', modKeyShift, () => {
  let ws = getNextScreen().workspace;
  if (!ws) {
    return;
  }
  moveFocusedWindowToWorkspace(ws.id);
  focusWindow(ws.windows[0]);
});
onKey('left', modKey, () => {
  focusNextScreen(-1);
});
onKey('left', modKeyShift, () => {
  let ws = getNextScreen(-1).workspace;
  if (!ws) {
    return;
  }
  moveFocusedWindowToWorkspace(ws.id);
  focusWindow(ws.windows[0]);
});
onKey('down', modKey, () => focusNextWindow());
onKey('j', modKey, () => focusNextWindow());

onKey('up', modKey, () => focusNextWindow(-1));
onKey('k', modKey, () => focusNextWindow(-1));


onKey('h', modKey, () => {
  getActiveWorkspace().mainRatio -= 0.1;
  getActiveWorkspace().render();
});
onKey('h', modKeyShift, () => {
  getActiveWorkspace().mainRatio -= 0.01;
  getActiveWorkspace().render();
});
onKey('l', modKey, () => {
  getActiveWorkspace().mainRatio += 0.1;
  getActiveWorkspace().render();
});
onKey('l', modKeyShift, () => {
  getActiveWorkspace().mainRatio += 0.01;
  getActiveWorkspace().render();
});

// Collect current window into active workspace.
onKey('return', modKey, () => {
  let window = Window.focused();
  if (window) {
    getActiveWorkspace().addWindow(window);
  }
});

onKey('return', modKeyShift, () => {
  let window = Window.focused();
  if (!window) {
    return;
  }
  for (let w of window.app().windows()) {
    if (!windowMap.has(w.hash())) {
      getActiveWorkspace().addWindow(w);  
    }
  }
});

onKey('delete', modKey, () => {
  let window = Window.focused();
  if (window) {
    getActiveWorkspace().removeWindow(window);
  }
});

onKey('c', modKeyShift, () => {
  let window = Window.focused();
  window?.close();
});

// Render focused window's workspace.
onKey('space', modKey, () => {
  let focused = Window.focused();
  if (!focused) {
    return;
  }
  let ws = workspaces.find(ws => focused && ws.findIndex(focused) != -1);
  if (ws) {
    getActiveScreen().activateWorkspace(ws.id);
  } else {
    getActiveScreen().vlog('No workspace for ' + focused.title(), false);
  }
});

// Rerender current screens.
onKey('space', modKeyShift, () => {
  let window = Window.focused();
  for (let s of screens) {
    s.workspace?.render();
    s.vlog('Rerendered');
  }
  focusWindow(window);
});

onKey('r', modKey, () => {
  getActiveWorkspace().spin();
});

onKey('r', modKeyShift, () => {
  let oldMousePos = Mouse.location();
  let screenWorkspaces = screens.map(s => s.workspace as Workspace);
  let back = screenWorkspaces.shift() as Workspace;
  screenWorkspaces.push(back);
  log(screenWorkspaces.map(w => w.id));
  screens.forEach((screen, i) => {
    log('setting SCREEN:' + screen.id + ' WINDOW: ' + screenWorkspaces[i].id);
    screen.setWorkspace(screenWorkspaces[i].id);
  });
  screens.forEach((screen) => {
    log('rendering SCREEN:' + screen.id + ' WINDOW: ' + screen.workspace?.id);
    screen.workspace?.render();
  });
  Mouse.move(oldMousePos);
});


onKey('m', modKey, () => {
  setMouseMoveFocus(!mouseMoveFocus);
});

onKey('a', modKey, () => {
  setAutoAddWindows(!autoAddWindows);
});


for (let i = 0; i <= 9; i++) {
  onKey(i.toString(), modKey, () => {
    let ws = workspaces[i];
    if (ws.screen) {
      let focused = Window.focused();
      let focusedScreen = getActiveScreen();
      log(focusedScreen.id);
      log(focused?.title());
      if (ws.screen !== focusedScreen) {
        ws.screen.vlog('Here ');
        focusedScreen.vlog('Already Showing ' + ws.id, false);
      } else {
        focusedScreen.vlog('This is');
      }
      ws.render();
      if (focusedScreen === ws.screen) {
        log(focusedScreen.id);
        focusWindow(ws.windows[0]);
      } else {
        log(focused?.title());
        focusWindow(focused);
      }

      return;
    }
    getActiveScreen().activateWorkspace(i);
  });
  onKey(i.toString(), modKeyShift, () => {
    moveFocusedWindowToWorkspace(i);
  });
}

function focusNextWindow(dir = 1) {
  let window = Window.focused();
  if (!window) {
    // TODO use mouse to figure our current screen?
    let screen = getActiveScreen();
    if (screen.workspace)
      screen.activateWorkspace(screen.workspace.id);
    return;
  }
  let hash = window.hash();
  let workspace = windowMap.get(hash);
  if (!workspace) {
    return;
  }
  let windows = workspace.windows;
  focusWindow(windows[(workspace.findIndex(window) + dir + windows.length) % windows.length]);
}

Event.on('screensDidChange', () => {
  initScreens();
});

Event.on('windowDidClose', (w) => {
  let ws = windowMap.get(w.hash());
  if (!ws) {
    return;
  }
  log('windowDidClose ' + w.title() + ' APPNAME: ' + w.app().name() + ' HASH: ' + w.hash() + ' removing from: ' + ws.id);
  ws.removeWindow(w);
});

Event.on('windowDidOpen', (w) => {
  log('windowDidOpen ' + w.title() + ' APPNAME: ' + w.app().name() + ' HASH: ' + w.hash() + ' adding to: ' + getActiveWorkspace().id);
  if (!w.isVisible() || windowMap.get(w.hash())) {
    return;
  }
  log('windowDidOpen ' + w.title() + ' APPNAME: ' + w.app().name() + ' HASH: ' + w.hash() + ' adding to: ' + getActiveWorkspace().id);
  // Phoenix modals shouldn't be part of our system.
  if (w.app().name() != 'Phoenix') {
    getActiveWorkspace().addWindow(w, true);
  }
});

Event.on('appDidLaunch', (a) => {
    log('appDidLaunch ' +a.name() + ' HASH: ' + a.hash() + ' adding to: ' + getActiveWorkspace().id);
    for (let w of a.windows()) {
    if (!w.isVisible() || windowMap.get(w.hash())) {
      return;
    }
    log('appDidLaunch ' + w.title() + ' APPNAME: ' + w.app().name() + ' HASH: ' + w.hash() + ' adding to: ' + getActiveWorkspace().id);
    // Phoenix modals shouldn't be part of our system.
    if (w.app().name() != 'Phoenix') {
      getActiveWorkspace().addWindow(w, true);
    }
  }
});

Event.on('appDidTerminate', (a) => {
  for (let w of a.windows()) {
    let ws = windowMap.get(w.hash());
    if (!ws) {
      return;
    }
    log('appDidTerminate ' + w.title() + ' APPNAME: ' + w.app().name() + ' HASH: ' + w.hash() + ' removing from: ' + ws.id);
    ws.removeWindow(w);
  }
});

Event.on('mouseDidMove', (p: any) => {
  if (!mouseMoveFocus || p.modifiers.find((m: string) => m === modKey[0])) {
    return;
  }

  let w = Window.recent().find(w => pointInsideFrame(p, w.frame()));
  w?.focus();
});

// Debug keys.
onKey('`', modKey, () => {
  for (let s of screens) {
    for (let w of s.workspace?.windows || []) {
      const m = new Modal();
      m.text = (s.workspace?.id.toString() || '') + ' ' + w.title();
      m.duration = 3;
      m.icon = w.app().icon();
      let modalBounds = m.frame();
      let windowBounds = w.frame();
      let origin = center(windowBounds);
      let screenBounds = s.screen.flippedFrame();
      let y = origin.y - screenBounds.y;
      y = screenBounds.height - y;
      origin.x -= modalBounds.width / 2;
      origin.y = y - modalBounds.height + s.screen.frame().y;
      m.origin = origin;
      m.show();
    }
  }
});

onKey('`', modKeyShift, () => {
  let w = Window.focused();
  if (!w) {
    return;
  }
  log('=============================================================');
  log(w.hash() + ' - ' + w.app.name + ' - ' + w.title());
  let loadState = Storage.get('state');
  log(loadState);
  log('=============================================================');
});
