VERSION = "0.1.0"


def make_exe():
    dist = default_python_distribution()
    policy = dist.make_python_packaging_policy()
    policy.extension_module_filter = "no-copyleft"

    # Toggle whether Python module source code for modules in the Python
    # distribution's standard library are included.
    # policy.include_distribution_sources = False

    # Toggle whether Python package resource files for the Python standard
    # library are included.
    # policy.include_distribution_resources = False

    # Controls the `add_include` attribute of `File` resources.
    # policy.include_file_resources = False

    policy.include_non_distribution_sources = False
    policy.include_test = False

    python_config = dist.make_python_interpreter_config()
    python_config.allocator_backend = "jemalloc"
    python_config.run_command = "from dosh import cli; cli.run()"

    exe = dist.to_python_executable(
        name="dosh",
        packaging_policy=policy,
        config=python_config,
    )
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

    signer = code_signer_from_windows_store_auto()
    signer.activate()


register_code_signers()

register_target("exe", make_exe)
register_target("resources", make_embedded_resources, depends=["exe"], default_build_script=True)
register_target("install", make_install, depends=["exe"], default=True)
register_target("msi_installer", make_msi, depends=["exe"])

resolve_targets()
