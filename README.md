# RSpec Package for Sublime Text

## Description

[RSpec][rspec] is a BDD (Behavior-Driven Development) testing framework for Ruby. This package adds support to Sublime Text for specifying and testing Ruby applications with RSpec. It contains extra syntax highlighting and many snippets.

[rspec]: https://rspec.info/

## Installation

Recommended: install via [Package Control][package-control].

[package-control]: https://packages.sublimetext.io/

Alternative (especially if you want to develop the package further): Clone (your fork of) the repository into your Sublime Text Packages directory.

## Key Bindings

RSpec does not define default key bindings to avoid conflicts with other packages. To add your own, open the Command Palette and execute "Preferences: RSpec Key Bindings".

## Features

* Syntax rules made specially for RSpec
   * RSpec plugin automatically uses *RSpec language syntax* when you are in a RSpec file
* RSpec (open spec).sublime-build: executing unit tests for the active module via the Sublime Text *Build* command
   * it chooses *RSpec* as the build command automatically when *RSpec* syntax is applied to the file
* RSpec (all specs).sublime-build: executing all unit tests for the active project via the Sublime Text *Build* command
* Command to create a new module and the spec for the module at the same time
* Command to go to the corresponding spec / source file (available in the Command Palette, can be configured to a keyboard shortcut)
* Large amount of *RSpec* snippets
* Symbol support: use Goto Symbol... inside an RSpec file and you will get a menu with the specification as you've defined it
   * You can also generate a structured document of a spec file with the "RSpec: Generate specification" command
