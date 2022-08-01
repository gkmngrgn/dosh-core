VERSION = "0.1.0"


def make_exe():
    dist = default_python_distribution()
    policy = dist.make_python_packaging_policy()
    policy.extension_module_filter = "no-copyleft"

    # Controls whether the file scanner attempts to classify files and emit
    # resource-specific values.
    # policy.file_scanner_classify_files = True

    # Controls whether `File` instances are emitted by the file scanner.
    # policy.file_scanner_emit_files = False

    # Controls the `add_include` attribute of "classified" resources
    # (`PythonModuleSource`, `PythonPackageResource`, etc).
    # policy.include_classified_resources = True

    # Toggle whether Python module source code for modules in the Python
    # distribution's standard library are included.
    # policy.include_distribution_sources = False

    # Toggle whether Python package resource files for the Python standard
    # library are included.
    # policy.include_distribution_resources = False

    # Controls the `add_include` attribute of `File` resources.
    # policy.include_file_resources = False

    # Controls the `add_include` attribute of `PythonModuleSource` not in
    # the standard library.
    # policy.include_non_distribution_sources = True

    policy.include_test = False

    python_config = dist.make_python_interpreter_config()

    # Make the embedded interpreter behave like a `python` process.
    # python_config.config_profile = "python"

    # Set initial value for `sys.path`. If the string `$ORIGIN` exists in
    # a value, it will be expanded to the directory of the built executable.
    # python_config.module_search_paths = ["$ORIGIN/lib"]

    python_config.allocator_backend = "jemalloc"

    # Enable the use of a custom allocator backend with the "raw" memory domain.
    # python_config.allocator_raw = True

    # Enable the use of a custom allocator backend with the "mem" memory domain.
    # python_config.allocator_mem = True

    # Enable the use of a custom allocator backend with the "obj" memory domain.
    # python_config.allocator_obj = True

    # Enable the use of a custom allocator backend with pymalloc's arena
    # allocator.
    # python_config.allocator_pymalloc_arena = True

    # Automatically calls `multiprocessing.set_start_method()` with an
    # appropriate value when OxidizedFinder imports the `multiprocessing`
    # module.
    # python_config.multiprocessing_start_method = 'auto'

    # Do not call `multiprocessing.set_start_method()` automatically. (This
    # is the default behavior of Python applications.)
    # python_config.multiprocessing_start_method = 'none'

    # Call `multiprocessing.set_start_method()` with explicit values.
    # python_config.multiprocessing_start_method = 'fork'
    # python_config.multiprocessing_start_method = 'forkserver'
    # python_config.multiprocessing_start_method = 'spawn'

    # Control whether `oxidized_importer` is the first importer on
    # `sys.meta_path`.
    # python_config.oxidized_importer = False

    # Enable the standard path-based importer which attempts to load
    # modules from the filesystem.
    # python_config.filesystem_importer = True

    # Set `sys.frozen = False`
    # python_config.sys_frozen = False

    # Set `sys.meipass`
    # python_config.sys_meipass = True

    # Write files containing loaded modules to the directory specified
    # by the given environment variable.
    # python_config.write_modules_directory_env = "/tmp/oxidized/loaded_modules"

    python_config.run_command = "from dosh import cli; cli.run()"

    exe = dist.to_python_executable(
        name="dosh",
        packaging_policy=policy,
        config=python_config,
    )

    # Install tcl/tk support files to a specified directory so the `tkinter` Python
    # module works.
    # exe.tcl_files_path = "lib"

    # Never attempt to copy Windows runtime DLLs next to the built executable.
    # exe.windows_runtime_dlls_mode = "never"

    # Copy Windows runtime DLLs next to the built executable when they can be
    # located.
    # exe.windows_runtime_dlls_mode = "when-present"

    # Copy Windows runtime DLLs next to the build executable and error if this
    # cannot be done.
    # exe.windows_runtime_dlls_mode = "always"
    exe.windows_subsystem = "console"
    exe.add_python_resources(exe.read_package_root(path=".", packages=["dosh"]))
    return exe


def make_embedded_resources(exe):
    return exe.to_embedded_resources()


def make_install(exe):
    files = FileManifest()
    files.add_python_resource(".", exe)
    return files


def make_msi(exe):
    return exe.to_wix_msi_builder("dosh", "DOSH", VERSION, "Gökmen Görgen")


def register_code_signers():
    if not VARS.get("ENABLE_CODE_SIGNING"):
        return

    # Use a code signing certificate in a .pfx/.p12 file, prompting the
    # user for its path and password to open.
    # pfx_path = prompt_input("path to code signing certificate file")
    # pfx_password = prompt_password(
    #     "password for code signing certificate file",
    #     confirm = True
    # )
    # signer = code_signer_from_pfx_file(pfx_path, pfx_password)

    # Use a code signing certificate in the Windows certificate store, specified
    # by its SHA-1 thumbprint. (This allows you to use YubiKeys and other
    # hardware tokens if they speak to the Windows certificate APIs.)
    # sha1_thumbprint = prompt_input(
    #     "SHA-1 thumbprint of code signing certificate in Windows store"
    # )
    # signer = code_signer_from_windows_store_sha1_thumbprint(sha1_thumbprint)

    # Choose a code signing certificate automatically from the Windows
    # certificate store.
    # signer = code_signer_from_windows_store_auto()

    # Activate your signer so it gets called automatically.
    # signer.activate()


register_code_signers()

register_target("exe", make_exe)
register_target("resources", make_embedded_resources, depends=["exe"], default_build_script=True)
register_target("install", make_install, depends=["exe"], default=True)
register_target("msi_installer", make_msi, depends=["exe"])

resolve_targets()
