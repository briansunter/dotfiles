# Dev journal

## 28-06-21
Lockdown started 24/4 and it seems this will be my project.

Many simpsons episodes. Implemented simple window adding and rotaties.

Need to do some window hiding to make thing usable

Probably want to store all window hashes so that reloads maintain state

There's something weird about flipped coordinates to work on too. That should get abstracted.

MVP Feature list:
- new window added to current workspace, or apps to workspaces
- switch workspace and hide all other windows
- mod + r to rotate
- mod + left/right to focus monitor
- mod + 1-9 to render workspace 1-9 on active monitor
- mod + shift + left/right to move window to left/right monitor workspace

## 29-06-21
Boom shakalaka, making good headway.

The basic version works, but I think there might be some weird issues with automagically adding/removing windows. But maybe not.

Still haven't figured out if I should do something with existing windows, but declaring window bankruptcy for now!

Did a lot of organization too and played around a bit. I'll upload everything tomorrow.

I also need to make a non-mouse focus override (probably while pressing modKey). Holding cmd + tab works for now....

Also, I should do better at window order detection and rotation. And focus empty workspaces reasonably w/ mod + L/R.

## 30-06-21
Did those things.

Just need to do some startup experience stuff but that would mean shutting down my laptop :'(

Also may as well check the single window experience.

Add mod + space to activate workspace for focused window.

Gotta make an appDidLaunch and terminate handler because MacOSX doesn't understand that windows belong to apps????

## 05-07-21
Things mostly work, but there's a bunch of jank. Somehow I'm not receiving windowOpen events anymore.

I should add a key to 'unhide' all windows and to disable the hiding somehow.

I think this is in a reasonable state to publish, with a couple more controls for being able to wrangle broken states. This just needs some cleanup and we're good to go.

## 03-08-21
Adding a 'collect all windows of focused app onto active workspace' button.