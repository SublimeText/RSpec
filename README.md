Description
===========
[RSpec](http://rspec.info/) is a BDD (Behavioral-Driven Development) testing framework for Ruby. This package adds support to Sublime Text 2 for testing Ruby applications with RSpec.

Package Installation
====================
Clone the repository in your Sublime Text 2 Pacakges directory.

Snippets
========


```Ruby
# desc
describe 'description' do
  ...
end
```

```Ruby
# con
context 'description' do
  ...
end
```

Features
========
* RSpec.sublime-build for executing unit tests for the active module via the S2 *Build* command
    * You must assign the builder for your project to 'Ceedling'
