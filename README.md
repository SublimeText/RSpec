Description
===========
[RSpec](http://rspec.info/) is a BDD (Behavioral-Driven Development) testing framework for Ruby. This package adds support to Sublime Text 2 for testing Ruby applications with RSpec.

Package Installation
====================
Clone the repository in your Sublime Text 2 Pacakges directory.

Snippets
========

## Definitons
```Ruby
# desc
describe 'description' do
  ...
end

# con
context 'description' do
  ...
end

# it
it 'description' do
  ...
end

# iti
it { should ... }
```

## Fabricators
```Ruby
# letf
let(:fabricator) { Fabricate.build(:fabricator) }
```

## Expectations
All `exepect` snippets are prefixed with `exp`

```Ruby
# expeql
expect(subject).to eql(value)

# expinclude
expect(subject).to include(element)

# exphave
expect(subject).to have(num).items

# expbenil
expect(subject).to be_nil

# expbeclose
expect(subject).to be_close(result, tolerance)

# expraise
expect { action }.to raise_error(Error)

# expmatch
expect(subject).to match(/regexp/)

# expdo
expect do
    action
end.to matcher

# expexist
expect(subject).to exist
```

## Mocking

Features
========
* RSpec.sublime-build for executing unit tests for the active module via the S2 *Build* command
    * You must assign the builder for your project to 'Ceedling'
