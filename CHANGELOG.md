### 2.0.1

* Removed `ctrl+atl+n` keymap (command: `rspec_create_module`)
* Added a new build file that uses `bundle exec`

### 2.0.0

* Fixed and improved new module-spec pair creation

### 2014-11-07

* Minor typo / quotes fixes

### 2014-11-06

* Package switched to use tag release

### 2014-11-05

* Added the ability to find the spec/source file when multiple "root" folders exist in the project

### 2014-11-04

* Build in spec file now auto choose rspec build (Thanks @osrocha)
* Added feature and scenario snippets (Thanks @jaredmoody)
* "subject" and "let" now highlight correctly, words like "subjective" and "letter" are no longer half highlighted
* Saving new file with RSpec filetype no longer prompts with ".spec.rb", not it's ".rb"
* Added "create new module" command to command palette, planning to remove the key binding <ctrl/super+alt+n>
