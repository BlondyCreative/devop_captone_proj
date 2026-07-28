[nosetests]
with-spec=1
spec-color=1
with-coverage=1
cover-erase=1
cover-package=service

[coverage:run]
branch = True
source = service

[coverage:report]
show_missing = True
precision = 2
