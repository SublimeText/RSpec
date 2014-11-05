# RSpec Package for Sublime Text 2/3

## Description

[RSpec](rspec) is a BDD (Behavior-Driven Development) testing framework for Ruby. This package adds support to Sublime Text 2 and 3 for specifying and testing Ruby applications with RSpec. It contains extra syntax highlighting and many snippets.

[rspec]: http://rspec.info/

## Installation

Recommended: install via [Package Control][package-control].

Alternative (especially if you want to develop the package further): Clone (your fork of) the repository into your Sublime Text Pacakges directory.

[package-control]: https://sublime.wbond.net/

## Features

* RSpec.tmLanguage: syntax rules sepcially for RSpec
   * RSpec plugin automatically uses *RSpec language syntax* when you are in a RSpec file
* RSpec.sublime-build: executing unit tests for the active module via the Sublime Text *Build* command
   * it chooses *RSpec* as the build command automatically when *RSpec* syntax is applied to the file
* Command to create a new module and the spec for the module at the same time
* Command to go to the corresponding spec / source file (shortcut: ctrl/command + .)
* Large amount of *RSpec* snippets
