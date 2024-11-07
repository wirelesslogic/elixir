Module core.config
==================

Functions
---------

    
`env_constructor(loader, node)`
:   

    
`get_base_name(input_path)`
:   

    
`get_file_type(input_path)`
:   

    
`include_constructor(loader, node)`
:   Include file referenced at node.

    
`load_config_into(sub_config, key, file)`
:   

    
`load_module_configs(directory, config)`
:   Load config.yml files from direct subdirectories of the given directory
    and merges them under their respective module names in the main config.

    
`recursive_load(sub_config, directory, parent_key=None)`
:   

    
`setup_config()`
:   

Classes
-------

`CustomLoader(stream)`
:   Initialize the scanner.

    ### Ancestors (in MRO)

    * yaml.loader.SafeLoader
    * yaml.reader.Reader
    * yaml.scanner.Scanner
    * yaml.parser.Parser
    * yaml.composer.Composer
    * yaml.constructor.SafeConstructor
    * yaml.constructor.BaseConstructor
    * yaml.resolver.Resolver
    * yaml.resolver.BaseResolver

    ### Class variables

    `yaml_constructors`
    :