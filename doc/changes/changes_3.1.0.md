# 3.1.0 - 2025-06-23

This release fixes a bug that prevented the rebuild from being triggered correctly when a user included the string [rebuild] in the commit message. Also, the nightly checks run always for all flavors.

## Bugs

 - #143: Fixed rebuild commit message for PR

## Refactorings

 - #145: Run all flavors for nightly checks
