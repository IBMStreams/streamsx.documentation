# How to add documentation

You can edit the documentation and create a pull request to submit your changes.

To preview the changes you've made, you can clone the repository and run Jekyll which will give you a local copy of the documentation site.


- [Install Jekyll](https://jekyllrb.com/docs/installation/)
- Clone this repository
- From a terminal window,
    ```
    cd streamsx.documentation
    jekyll serve
    ```
  This should produce some output:
  ```
    Configuration file: /Users/n.../streamsx.documentation/_config.yml
              Source: /Users/n.../streamsx.documentation
         Destination: /Users/.../streamsx.documentation/_site
   Incremental build: disabled. Enable with --incremental
        Generating...
                      done in 9.221 seconds.
          MORE INFO: https://github.com/guard/listen/wiki/Duplicate-directory-errors
   Auto-regeneration: enabled /Users/..../streamsx.documentation43
      Server address: http://127.0.0.1:4000/streamsx.documentation/
    Server running... press ctrl-c to stop.
  ```
Go to `127.0.0.1:4000/streamsx.documentation/` to preview your changes.
