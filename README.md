# find-ansible-modules

**Simple Python script for finding modules used in Ansible playbooks or task files.**

## Requirements

Python 3.8 or higher.

## Example Usage

The script expects filenames with a `.yml` or `.yaml` extension as arguments.  

Using `find` and `xargs` we can feed a list of files to it:

```
cd my-role
find . -type f \( -name "*.yml" -o -name "*.yaml" \) | xargs ~/path/to/find-ansible-modules.py
```

Alternatively, specify the files on the cmdline:

```
cd my-role
~/path/to/find-ansible-modules.py tasks/main.yml tasks/myOtherTasksFile.yaml
```

## License

Licensed under [MIT License](https://opensource.org/licenses/MIT).
See [LICENSE](https://github.com/brycech/find-ansible-modules/blob/master/LICENSE) file in repository.
